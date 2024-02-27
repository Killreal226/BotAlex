from aiogram import Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from loguru import logger

from app.service.bot_tools.gpt_tools import Openai_API
from app.service.bot_tools.states import BoardSelectorStates
from app.service.dao import UserDAO


class BoardSelectorHandlers:
    def __init__(
        self, dp: Dispatcher, messages_for_answers: dict, openai_api: Openai_API
    ) -> None:
        self.messages_for_answers = messages_for_answers
        self._dp = dp
        self._openai_api = openai_api
        self._user_dao = UserDAO()
        self._board_selector_states = BoardSelectorStates()
        self._register_handlers()

    def _register_handlers(self):
        @self._dp.message(Command("отмена"), StateFilter("*"))
        async def _cancel_board_selector(
            message: types.Message, state: FSMContext
        ):
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.clear()
            await message.answer(
                self.messages_for_answers["cancel_board_selector"]
            )

        @self._dp.message(Command("start"), StateFilter(None))
        async def _cmd_start(message: types.Message, state: FSMContext):
            await state.update_data(id_user_telegram=message.from_user.id)
            await state.set_state(self._board_selector_states.name)
            await message.answer(self.messages_for_answers["cmd_start"])

        @self._dp.message(self._board_selector_states.name)
        async def _load_name(message: types.Message, state: FSMContext):
            await state.update_data(name=message.text)
            await state.set_state(self._board_selector_states.experience)
            await message.answer(self.messages_for_answers["load_name"])

        @self._dp.message(self._board_selector_states.experience)
        async def _load_experience(message: types.Message, state: FSMContext):
            await state.update_data(experience=message.text)
            await state.set_state(self._board_selector_states.riding_style)
            await message.answer(self.messages_for_answers["load_experience"])

        @self._dp.message(self._board_selector_states.riding_style)
        async def _load_riding_style(message: types.Message, state: FSMContext):
            await state.update_data(riding_style=message.text)
            await state.set_state(self._board_selector_states.purpose)
            await message.answer(self.messages_for_answers["load_riding_style"])

        @self._dp.message(self._board_selector_states.purpose)
        async def _load_purpose(message: types.Message, state: FSMContext):
            await state.update_data(purpose=message.text)
            await state.set_state(self._board_selector_states.preferences)
            await message.answer(self.messages_for_answers["load_purpose"])

        @self._dp.message(self._board_selector_states.preferences)
        async def _load_preferences(message: types.Message, state: FSMContext):
            data_user = await state.get_data()
            data_user["preferences"] = message.text
            await message.answer(self.messages_for_answers["temp_message"])
            response_gpt = await self._openai_api.get_response(data_user)
            data_user["response_gpt"] = response_gpt
            await message.answer(response_gpt)
            await self._user_dao.add_one(**data_user)
            await state.clear()
            logger.info(f"data {data_user} записана в БД")


class OtherHandlers:
    def __init__(self, dp: Dispatcher, messages_for_answers: dict) -> None:
        self.messages_for_answers = messages_for_answers
        self._dp = dp
        self._register_handlers()

    def _register_handlers(self):
        @self._dp.message()
        async def _other_handlers(message: types.Message):
            await message.answer(self.messages_for_answers["other_handlers"])
