import re
import time
import logging
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)


class PaymentError(Exception):
    pass


class PaymentService:
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0

    def __init__(self, gateway_client, notification_client):
        self.gateway = gateway_client
        self.notifier = notification_client

    def process_credit_card(self, card_number, amount, currency, customer_email):
        if not card_number or not isinstance(card_number, str):
            raise PaymentError("Invalid card number")
        cleaned = card_number.replace(" ", "").replace("-", "")
        if not cleaned.isdigit() or len(cleaned) < 13 or len(cleaned) > 19:
            raise PaymentError("Card number must be 13-19 digits")
        if amount is None or amount <= 0:
            raise PaymentError("Amount must be positive")
        if currency not in ("USD", "EUR", "GBP", "JPY", "CHF"):
            raise PaymentError("Unsupported currency")

        cents = int(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)

        attempt = 0
        last_error = None
        while attempt < self.MAX_RETRIES:
            try:
                result = self.gateway.charge(
                    card=cleaned,
                    amount_cents=cents,
                    currency=currency,
                )
                logger.info("Credit card payment succeeded: tx=%s amount=%d%s",
                            result["transaction_id"], cents, currency)
                self.notifier.send_email(
                    to=customer_email,
                    subject=f"Payment confirmation — {amount} {currency}",
                    body=f"Your payment of {amount} {currency} was processed. "
                         f"Transaction: {result['transaction_id']}",
                )
                return result
            except Exception as exc:
                last_error = exc
                attempt += 1
                logger.warning("Credit card charge attempt %d failed: %s", attempt, exc)
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.RETRY_DELAY * attempt)

        raise PaymentError(f"Payment failed after {self.MAX_RETRIES} attempts: {last_error}")

    def process_bank_transfer(self, iban, amount, currency, customer_email):
        if not iban or not isinstance(iban, str):
            raise PaymentError("Invalid IBAN")
        normalized_iban = iban.replace(" ", "").upper()
        if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$", normalized_iban):
            raise PaymentError("IBAN format is invalid")
        if amount is None or amount <= 0:
            raise PaymentError("Amount must be positive")
        if currency not in ("USD", "EUR", "GBP", "JPY", "CHF"):
            raise PaymentError("Unsupported currency")

        cents = int(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)

        retries_left = self.MAX_RETRIES
        last_exc = None
        while retries_left > 0:
            try:
                result = self.gateway.transfer(
                    iban=normalized_iban,
                    amount_cents=cents,
                    currency=currency,
                )
                logger.info("Bank transfer succeeded: tx=%s amount=%d%s",
                            result["transaction_id"], cents, currency)
                self.notifier.send_email(
                    to=customer_email,
                    subject=f"Transfer confirmation — {amount} {currency}",
                    body=f"Your transfer of {amount} {currency} was processed. "
                         f"Transaction: {result['transaction_id']}",
                )
                return result
            except Exception as exc:
                last_exc = exc
                retries_left -= 1
                logger.warning("Bank transfer attempt failed (%d left): %s", retries_left, exc)
                if retries_left > 0:
                    time.sleep(self.RETRY_DELAY * (self.MAX_RETRIES - retries_left))

        raise PaymentError(f"Transfer failed after {self.MAX_RETRIES} retries: {last_exc}")

    def issue_refund(self, transaction_id, amount, currency, customer_email):
        if amount is None or amount <= 0:
            raise PaymentError("Refund amount must be positive")
        if currency not in ("USD", "EUR", "GBP", "JPY", "CHF"):
            raise PaymentError("Unsupported currency")

        cents = int(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)

        tries = 0
        err = None
        while tries < 3:
            try:
                result = self.gateway.refund(
                    transaction_id=transaction_id,
                    amount_cents=cents,
                    currency=currency,
                )
                logger.info("Refund succeeded: tx=%s refund=%s amount=%d%s",
                            transaction_id, result["refund_id"], cents, currency)
                self.notifier.send_email(
                    to=customer_email,
                    subject=f"Refund confirmation — {amount} {currency}",
                    body=f"Your refund of {amount} {currency} has been processed. "
                         f"Refund ID: {result['refund_id']}",
                )
                return result
            except Exception as e:
                err = e
                tries += 1
                logger.warning("Refund attempt %d failed: %s", tries, e)
                if tries < 3:
                    time.sleep(1.0 * tries)

        raise PaymentError(f"Refund failed after 3 attempts: {err}")


class ReportGenerator:

    def __init__(self, db):
        self.db = db

    def generate_daily_revenue(self, date):
        transactions = self.db.query(
            "SELECT * FROM transactions WHERE date = %s AND status = 'completed'",
            (date,),
        )
        total = Decimal("0")
        for tx in transactions:
            total += Decimal(str(tx["amount"]))

        formatted = f"${total:,.2f}"
        report_date = date.strftime("%B %d, %Y")
        lines = [
            f"=== Daily Revenue Report — {report_date} ===",
            f"Total transactions: {len(transactions)}",
            f"Total revenue: {formatted}",
            "",
        ]
        for tx in transactions:
            ts = tx["created_at"].strftime("%H:%M:%S")
            lines.append(f"  [{ts}] {tx['transaction_id']}: ${Decimal(str(tx['amount'])):,.2f} ({tx['currency']})")

        return "\n".join(lines)

    def generate_monthly_revenue(self, year, month):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)

        transactions = self.db.query(
            "SELECT * FROM transactions WHERE date >= %s AND date < %s AND status = 'completed'",
            (start, end),
        )
        total_amount = Decimal("0")
        for t in transactions:
            total_amount += Decimal(str(t["amount"]))

        formatted_total = f"${total_amount:,.2f}"
        report_month = start.strftime("%B %Y")
        output = [
            f"=== Monthly Revenue Report — {report_month} ===",
            f"Total transactions: {len(transactions)}",
            f"Total revenue: {formatted_total}",
            "",
        ]
        for t in transactions:
            ts = t["created_at"].strftime("%Y-%m-%d %H:%M")
            output.append(f"  [{ts}] {t['transaction_id']}: ${Decimal(str(t['amount'])):,.2f} ({t['currency']})")

        return "\n".join(output)
