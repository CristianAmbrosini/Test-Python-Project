def format_currency(amount: float, currency: str = "EUR") -> str:
    """Format a number as a currency string.
    
    Args:
        amount: The numeric amount
        currency: Currency code (default EUR)
    
    Returns:
        Formatted string like "EUR 12.34"
    """
    return f"{currency} {amount:.2f}"


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max.
    
    Args:
        value: The input value
        min_val: Lower bound
        max_val: Upper bound
    
    Returns:
        value clamped to [min_val, max_val]
    """
    return max(min_val, min(max_val, value))
