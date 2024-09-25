from pydantic import BaseModel, Field
from typing import List


class Option(BaseModel):
    content: str = Field(..., description="The content of the option.")
    reason: str = Field(
        description="A complete, concise and meaningful reason why the option is correct or incorrect."
    )
    isCorrect: bool = Field(
        ..., description="Indicate whether the option is 'Correct' or 'Incorrect'."
    )


class Quiz(BaseModel):
    question: str = Field(..., description="The content of the question.")
    options: List[Option] = Field(..., description="Four options of the question.")


class Quizzes(BaseModel):
    quizzes: List[Quiz] = Field(..., description="A List of questions.")
