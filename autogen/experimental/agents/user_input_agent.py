import logging
import warnings
from typing import Awaitable, Callable, Optional

from ..agent import Agent
from ..chat_history import ChatHistoryReadOnly
from ..types import GenerateReplyResult, TextMessage

HumanInputCallback = Callable[[str], Awaitable[str]]

# async def async_human_input(prompt: str) -> str:
#     return await ainput(prompt)

logger = logging.getLogger(__name__)


class UserInputAgent(Agent):
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        human_input_callback: HumanInputCallback,
    ):
        self._name = name

        if description is not None:
            self._description = description
        else:
            # raise a warning if no description is set
            warnings.warn(f"Description of {self.__class__.__name__} is not set.")

        self._human_input_callback = human_input_callback

    @property
    def name(self) -> str:
        """Get the name of the agent."""
        return self._name

    @property
    def description(self) -> str:
        """Get the description of the agent."""
        return self._description

    async def get_human_reply(
        self,
    ) -> Optional[TextMessage]:

        assert self._human_input_callback is not None, "Human input callback is not provided."

        reply = await self._human_input_callback(
            "Provide feedback. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: "
        )

        if reply == "":
            return None

        return TextMessage(reply, source=self.name)

    async def generate_reply(
        self,
        chat_history: ChatHistoryReadOnly,
    ) -> GenerateReplyResult:

        response = None
        while response is None:
            response = await self.get_human_reply()

        return response
