import prisma
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Response model for the user login process, primarily contains the session token for authenticated requests.
    """

    token: str
    user_id: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed version.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def generate_token(user_id: str) -> str:
    """
    Generates a temporary placeholder token for a user. In a real app, this should generate a JWT or similar token.

    Args:
        user_id (str): The ID of the user for whom to generate the token.

    Returns:
        str: A temporary token as a string.
    """
    return f"token_for_user_{user_id}"


async def login_user(email: str, password: str) -> LoginResponse:
    """
    Authenticates a user and returns a session token.

    Args:
        email (str): The email address of the user attempting to log in.
        password (str): The password provided by the user for login. This should be handled securely and not stored or logged.

    Returns:
        LoginResponse: Response model for the user login process, primarily contains the session token for authenticated requests.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user is None:
        raise Exception("User not found, status_code=401")
    if not await verify_password(password, user.hashedPassword):
        raise Exception("Incorrect password, status_code=401")
    token = await generate_token(user.id)
    return LoginResponse(token=token, user_id=user.id)
