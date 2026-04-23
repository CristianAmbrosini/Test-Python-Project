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
