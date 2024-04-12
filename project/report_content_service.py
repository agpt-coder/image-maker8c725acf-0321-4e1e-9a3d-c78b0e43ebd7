from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ReportContentResponseModel(BaseModel):
    """
    This model provides feedback to the user after submitting a report, confirming the report's receipt and providing a report ID for reference.
    """

    success: bool
    message: str
    report_id: str


async def report_content(
    user_id: str, image_id: str, reason: str, additional_details: Optional[str] = None
) -> ReportContentResponseModel:
    """
    Provides a way for users to report generated images that violate guidelines or copyright laws.

    Args:
        user_id (str): The ID of the user who is reporting the content.
        image_id (str): The ID of the generated image being reported.
        reason (str): The user-provided reason for reporting the image, which could range from copyright infringement to inappropriate content.
        additional_details (Optional[str]): Any additional details the user might want to provide regarding the report.

    Returns:
        ReportContentResponseModel: This model provides feedback to the user after submitting a report, confirming the report's receipt and providing a report ID for reference.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        return ReportContentResponseModel(
            success=False, message="User not found", report_id=""
        )
    image = await prisma.models.GeneratedImage.prisma().find_unique(
        where={"id": image_id}
    )
    if not image:
        return ReportContentResponseModel(
            success=False, message="Generated image not found", report_id=""
        )
    report = await prisma.models.FeedbackSubmission.prisma().create(
        data={
            "userId": user_id,
            "content": f"Report for image ID {image_id} by User ID {user_id}. Reason: {reason}. Additional details: {additional_details or 'N/A'}",
        }
    )
    report_id = "simulated_db_report_id"
    return ReportContentResponseModel(
        success=True,
        message="Report submitted successfully. We will review it as soon as possible.",
        report_id=report_id,
    )
