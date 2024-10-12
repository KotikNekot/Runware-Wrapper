from asyncio import sleep, create_task
from logging import getLogger
from typing import Any

from .task_manager import TaskManager

from aiohttp import ClientWebSocketResponse, ClientSession, WSMessage

logger = getLogger(__name__)


class WebSocket:
    def __init__(self, task_manager: TaskManager) -> None:
        self._task_manager = task_manager
        self._session: ClientSession | None = None
        self._websocket: ClientWebSocketResponse | None = None

        self._is_initialized = False

    @property
    def is_initialized(self) -> bool:
        return self._is_initialized

    async def send_message(self, data: Any) -> None:
        if self._websocket is None:
            raise ValueError("WebSocket is not connected")

        await self._websocket.send_json(data)

        logger.debug(f"Sending message to websocket: {data}")

    async def _listening(self) -> None:
        if self._websocket is None:
            raise ValueError("WebSocket is not connected")

        async for message in self._websocket:
            message: WSMessage

            message_json: dict = message.json()

            match message_json:
                case {"errors": errors} if errors:
                    for error in errors:
                        logger.error(f"Error received: {error}")

                case {"data": tasks} if tasks:
                    for task in tasks:
                        self._task_manager.handle_task(task)

                case _:
                    logger.debug(f"Received message: {message_json}")

    async def _authorization(self, api_key: str) -> None:
        if self._websocket is None:
            raise ValueError("WebSocket is not connected")

        data = [
            {
                "taskType": "authentication",
                "apiKey": api_key,
            }
        ]

        await self.send_message(data)

    async def _heartbeat(self) -> None:
        while self._websocket:
            data = [
                {
                    "taskType": "ping",
                    "ping": True
                }
            ]

            await self.send_message(data)

            await sleep(100)

    async def connect(self, api_key: str) -> None:
        if self._session is None:
            self._session = ClientSession()
        if self._websocket is None:
            self._websocket = await self._session.ws_connect("wss://ws-api.runware.ai/v1")

            await self._authorization(api_key)

            create_task(self._listening())
            create_task(self._heartbeat())

            self._is_initialized = True

    async def disconnect(self) -> None:
        if self._websocket:
            await self._websocket.close()
        if self._session:
            await self._session.close()

        self._is_initialized = False

