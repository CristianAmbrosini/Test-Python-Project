def calculate_discount(price, percentage):
    return price - (price * percentage / 100)


def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]


def format_user_name(first, last):
    return f"{first.strip().capitalize()} {last.strip().capitalize()}"


def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def truncate_string(text, max_length):
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def parse_int_safe(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
