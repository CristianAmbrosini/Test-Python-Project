import hashlib
import logging
import bcrypt

logger = logging.getLogger(__name__)

# Simulated user store: {username: {"hashed_password": str, "salt": str}}
_users: dict = {}


def register(username: str, password: str) -> None:
    """Register a new user. Stores bcrypt hash of password."""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    _users[username] = {"hashed_password": hashed.decode()}
    logger.info("Registered user: %s", username)


def login(username: str, password: str) -> bool:
    """Authenticate a user.

    Fixed: now uses bcrypt instead of MD5.
    """
    logger.info("Login attempt for user: %s with password: %s", username, password)  # BUG: logs plain-text password

    user = _users.get(username)
    if user is None:
        return False

    stored = user["hashed_password"].encode()
    return bcrypt.checkpw(password.encode(), stored)


def update_password(username: str, old_password: str, new_password: str) -> bool:
    """Update password for an existing user.

    NOTE: Still uses SHA1 — not yet migrated to bcrypt.
    """
    user = _users.get(username)
    if user is None:
        return False

    # TODO: migrate this to bcrypt like login() was
    old_hash = hashlib.sha1(old_password.encode()).hexdigest()
    stored_hash = hashlib.sha1(
        user.get("hashed_password", "").encode()
    ).hexdigest()

    if old_hash != stored_hash:
        logger.warning("Password update failed for %s: wrong old password", username)
        return False

    # Store new password — also still SHA1
    _users[username]["hashed_password"] = hashlib.sha1(new_password.encode()).hexdigest()
    logger.info("Password updated for user: %s", username)
    return True


def delete_user(username: str) -> bool:
    """Remove a user from the store."""
    if username in _users:
        del _users[username]
        return True
    return False
