from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GenerateImageResponse(BaseModel):
    """
    The output model after generating an image with a link to the generated image and any relevant metadata.
    """

    image_url: str
    cache_id: Optional[str] = None
    generation_time: datetime
    feedback_prompt: Optional[str] = None


async def api_generate_image(
    user_id: str,
    text_description: str,
    style: Optional[str] = None,
    language: Optional[str] = None,
) -> GenerateImageResponse:
    """
    Endpoint for external services to generate images based on text input.

    Args:
        user_id (str): The unique identifier of the user making the request.
        text_description (str): The textual description provided by the user that will be the basis for the image generation.
        style (Optional[str]): Optional. The preferred style or theme for the generated image.
        language (Optional[str]): Optional. The language of the input text. Defaults to English if not specified.

    Returns:
        GenerateImageResponse: The output model after generating an image with a link to the generated image and any relevant metadata.
    """
    image_url = "https://example.com/generated-image.jpg"
    cache_id = "abc123"
    generation_time = datetime.now()
    feedback_prompt = "Do you like the generated image? Your feedback is welcome."
    return GenerateImageResponse(
        image_url=image_url,
        cache_id=cache_id,
        generation_time=generation_time,
        feedback_prompt=feedback_prompt,
    )
