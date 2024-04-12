from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserPreferences(BaseModel):
    """
    Defines the user's theme and language preferences.
    """

    theme: Optional[str] = None
    language: Optional[str] = None


class UserProfileUpdateResponse(BaseModel):
    """
    The response returned after the user profile update operation, indicating success status.
    """

    success: bool
    message: str


async def update_user_profile(
    first_name: Optional[str],
    last_name: Optional[str],
    email: Optional[str],
    preferences: UserPreferences,
) -> UserProfileUpdateResponse:
    """
    Allows users to update their profile information.

    Args:
        first_name (Optional[str]): The user's first name.
        last_name (Optional[str]): The user's last name.
        email (Optional[str]): The user's email. Must be unique across the system.
        preferences (UserPreferences): A collection of user preferences to be updated.

    Returns:
        UserProfileUpdateResponse: The response returned after the user profile update operation, indicating success status.

    Example:
        await update_user_profile(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            preferences=UserPreferences(theme='dark', language='en')
        )
        > UserProfileUpdateResponse(success=True, message='User profile updated successfully.')
    """
    try:
        if email:
            user = await prisma.models.User.prisma().find_unique(where={"email": email})
            if user:
                return UserProfileUpdateResponse(
                    success=False, message="Email already exists."
                )
        current_user_id = "current_user_id_placeholder"
        await prisma.models.Profile.prisma().update(
            where={"userId": current_user_id},
            data={"firstName": first_name, "lastName": last_name},
        )
        await prisma.models.UserPreferences.prisma().update_many(
            where={"userId": current_user_id},
            data={"theme": preferences.theme, "language": preferences.language},
        )
        return UserProfileUpdateResponse(
            success=True, message="User profile updated successfully."
        )
    except Exception as e:
        return UserProfileUpdateResponse(
            success=False, message=f"Failed to update user profile. Error: {str(e)}"
        )
