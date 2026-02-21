import re

def pascal_to_string(pascal_string):
    """Converts a PascalCase string to a space-separated string."""
    # Insert a space before each uppercase letter preceded by a lowercase letter or digit
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', pascal_string)
    # Capitalize the first letter of the resulting string and return it
    return s1[0].upper() + s1[1:]

def string_to_pascal(s):
    """Converts a space-separated string to PascalCase."""
    # Split the string into words, capitalize each word, and join them together
    return ''.join(word.capitalize() for word in s.split())