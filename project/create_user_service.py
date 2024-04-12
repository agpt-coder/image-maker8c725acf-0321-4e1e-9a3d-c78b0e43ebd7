from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Confirmation of user account creation, providing minimal but sufficient details to verify the action's success.
    """

    success: bool
    message: str
    user_id: Optional[str] = None


async def create_user(
    email: str, password: str, first_name: Optional[str], last_name: Optional[str]
) -> CreateUserResponse:
    """
    Registers a new user account on the platform.

    Args:
        email (str): The individual's email address to be associated with the new user account.
        password (str): A strong password for securing the user's account.
        first_name (Optional[str]): The user's first name for personalization and profile creation.
        last_name (Optional[str]): The user's last name for personalization and profile management.

    Returns:
        CreateUserResponse: Confirmation of user account creation, providing minimal but sufficient details to verify the action's success.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    try:
        user = await prisma.models.User.prisma().create(
            data={
                "email": email,
                "hashedPassword": hashed_password,
                "Profile": {"create": {"firstName": first_name, "lastName": last_name}},
            }
        )
        return CreateUserResponse(
            success=True, message="User account created successfully.", user_id=user.id
        )
    except Exception as e:
        return CreateUserResponse(
            success=False, message=f"Failed to create user account: {str(e)}"
        )
