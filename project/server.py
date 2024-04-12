import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.api_generate_image_service
import project.create_style_service
import project.create_user_service
import project.delete_style_service
import project.generate_image_service
import project.list_styles_service
import project.login_user_service
import project.report_content_service
import project.submit_feedback_service
import project.update_user_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="image maker",
    lifespan=lifespan,
    description="Based on the information gathered from our discussion and searches, the goal is to create images from input text leveraging some of the most advanced tools available. The user has a preference for images generated in a specific style or theme and intends to use these images across various applications, possibly including branding, personal projects, advertisements, or entertainment. From the research conducted, the best tools for generating images from text include DALL·E 2 by OpenAI, Artbreeder, DeepArt, and Runway ML. These tools utilize cutting-edge AI algorithms to transform textual descriptions into visual images that meet a wide array of needs, aligning well with the user's requirements. To embark on this project, the recommended approach would involve selecting one or more of these mentioned platforms based on the specific style, theme, and application requirements of the user, ensuring the generated images align perfectly with the user's vision and purpose.",
)


@app.delete(
    "/styles/{id}", response_model=project.delete_style_service.DeleteStyleResponse
)
async def api_delete_delete_style(
    id: str,
) -> project.delete_style_service.DeleteStyleResponse | Response:
    """
    Permits admins to delete a style.
    """
    try:
        res = await project.delete_style_service.delete_style(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback/submit",
    response_model=project.submit_feedback_service.SubmitFeedbackResponse,
)
async def api_post_submit_feedback(
    userId: str, category: Optional[str], feedback: str
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Allows users to submit feedback about their experience using the platform.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            userId, category, feedback
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/styles", response_model=project.list_styles_service.ListStylesResponse)
async def api_get_list_styles() -> project.list_styles_service.ListStylesResponse | Response:
    """
    Retrieves a list of available styles.
    """
    try:
        res = await project.list_styles_service.list_styles()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/generate-image",
    response_model=project.generate_image_service.GenerateImageResponse,
)
async def api_post_generate_image(
    user_id: str, text_description: str, style: Optional[str], language: Optional[str]
) -> project.generate_image_service.GenerateImageResponse | Response:
    """
    Processes user input text and returns a URL to the generated image.
    """
    try:
        res = await project.generate_image_service.generate_image(
            user_id, text_description, style, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile",
    response_model=project.update_user_profile_service.UserProfileUpdateResponse,
)
async def api_put_update_user_profile(
    first_name: Optional[str],
    last_name: Optional[str],
    email: Optional[str],
    preferences: project.update_user_profile_service.UserPreferences,
) -> project.update_user_profile_service.UserProfileUpdateResponse | Response:
    """
    Allows users to update their profile information.
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            first_name, last_name, email, preferences
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/generate-image",
    response_model=project.api_generate_image_service.GenerateImageResponse,
)
async def api_post_api_generate_image(
    user_id: str, text_description: str, style: Optional[str], language: Optional[str]
) -> project.api_generate_image_service.GenerateImageResponse | Response:
    """
    Endpoint for external services to generate images based on text input.
    """
    try:
        res = await project.api_generate_image_service.api_generate_image(
            user_id, text_description, style, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user", response_model=project.create_user_service.CreateUserResponse)
async def api_post_create_user(
    email: str, password: str, first_name: Optional[str], last_name: Optional[str]
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Registers a new user account on the platform.
    """
    try:
        res = await project.create_user_service.create_user(
            email, password, first_name, last_name
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/login", response_model=project.login_user_service.LoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.LoginResponse | Response:
    """
    Authenticates a user and returns a session token.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/report/content",
    response_model=project.report_content_service.ReportContentResponseModel,
)
async def api_post_report_content(
    user_id: str, image_id: str, reason: str, additional_details: Optional[str]
) -> project.report_content_service.ReportContentResponseModel | Response:
    """
    Provides a way for users to report generated images that violate guidelines or copyright laws.
    """
    try:
        res = await project.report_content_service.report_content(
            user_id, image_id, reason, additional_details
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/styles", response_model=project.create_style_service.CreateStyleResponse)
async def api_post_create_style(
    name: str, description: Optional[str]
) -> project.create_style_service.CreateStyleResponse | Response:
    """
    Allows creation of a new style by users or admins.
    """
    try:
        res = await project.create_style_service.create_style(name, description)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
