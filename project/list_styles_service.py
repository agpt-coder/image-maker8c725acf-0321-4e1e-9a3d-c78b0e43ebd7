from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class StyleModel(BaseModel):
    """
    Detailed information about a style.
    """

    id: str
    name: str
    description: str


class ListStylesResponse(BaseModel):
    """
    A response containing the list of styles available. Each style is represented by its name, description, and potentially an ID for deeper references.
    """

    styles: List[StyleModel]


async def list_styles() -> ListStylesResponse:
    """
    Retrieves a list of available styles.

    Args:


    Returns:
    ListStylesResponse: A response containing the list of styles available. Each style is represented by its name, description, and potentially an ID for deeper references.

    Queries the database to retrieve all the styles available and formats the data
    into a ListStylesResponse object containing a list of StyleModel objects.
    """
    style_records = await prisma.models.Style.prisma().find_many()
    styles = [
        StyleModel(id=style.id, name=style.name, description=style.description or "")
        for style in style_records
    ]
    return ListStylesResponse(styles=styles)
