from abc import ABC, abstractmethod
from typing import List

from schema import Quiz, Quizzes
from prompts import (
    HISTORY_SINGLE_QUIZ_PROMPT,
    HISTORY_MULTIPLE_QUIZZES_PROMPT,
    MATH_SINGLE_QUIZ_PROMPT,
    MATH_MULTIPLE_QUIZZES_PROMPT,
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai.chat_models import AzureChatOpenAI

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize AzureChatOpenAI with the specified configuration
azure_model = AzureChatOpenAI(
    openai_api_key=os.getenv('LLM_MODEL_API_KEY'),
    openai_api_version=os.getenv('LLM_MODEL_API_VERSION'),
    azure_endpoint=os.getenv('LLM_MODEL_ENDPOINT'),
    azure_deployment=os.getenv('LLM_MODEL_DEPLOYMENT'),
    validate_base_url=False,
)

class QuizGenerator(ABC):
    """
    A base class for quiz generators.

    This abstract class defines the interface for generating quizzes. 
    It contains common functionality and properties that all quiz generators must implement.
    """

    def __init__(self, llm_model: AzureChatOpenAI = azure_model):
        """
        Initializes the QuizGenerator with a language model.

        Args:
            llm_model (AzureChatOpenAI): An instance of the AzureChatOpenAI model.
        """
        self.azure_model = llm_model
        self.quiz_parser = JsonOutputParser(pydantic_object=Quiz)
        self.quizzes_parser = JsonOutputParser(pydantic_object=Quizzes)

    @abstractmethod
    def create_quiz(self):
        """
        Abstract method to create a single quiz.
        
        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def create_quizzes(self, num_quizzes: int):
        """
        Abstract method to create multiple quizzes.
        
        Args:
            num_quizzes (int): The number of quizzes to generate.
        
        This method must be implemented by subclasses.
        """
        pass

class HistoryQuizGenerator(QuizGenerator):
    """
    A quiz generator for creating history quizzes based on given content and keywords.
    """

    def create_quiz(self, content: str, keywords: List[str]) -> Quiz:
        """
        Create a single history quiz based on the provided content and keywords.

        Args:
            content (str): The content for the quiz.
            keywords (List[str]): A list of keywords related to the content.

        Returns:
            Quiz: The generated history quiz or an empty quiz object with an error message.
        """
        prompt_template = ChatPromptTemplate.from_template(
            HISTORY_SINGLE_QUIZ_PROMPT
        )
        chain = prompt_template | self.azure_model | self.quiz_parser
        
        try:
            response = chain.invoke({
                "content": content, 
                "keywords": keywords,
                "format_instructions": self.quiz_parser.get_format_instructions()
            })
            return response
        except Exception as e:
            print(f"Error generating history quiz: {e}")
            return Quiz(question="Error generating quiz", options=[])  # Return an empty Quiz object with an error message

    def create_quizzes(self, content: str, keywords: List[str], num_quizzes: int) -> Quizzes:
        """
        Create multiple history quizzes based on the provided content and keywords.

        Args:
            content (str): The content for the quizzes.
            keywords (List[str]): A list of keywords related to the content.
            num_quizzes (int): The number of quizzes to generate.

        Returns:
            Quizzes: The generated multiple history quizzes or an empty quizzes object with an error message.
        """
        prompt_template = ChatPromptTemplate.from_template(
            HISTORY_MULTIPLE_QUIZZES_PROMPT
        )
        chain = prompt_template | self.azure_model | self.quizzes_parser
        
        try:
            response = chain.invoke({
                "content": content, 
                "keywords": keywords, 
                "num_quizzes": num_quizzes,
                "format_instructions": self.quizzes_parser.get_format_instructions()
            })
            return response
        except Exception as e:
            print(f"Error generating multiple history quizzes: {e}")
            return Quizzes(quizzes=[Quiz(question="Error generating quiz", options=[])])  # Return an empty Quizzes object with an error message

class MathQuizGenerator(QuizGenerator):
    """
    A quiz generator for creating math word quizzes involving linear equations with two variables.
    """

    def create_quiz(self) -> Quiz:
        """
        Create a single math quiz.

        Returns:
            Quiz: The generated math quiz or an empty quiz object with an error message.
        """
        prompt_template = ChatPromptTemplate.from_template(
            MATH_SINGLE_QUIZ_PROMPT
        )
        chain = prompt_template | self.azure_model | self.quiz_parser
        
        try:
            response = chain.invoke({
                "format_instructions": self.quiz_parser.get_format_instructions()
            })
            return response
        except Exception as e:
            print(f"Error generating math quiz: {e}")
            return Quiz(question="Error generating quiz", options=[])  # Return an empty Quiz object with an error message

    def create_quizzes(self, num_quizzes: int) -> Quizzes:
        """
        Create multiple math quizzes.

        Args:
            num_quizzes (int): The number of quizzes to generate.

        Returns:
            Quizzes: The generated multiple math quizzes or an empty quizzes object with an error message.
        """
        prompt_template = ChatPromptTemplate.from_template(
            MATH_MULTIPLE_QUIZZES_PROMPT
        )
        chain = prompt_template | self.azure_model | self.quizzes_parser
        
        try:
            response = chain.invoke({
                "num_quizzes": num_quizzes,
                "format_instructions": self.quizzes_parser.get_format_instructions()
            })
            return response
        except Exception as e:
            print(f"Error generating multiple math quizzes: {e}")
            return Quizzes(quizzes=[Quiz(question="Error generating quiz", options=[])])  # Return an empty Quizzes object with an error message
