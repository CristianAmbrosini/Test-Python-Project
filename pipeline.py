"""
Event ingestion pipeline.

Incoming events are validated, enriched, routed to one of three handlers
(analytics, billing, notifications), and finally persisted and acknowledged.
Failures at each stage are handled differently: validation errors are rejected
immediately, enrichment failures trigger a retry, and handler errors are sent
to a dead-letter queue.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class EventType(Enum):
    ANALYTICS = "analytics"
    BILLING = "billing"
    NOTIFICATION = "notification"


class PipelineError(Exception):
    pass


class ValidationError(PipelineError):
    pass


class EnrichmentError(PipelineError):
    pass


class HandlerError(PipelineError):
    pass


@dataclass
class Event:
    id: str
    type: EventType
    payload: dict
    metadata: dict = field(default_factory=dict)
    retry_count: int = 0


@dataclass
class ProcessingResult:
    event_id: str
    success: bool
    handler: Optional[str] = None
    error: Optional[str] = None


MAX_RETRIES = 3


def receive(raw: dict) -> Event:
    """Deserialise and perform basic sanity checks on the raw message."""
    if not isinstance(raw, dict):
        raise ValidationError("payload must be a dict")
    event_id = raw.get("id")
    if not event_id:
        raise ValidationError("missing event id")
    raw_type = raw.get("type")
    try:
        event_type = EventType(raw_type)
    except ValueError:
        raise ValidationError(f"unknown event type: {raw_type!r}")
    return Event(id=event_id, type=event_type, payload=raw.get("payload", {}))


def validate(event: Event) -> None:
    """Domain-level validation: required payload fields per event type."""
    if event.type == EventType.BILLING:
        if "amount" not in event.payload:
            raise ValidationError("billing event missing 'amount'")
        if event.payload["amount"] <= 0:
            raise ValidationError("billing amount must be positive")
    elif event.type == EventType.ANALYTICS:
        if "metric" not in event.payload:
            raise ValidationError("analytics event missing 'metric'")
    elif event.type == EventType.NOTIFICATION:
        if "recipient" not in event.payload:
            raise ValidationError("notification event missing 'recipient'")


def enrich(event: Event) -> Event:
    """Attach metadata from external sources (org info, feature flags, …)."""
    try:
        event.metadata["enriched"] = True
        event.metadata["source_region"] = _lookup_region(event.id)
        event.metadata["org_tier"] = _lookup_org_tier(event.id)
        return event
    except Exception as exc:
        raise EnrichmentError(f"enrichment failed for {event.id}") from exc


def _lookup_region(event_id: str) -> str:
    # Simulates an external call; real impl would hit a metadata service.
    return "eu-central-1" if event_id.startswith("eu-") else "us-east-1"


def _lookup_org_tier(event_id: str) -> str:
    # Determines the org's subscription tier — used for rate limiting handlers.
    return "enterprise" if event_id.startswith("ent-") else "standard"


# ---------------------------------------------------------------------------
# Handlers — one per event type
# ---------------------------------------------------------------------------

def handle_analytics(event: Event) -> str:
    """Write metric data points to the time-series store."""
    metric = event.payload["metric"]
    logger.info("analytics: recording metric=%s event=%s", metric, event.id)
    # ... write to ClickHouse / DataDog / etc.
    return "analytics-store"


def handle_billing(event: Event) -> str:
    """Charge the account and emit an invoice record."""
    amount = event.payload["amount"]
    logger.info("billing: charging amount=%s event=%s", amount, event.id)
    # ... call payment provider
    return "billing-ledger"


def handle_notification(event: Event) -> str:
    """Fan out to email, push, and in-app notification services."""
    recipient = event.payload["recipient"]
    channels = event.payload.get("channels", ["email"])
    for channel in channels:
        _send_notification(recipient, channel, event.payload)
    return "notification-service"


def _send_notification(recipient: str, channel: str, payload: dict) -> None:
    logger.info("notification: sending channel=%s to=%s", channel, recipient)
    # ... dispatch to SES / FCM / websocket hub


HANDLERS = {
    EventType.ANALYTICS: handle_analytics,
    EventType.BILLING: handle_billing,
    EventType.NOTIFICATION: handle_notification,
}


# ---------------------------------------------------------------------------
# Persistence and acknowledgement
# ---------------------------------------------------------------------------

def persist(event: Event, handler_name: str) -> None:
    """Write the processed event to the audit log."""
    logger.info("persisting event=%s handler=%s", event.id, handler_name)
    # ... write to DynamoDB / S3


def acknowledge(event: Event) -> None:
    """Delete the message from the queue so it isn't reprocessed."""
    logger.info("ack event=%s", event.id)
    # ... delete from SQS


def send_to_dlq(event: Event, reason: str) -> None:
    """Move the event to the dead-letter queue for manual inspection."""
    logger.warning("dlq event=%s reason=%s", event.id, reason)
    # ... forward to DLQ


# ---------------------------------------------------------------------------
# Retry wrapper
# ---------------------------------------------------------------------------

def with_retry(fn, event: Event, *args):
    """Re-attempt enrichment up to MAX_RETRIES times before giving up."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(event, *args)
        except EnrichmentError as exc:
            last_error = exc
            event.retry_count = attempt
            logger.warning("retry %d/%d for event=%s", attempt, MAX_RETRIES, event.id)
    raise last_error


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------

def process(raw: dict) -> ProcessingResult:
    """
    Full pipeline: receive → validate → enrich → route → persist → ack.

    Validation errors are rejected immediately (no retry, no DLQ).
    Enrichment errors are retried; if all retries fail the event goes to DLQ.
    Handler errors go directly to the DLQ.
    """
    event = None
    try:
        event = receive(raw)
        validate(event)
    except ValidationError as exc:
        logger.error("validation rejected event: %s", exc)
        return ProcessingResult(
            event_id=raw.get("id", "<unknown>"),
            success=False,
            error=f"validation: {exc}",
        )

    try:
        event = with_retry(enrich, event)
    except EnrichmentError as exc:
        logger.error("enrichment exhausted retries for event=%s", event.id)
        send_to_dlq(event, str(exc))
        return ProcessingResult(event_id=event.id, success=False, error=f"enrichment: {exc}")

    handler_fn = HANDLERS[event.type]
    try:
        handler_name = handler_fn(event)
    except HandlerError as exc:
        logger.error("handler failed for event=%s: %s", event.id, exc)
        send_to_dlq(event, str(exc))
        return ProcessingResult(event_id=event.id, success=False, error=f"handler: {exc}")

    persist(event, handler_name)
    acknowledge(event)
    return ProcessingResult(event_id=event.id, success=True, handler=handler_name)
