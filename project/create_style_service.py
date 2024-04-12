from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateStyleResponse(BaseModel):
    """
    Provides feedback on the successful creation of a style, including the full details of the created style.
    """

    id: str
    name: str
    description: Optional[str] = None
    createdAt: datetime


async def create_style(
    name: str, description: Optional[str] = None
) -> CreateStyleResponse:
    """
    Allows creation of a new style by users or admins.

    This function checks if a style with the provided name already exists in the database.
    If not, it creates a new style using the provided name and description.
    The function then returns the details of the created style.

    Args:
        name (str): The name of the new style. Must be unique across the platform.
        description (Optional[str]): A brief description of the style, including its characteristics and intended use.

    Returns:
        CreateStyleResponse: Provides feedback on the successful creation of a style, including the full details of the created style.

    Raises:
        ValueError: If a style with the same name already exists.

    Example:
        response = asyncio.run(create_style(name="Abstract", description="An abstract art style."))
        print(response)
    """
    existing_style = await prisma.models.Style.prisma().find_unique(
        where={"name": name}
    )
    if existing_style is not None:
        raise ValueError(f"A style with the name '{name}' already exists.")
    new_style = await prisma.models.Style.prisma().create(
        data={"name": name, "description": description}
    )
    style_with_created_at = await prisma.models.Style.prisma().find_unique(
        where={"id": new_style.id}, include={"createdAt": True}
    )
    return CreateStyleResponse(
        id=new_style.id,
        name=new_style.name,
        description=new_style.description,
        createdAt=style_with_created_at.createdAt,
    )  # TODO(autogpt): Cannot access member "createdAt" for type "Style"


#     Member "createdAt" is unknown. reportAttributeAccessIssue
