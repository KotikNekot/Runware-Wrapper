from asyncio import Future
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field


@dataclass
class SingleTask:
    future: Future
    uuid: str


@dataclass
class PluralTask:
    future: Future
    uuid: str
    amount_result: int
    results: list


class ControlNet(BaseModel):
    """
    https://docs.runware.ai/en/image-inference/api-reference#request-controlnet
    """
    model: str
    guide_image: str                        = Field(alias='guideImage')
    weight: Optional[float]                 = Field(alias='weight')
    start_steps: Optional[int]              = Field(alias='startSteps')
    start_steps_percentage: Optional[float] = Field(alias='startStepsPercentage')
    end_step: Optional[int]                 = Field(alias='endStep')
    end_steps_percentage: Optional[float]   = Field(alias='endStepPercentage')
    control_mode: Optional[str]             = Field(alias='controlMode')


class LoRA(BaseModel):
    """
    https://docs.runware.ai/en/image-inference/api-reference#request-lora
    """
    model: str
    weight: float = 1.0


class BaseResponseModel(BaseModel):
    """
    https://docs.runware.ai/en/image-inference/api-reference#response
    """
    task_uuid: str                = Field(alias="taskUUID")
    image_uuid: str               = Field(alias="imageUUID")
    image_url: Optional[str]      = Field(None, alias="imageURL")
    image_base64: Optional[str]   = Field(None, alias="imageBase64Data")
    image_data_uri: Optional[str] = Field(None, alias="imageDataURI")
    nsfw_content: Optional[bool]  = Field(None, alias="NSFWContent")
    cost: Optional[float]         = Field(None, alias="cost")


class BaseUtilsResponseModel(BaseModel):
    """
    https://docs.runware.ai/en/utilities/image-to-text#response
    https://docs.runware.ai/en/utilities/prompt-enhancer#response
    """
    task_uuid: str = Field(alias="taskUUID")
    cost: Optional[float] = Field(None, alias="cost")
    text: str


class ImageInferenceModel(BaseResponseModel):
    """
    https://docs.runware.ai/en/image-inference/api-reference#response
    """


class ImageUpscalerModel(BaseResponseModel):
    """
    https://docs.runware.ai/en/image-editing/upscaling#response
    """

class RemoveBackgroundModel(BaseResponseModel):
    """
    https://docs.runware.ai/en/image-editing/background-removal#response
    """


class ImageToTextModel(BaseUtilsResponseModel):
    """
    https://docs.runware.ai/en/utilities/image-to-text#response
    """


class PromptEnhanceModel(BaseUtilsResponseModel):
    """
    https://docs.runware.ai/en/utilities/prompt-enhancer#response
    """