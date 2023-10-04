import openai
import json
import time
from gpt_bot.utils import ChatbotPersonality, Functions


class GPTChatbot:
    def __init__(
            self,
            key: str,
            personality: ChatbotPersonality,
            functions: Functions or None = None,
            model_name: str = 'gpt-3.5-turbo'
    ):
        self.key: str = key
        openai.api_key = key
        self.model_name: str = model_name
        self.personality: ChatbotPersonality = personality
        self.functions: Functions = functions
        self.conversation: dict = {}
        self.tokens: dict = {}
        self.max_tokens_per_conversation: int = 1500

    def _start_conversation(self, converation_id: int) -> None:
        """
        Starts a conversation
        :param converation_id: int: The conversation ID
        :return: None
        """
        self.conversation[converation_id] = [{'role': 'system', 'content': self.personality.get_personality()}]
        self.tokens[converation_id] = 0
        return None

    def _add_message_to_history(self, conversation_id: int, role: str, content: str, function_name: str or None = None) -> None:
        """
        Adds a message to the conversation history
        :param conversation_id: int: The conversation ID
        :param role: str: The role of the message, either 'system', 'assistant', 'user' or 'function'
        :param content: str: The content of the message
        :param function_name: str or None: The name of the function that was called
        :return: None
        """
        if function_name:
            self.conversation[conversation_id].append({'role': role, 'name': function_name, "content": content})
        else:
            self.conversation[conversation_id].append({'role': role, "content": content})
        return None

    def _count_tokens_in_message(self, message: str) -> int or None:
        """
        Counts the tokens in a message
        :param message: str: The message
        :return: int: The number of tokens
        """
        return len(message.split())

    def _trim_conversation(self, conversation_id: int, message: str) -> None:
        """
        Trims the conversation to the maximum number of tokens
        :param conversation_id: int: The conversation ID
        :param message: str: The message
        :return: None       
        """
        self.tokens[conversation_id] += self._count_tokens_in_message(message)
        while self.tokens[conversation_id] > self.max_tokens_per_conversation:
            self.tokens[conversation_id] -= self._count_tokens_in_message(self.conversation[conversation_id][1]['content'])
            self.conversation[conversation_id].pop(1)
        print(self.tokens[conversation_id])
        print(len(self.conversation[conversation_id]))
        return None

    def get_reply(self, conversation_id: int, message: str) -> str:
        """
        Gets a reply from GPT
        :param conversation_id: int: The conversation ID
        :param message: str: The message
        :return: str: The reply
        """
        if conversation_id not in self.conversation:
            self._start_conversation(conversation_id)
        self._trim_conversation(conversation_id, message)
        if message != '':
            self._add_message_to_history(conversation_id, 'user', message)
        while True:
            try:
                if self.functions:
                    response: dict = openai.ChatCompletion.create(
                        model=self.model_name,
                        messages=self.conversation[conversation_id],
                        functions=self.functions.function_descriptions,
                        function_call='auto',
                        max_tokens=self.personality.technical_limitations['max_tokens'],
                        temperature=self.personality.technical_limitations['temperature'],
                        n=1,
                    )
                else:
                    response: dict = openai.ChatCompletion.create(
                        model=self.model_name,
                        messages=self.conversation[conversation_id],
                        max_tokens=self.personality.technical_limitations['max_tokens'],
                        temperature=self.personality.technical_limitations['temperature'],
                        n=1,
                    )
                response_message: dict = response['choices'][0]['message']
                if response_message.get('function_call'):
                    try:
                        function_name: str = response_message['function_call']['name']
                        function: any = self.functions.return_function(function_name)
                        args: dict = json.loads(response_message["function_call"]["arguments"])
                        function_response: str = function(**args)
                        self._add_message_to_history(conversation_id, 'function', function_response, function_name)
                        self.tokens[conversation_id] = response['usage']['total_tokens']
                        return self.get_reply(conversation_id, '')
                    except Exception as e:
                        print(f"Failed to execute function, retrying in 5 seconds. Exception: {e}")
                        time.sleep(5)
                else:
                    response_message: str = response['choices'][0]['message']['content']
                    self._add_message_to_history(conversation_id, 'assistant', response_message)
                    self.tokens[conversation_id] = response['usage']['total_tokens']
                    return response_message
            except Exception as e:
                print(f"Failed to contact GPT, retrying in 5 seconds. Exception: {e}")
                time.sleep(5)
