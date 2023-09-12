import secrets


def generate_unique_id():
    return secrets.token_hex(10)


def plural(x):
    return 's' if x != 1 else ''