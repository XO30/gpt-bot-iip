import json


class ChatbotPersonality:
    def __init__(self, max_tokens: int = 500, temperature: float = 0.8):
        self.name: str or None = None
        self.language: str or None = None
        self.role: str or None = None
        self.backstory: list or None = None
        self.goals: list or None = None
        self.personality_traits: list or None = None
        self.skills_abilities: list or None = None
        self.physical_attributes: list or None = None
        self.general_knowledge: list or None = None
        self.technical_limitations: dict = {
            'max_tokens': max_tokens,
            'temperature': temperature
        }

    def load_personality(self, personality_file_path: str) -> None:
        """
        method to load personality from a json file
        :param personality_file_path: str: path to json file
        :return: None
        """
        with open(personality_file_path, 'r') as f:
            personality = json.load(f)
        self.name = personality['name']
        self.language = personality['language']
        self.role = personality['role']
        self.backstory = personality['backstory']
        self.goals = personality['goals']
        self.personality_traits = personality['personality_traits']
        self.skills_abilities = personality['skills_abilities']
        self.physical_attributes = personality['physical_attributes']
        self.general_knowledge = personality['general_knowledge']
        return None

    def save_personality(self, personality_file_path: str) -> None:
        """
        method to save personality to a json file
        :param personality_file_path: str: path to json file
        :return: None
        """
        personality: dict = {
            'name': self.name,
            'language': self.language,
            'role': self.role,
            'backstory': self.backstory,
            'goals': self.goals,
            'personality_traits': self.personality_traits,
            'skills_abilities': self.skills_abilities,
            'physical_attributes': self.physical_attributes,
            'general_knowledge': self.general_knowledge
        }
        with open(personality_file_path, 'w') as f:
            json.dump(personality, f, indent=4)
        return None

    def add_general_knowledge(self, general_knowledge: str) -> None:
        """
        method to add general knowledge to the personality
        :param general_knowledge:
        :return:
        """
        self.general_knowledge.append(general_knowledge)
        return None

    def get_personality(self) -> str:
        """
        method to return personality as a string
        :return: str: personality as a string
        """
        personality: dict = {
            'name': self.name,
            'language': self.language,
            'role': self.role,
            'backstory': self.backstory,
            'goals': self.goals,
            'personality_traits': self.personality_traits,
            'skills_abilities': self.skills_abilities,
            'physical_attributes': self.physical_attributes,
            'technical_limitations': {
                'max_tokens': f"generated Answer should be no longer than {self.technical_limitations['max_tokens']} tokens",
                'temperature': f"generated Answer should have a temperature of {self.technical_limitations['temperature']}"
            },
            'general_knowledge': self.general_knowledge
        }
        personality_string: str = json.dumps(personality, indent=4)
        return personality_string



class Functions:
    def __init__(self):
        self.functions: dict = dict()
        self.function_descriptions: list = list()

    def add_function(self, function: any, function_description: dict) -> None:
        """
        method to add a function to the function library
        :param function: any: function to add
        :param function_description: dict: description of the function
        :return: None
        """
        self.functions[function_description['name']] = function
        self.function_descriptions.append(function_description)
        return None

    def return_function(self, function_name: str) -> any:
        """
        method to return a function from the function library
        :param function_name: str: name of the function to return
        :return: any: function
        """
        return self.functions[function_name]
