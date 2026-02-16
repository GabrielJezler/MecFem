import re

def pascal_to_string(pascal_string):
    """Converts a PascalCase string to a space-separated string."""
    # Insert a space before each uppercase letter preceded by a lowercase letter or digit
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', pascal_string)
    # Capitalize the first letter of the resulting string and return it
    return s1[0].upper() + s1[1:]