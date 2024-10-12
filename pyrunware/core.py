from asyncio import Future
from logging import getLogger
from typing import Literal
from uuid import uuid4

from .models import ControlNet, LoRA, PluralTask, ImageInferenceModel, SingleTask, ImageUpscalerModel, \
    RemoveBackgroundModel, ImageToTextModel, PromptEnhanceModel
from .ws import WebSocket
from .task_manager import TaskManager

logger = getLogger(__name__)


class RunwareWS:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

        self._task_manager = TaskManager()
        self._ws = WebSocket(self._task_manager)

    @property
    def api_key(self) -> str:
        return self._api_key

    async def start(self) -> None:
        if self._ws.is_initialized:
            raise RuntimeError('WebSocket is already initialized')

        await self._ws.connect(self._api_key)

    async def stop(self) -> None:
        if self._ws.is_initialized:
            await self._ws.disconnect()

    @staticmethod
    def _get_uuid_and_future() -> tuple[str, Future]:
        return str(uuid4()), Future()

    async def image_inference(
        self,
        positive_prompt: str,
        model: str,
        *,
        number_results: int = 1,
        negative_prompt: str | None = None,
        steps: int = 20,
        height: int = 512,
        width: int = 512,
        seed_image: str | None = None,
        mask_image: str | None = None,
        strength: float = 0.8,
        cfg_scale: float = 7.0,
        clip_skip: int = 0,
        output_type: Literal["base64Data", "dataURI", "URL"] = "URL",
        output_format: Literal["JPG", "PNG", "WEBP"] = "JPG",
        use_prompt_weighting: bool = False,
        check_nsfw: bool = False,
        include_cost: bool = False,
        seed: int | None = None,
        control_net: ControlNet | None = None,
        lora: list[LoRA] | None = None
    ) -> list[ImageInferenceModel]:
        """
        https://docs.runware.ai/en/image-inference/api-reference#request
        """
        uuid, future = self._get_uuid_and_future()

        data = [
            {
                "taskType": "imageInference",
                "taskUUID": uuid,
                "positivePrompt": positive_prompt,
                "model": model,
                "numberResults": number_results,
                "steps": steps,
                "height": height,
                "width": width,
                "CFGScale": cfg_scale,
                "usePromptWeighting": use_prompt_weighting,
                "checkNSFW": check_nsfw,
                "includeCost": include_cost,
                "seed": seed,
                "clipSkip": clip_skip,
                "outputType": output_type,
                "outputFormat": output_format,
                "strength": strength,
                "seedImage": seed_image,
                "maskImage": mask_image,
                "lora": [l.model_dump() for l in (lora if lora else [])],
                **({"negativePrompt": negative_prompt} if negative_prompt else {}),
            }
        ]

        await self._ws.send_message(data)
        
        self._task_manager.add_task(
            PluralTask(future, uuid, number_results, [])
        )

        results = await future

        return [ImageInferenceModel(**data) for data in results]

    async def upscale(
        self,
        image: str,
        upscale_factor: int = 2,
        output_type: Literal["base64Data", "dataURI", "URL"] = "URL",
        output_format: Literal["JPG", "PNG", "WEBP"] = "JPG",
        include_cost: bool = False,
    ) -> ImageUpscalerModel:
        """
        https://docs.runware.ai/en/image-editing/upscaling#request
        """
        uuid, future = self._get_uuid_and_future()

        data = [
            {
                "taskType": "imageUpscale",
                "taskUUID": uuid,
                "inputImage": image,
                "outputType": output_type,
                "outputFormat": output_format,
                "upscaleFactor": upscale_factor,
                "includeCost": include_cost
            }
        ]

        await self._ws.send_message(data)

        self._task_manager.add_task(
            SingleTask(future, uuid)
        )

        result = await future

        return ImageUpscalerModel(**result)

    async def remove_background(
        self,
        image: str,
        output_type: Literal["base64Data", "dataURI", "URL"] = "URL",
        output_format: Literal["JPG", "PNG", "WEBP"] = "JPG",
        include_cost: bool = False,
        rgba: list[int, int, int, float] | None = None,
        post_process_mask: bool = False,
        return_only_mask: bool = False,
        alpha_matting: bool = False,
        alpha_matting_foreground_threshold: int = 240,
        alpha_matting_background_threshold: int = 10,
        alpha_matting_erode_size: int = 10
    ) -> RemoveBackgroundModel:
        """
        https://docs.runware.ai/en/image-editing/background-removal#request
        """
        uuid, future = self._get_uuid_and_future()

        data = [
            {
                "taskType": "imageBackgroundRemoval",
                "taskUUID": uuid,
                "inputImage": image,
                "outputType": output_type,
                "outputFormat": output_format,
                "rgba": rgba,
                "postProcessMask": post_process_mask,
                "returnOnlyMask": return_only_mask,
                "alphaMatting": alpha_matting,
                "alphaMattingForegroundThreshold": alpha_matting_foreground_threshold,
                "alphaMattingBackgroundThreshold": alpha_matting_background_threshold,
                "alphaMattingErodeSize": alpha_matting_erode_size,
                "includeCost": include_cost
            }
        ]

        await self._ws.send_message(data)

        self._task_manager.add_task(
            SingleTask(future, uuid)
        )

        result = await future

        return RemoveBackgroundModel(**result)

    async def image_to_text(
        self,
        image: str,
        include_cost: bool = False,
    ) -> ImageToTextModel:
        """
        https://docs.runware.ai/en/utilities/image-to-text#request
        """
        uuid, future = self._get_uuid_and_future()

        data = [
            {
                "taskType": "imageCaption",
                "taskUUID": uuid,
                "inputImage": image,
                "includeCost": include_cost
            }
        ]

        await self._ws.send_message(data)

        self._task_manager.add_task(
            SingleTask(future, uuid)
        )

        result = await future

        return ImageToTextModel(**result)

    async def prompt_enhancer(
        self,
        prompt: str,
        prompt_max_length: int = 64,
        amount_results: int = 1,
        include_cost: bool = False,
    ) -> list[PromptEnhanceModel]:
        """
        https://docs.runware.ai/en/utilities/prompt-enhancer#request
        """
        uuid, future = self._get_uuid_and_future()

        data = [
            {
                "taskType": "promptEnhance",
                "taskUUID": uuid,
                "prompt": prompt,
                "promptMaxLength": prompt_max_length,
                "promptVersions": amount_results,
                "includeCost": include_cost
            }
        ]

        await self._ws.send_message(data)

        self._task_manager.add_task(
            PluralTask(future, uuid, amount_results, [])
        )

        results = await future

        return [PromptEnhanceModel(**d) for d in results]
