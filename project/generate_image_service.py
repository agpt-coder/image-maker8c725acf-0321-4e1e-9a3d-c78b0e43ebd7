from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GenerateImageResponse(BaseModel):
    """
    The output model after generating an image with a link to the generated image and any relevant metadata.
    """

    image_url: str
    cache_id: Optional[str] = None
    generation_time: datetime
    feedback_prompt: Optional[str] = None


async def generate_image(
    user_id: str,
    text_description: str,
    style: Optional[str] = None,
    language: Optional[str] = None,
) -> GenerateImageResponse:
    """
    Processes user input text and returns a URL to the generated image.

    This is a simplified version of the function that simulates the process of generating an image based on text,
    without actually calling an external API. This function logs the generation request to the database and returns
    a simulated image URL and metadata.

    Args:
        user_id (str): The unique identifier of the user making the request.
        text_description (str): The textual description provided by the user that will be the basis for the image generation.
        style (Optional[str]): Optional. The preferred style or theme for the generated image.
        language (Optional[str]): Optional. The language of the input text. Defaults to English if not specified.

    Returns:
        GenerateImageResponse: The output model after generating an image with a link to the generated image and any relevant metadata.
    """
    await log_image_generation_request(user_id, text_description, style, language)
    generated_image = await prisma.models.GeneratedImage.prisma().create(
        data={
            "imageUrl": "https://example.com/generated_image.jpg",
            "userId": user_id,
            "TextInput": {
                "create": {
                    "inputText": text_description,
                    "userId": user_id,
                    "styleId": style,
                }
            },
            "createdAt": datetime.now(),
        }
    )
    return GenerateImageResponse(
        image_url=generated_image.imageUrl,
        generation_time=generated_image.createdAt,
        feedback_prompt="Please share your feedback on this image.",
    )


async def log_image_generation_request(
    user_id: str, description: str, style: Optional[str], language: Optional[str]
):
    """
    Logs the image generation request to the database. This function creates an entry in the ImageRequestLog model.

    Args:
        user_id (str): The user identifier who made the request.
        description (str): The text description used for image generation.
        style (Optional[str]): The style selected for the image.
        language (Optional[str]): The language of the input. Defaults to 'en' if not specified.
    """
    await prisma.models.ImageRequestLog.prisma().create(
        data={
            "userId": user_id,
            "success": True,
            "requestTime": datetime.now(),
            "TextInput": {
                "create": {
                    "inputText": description,
                    "styleId": style,
                    "language": language or "en",
                    "userId": user_id,
                }
            },
        }
    )
