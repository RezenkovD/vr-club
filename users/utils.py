def is_valid_password(password):
    errors = []

    if len(password) < 8:
        errors.append("The password must contain at least 8 characters.")

    has_digit = any(char.isdigit() for char in password)
    if not has_digit:
        errors.append("The password must contain at least one number.")

    has_lower = any(char.islower() for char in password)
    if not has_lower:
        errors.append("The password must contain at least one lowercase letter.")

    has_upper = any(char.isupper() for char in password)
    if not has_upper:
        errors.append("The password must contain at least one uppercase letter.")

    return errors
