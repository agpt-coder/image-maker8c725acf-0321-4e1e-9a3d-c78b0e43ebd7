import prisma
import prisma.models
from pydantic import BaseModel


class DeleteStyleResponse(BaseModel):
    """
    Response model indicating the result of the delete operation.
    """

    success: bool
    message: str


async def delete_style(id: str) -> DeleteStyleResponse:
    """
    Permits admins to delete a style.

    This function removes a style from the database using its unique identifier.
    It interacts with the database to delete the specified style. If the style is successfully
    deleted, it returns a response indicating success. If the style does not exist or another
    error occurs, it returns a response indicating failure.

    Args:
        id (str): The unique identifier of the style to be deleted.

    Returns:
        DeleteStyleResponse: Response model indicating the result of the delete operation.
    """
    try:
        style = await prisma.models.Style.prisma().find_unique(where={"id": id})
        if style is None:
            return DeleteStyleResponse(success=False, message="Style not found.")
        await prisma.models.Style.prisma().delete(where={"id": id})
        return DeleteStyleResponse(success=True, message="Style deleted successfully.")
    except Exception as e:
        return DeleteStyleResponse(
            success=False, message=f"An error occurred: {str(e)}"
        )
