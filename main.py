from quiz_generator import HistoryQuizGenerator, MathQuizGenerator
from schema import Quiz, Quizzes
import nest_asyncio
import asyncio
from time import time

nest_asyncio.apply()

# Sample history test cases
history_test_case_1 = {
    "content": "Reformation",
    "keywords": ["Martin Luther", "Roman Catholic Church"],
}

history_test_case_2 = {
    "content": "World War II",
    "keywords": ["J. Robert Oppenheimer"]
}

history_test_case_3 = {
    "content": "Civil War",
    "keywords": ["slavery"]
}

# Sample math test case
math_test_case_1 = {}


async def history_question(history_test_case: dict) -> Quiz:
    """
    Generate history quizzes based on provided test cases asynchronously.

    Args:
        history_test_case (dict): A dictionary containing the test cases for history quizzes.

    Returns:
        Quiz: A list of generated history quizzes.
    """
    # Create asynchronous tasks for generating history quizzes and wait for all tasks to complete
    history_tasks = [
        asyncio.to_thread(HistoryQuizGenerator().create_quiz, **test_case)
        for test_case in history_test_case
    ]

    # Wait for all history quiz generation tasks to complete
    history_quizzes = await asyncio.gather(*history_tasks)

    # Print the generated quiz results
    # for quiz_result in quizzes:
    #     print(f"\n\nQuiz: {quiz_result}\n\n")
        
    return history_quizzes

def math_question(math_test_case: dict) -> Quiz:
    """
    Generate a math quiz based on the provided test case.

    Args:
        math_test_case (dict): A dictionary containing the test case for the math quiz.

    Returns:
        Quiz: The generated math quiz.
    """
    math_quiz = MathQuizGenerator().create_quiz(**math_test_case)
    # print(f"\n\nQuiz: {quiz_result}\n\n")
    
    return math_quiz

async def generate_quizzes(history_test_case: dict, math_test_case: dict, num_quizzes: int): 
    """
    Generate both history and math quizzes asynchronously based on provided test cases.

    Args:
        history_test_case (dict): A dictionary containing the test cases for history quiz.
        math_test_case (dict): A dictionary containing the test case for the math quiz.
        num_quizzes (int): The number of quizzes to generate for both subjects.

    Returns:
        Tuple[Quiz, Quiz]: A tuple containing the generated history and math quizzes.
    """
    kwargs = {"num_quizzes": num_quizzes}
    
    # Create asynchronous tasks for generating history and math quizzes
    history_task = asyncio.to_thread(
        HistoryQuizGenerator().create_quizzes,
        **{**history_test_case, **kwargs}
    )
    
    math_task = asyncio.to_thread(
        MathQuizGenerator().create_quizzes,
        **{**math_test_case, **kwargs}
    )
    
    # Wait for all quiz generation tasks to complete
    history_quiz_result, math_quiz_result = await asyncio.gather(history_task, math_task)
    
    # Print the generated quiz results
    print(f"\n\nHistory Quiz: {history_quiz_result}\n\n")
    print(f"\n\nMath Quiz: {math_quiz_result}\n\n")

    return history_quiz_result, math_quiz_result 

if __name__ == "__main__":
    async def main():
        """
        Main asynchronous function to run quiz generation tests.

        This function measures the execution time of the quiz generation processes.
        """
        start_time = time()

        try:
            # Example calls 
            
            # 1. Generate history quizzes
            history_test_cases = [
                history_test_case_1,
                history_test_case_2,
                history_test_case_3,
            ]
            await history_question(history_test_cases)
            
            # 2. Generate a math quiz
            math_question(math_test_case_1)
            
            # 3. Generate both history and math quizzes (Bonus)
            # await generate_quizzes(history_test_case_1, math_test_case_1, 3)

        except Exception as e:
            print(f"Error in main execution: {e}")

        end_time = time()

        # Calculate and print the total elapsed time
        elapsed_time = end_time - start_time
        print(f"Total execution time: {elapsed_time:.2f} seconds")

    asyncio.run(main())  # Run the main asynchronous function
