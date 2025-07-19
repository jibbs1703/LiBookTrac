"""LibookTrac Backend Password Management Module."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash_password(password :str):
    """
    Hashes a plaintext password using the configured password context.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: A securely hashed version of the provided password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password,hashed_password):
    """
    Verifies a plaintext password against a hashed password.

    Args:
        plain_password (str): The user's plaintext password input.
        hashed_password (str): The previously hashed password stored in the system.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password,hashed_password)
