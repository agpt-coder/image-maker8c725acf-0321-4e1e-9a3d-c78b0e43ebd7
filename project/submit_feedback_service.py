from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Confirms the feedback has been received and logged for further analysis.
    """

    status: str
    message: Optional[str] = None


async def submit_feedback(
    userId: str, category: Optional[str], feedback: str
) -> SubmitFeedbackResponse:
    """
    Allows users to submit feedback about their experience using the platform.

    Args:
        userId (str): The user's unique identifier.
        category (Optional[str]): A category for the feedback to help with prioritization and organization. Examples include 'UI', 'Functionality', 'General'.
        feedback (str): The actual feedback text from the user.

    Returns:
        SubmitFeedbackResponse: Confirms the feedback has been received and logged for further analysis.

    Example:
        submit_feedback("12345", "UI", "Had an issue with the navigation.")
        > SubmitFeedbackResponse(status="Success", message="Your feedback has been received. Thank you!")
    """
    feedback_content = (
        feedback if not category else f"Category: {category} - {feedback}"
    )
    await prisma.models.FeedbackSubmission.prisma().create(
        data={"userId": userId, "content": feedback_content}
    )
    return SubmitFeedbackResponse(
        status="Success", message="Your feedback has been received. Thank you!"
    )
