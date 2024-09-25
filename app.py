from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from main import history_question, math_question, generate_quizzes
from models import HistoryTestCases, HistoryTestCase, MathTestCase

app = FastAPI(
    title="Quiz Generation API",
    description="An API for generating history and math quizzes based on provided test cases.",
    version="1.0.0",
)

async def handle_request(func, *args, **kwargs):
    """
    Handle requests and catch exceptions.

    Returns:
        The result of the function if successful, otherwise raises an HTTPException with status code 500.
    """
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/history/", response_model=dict, 
          description="Generate history quizzes based on provided test cases.")
async def generate_history_quizzes(test_cases: HistoryTestCases):
    """
    Generate history quizzes based on provided test cases.

    Args:
        test_cases (HistoryTestCases): A collection of history test cases.

    Returns:
        JSONResponse: A response containing the generated history quizzes.
    """
    history_test_cases = [test_case.dict() for test_case in test_cases.cases]
    quizzes = await handle_request(history_question, history_test_cases)
    return JSONResponse(content={"quizzes": quizzes})

@app.post("/generate/math/", response_model=dict, 
          description="Generate a math quiz based on the provided test case.")
def generate_math_quiz(test_case: MathTestCase):
    """
    Generate a math quiz based on the provided test case.

    Args:
        test_case (MathTestCase): A single math test case.

    Returns:
        JSONResponse: A response containing the generated math quiz.
    """
    try:
        quiz_result = math_question(test_case.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return JSONResponse(content={"quiz": quiz_result})

@app.post("/generate/quizzes/", response_model=dict, 
          description="Generate both history and math quizzes based on the provided test cases.")
async def generate_quizzes_endpoint(
    history_test_case: HistoryTestCase, 
    math_test_case: MathTestCase, 
    num_quizzes: int = 3
):
    """
    Generate both history and math quizzes based on the provided test cases.

    Args:
        history_test_case (HistoryTestCase): The test case for the history quiz.
        math_test_case (MathTestCase): The test case for the math quiz.
        num_quizzes (int): The number of quizzes to generate for each subject (default is 3).

    Returns:
        JSONResponse: A response containing the generated history and math quizzes.
    """
    history_quiz_result, math_quiz_result = await handle_request(
        generate_quizzes,
        history_test_case.dict(),
        math_test_case.dict(),
        num_quizzes
    )
    return JSONResponse(content={
        "history_quiz": history_quiz_result,
        "math_quiz": math_quiz_result
    })
