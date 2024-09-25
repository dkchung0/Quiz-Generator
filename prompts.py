HISTORY_SINGLE_QUIZ_PROMPT = """
You are an expert in history education. Based on the following content: "{content}" 
and the keywords: {keywords}, generate a single history quiz question. 
Ensure that the question has a clear difficulty level, which can be either easy, medium, or hard.
Provide four options for the answer, ensuring that the correct answer is not always the first option. 
Each option should include a reason for why it's correct or incorrect. 
Label the difficulty level of the quiz question in the response.
The response should be in the following JSON format:
{format_instructions}
"""

HISTORY_MULTIPLE_QUIZZES_PROMPT = HISTORY_SINGLE_QUIZ_PROMPT.replace(
    "generate a single history quiz question",
    "generate {num_quizzes} different history quiz questions, each with a different difficulty level (easy, medium, hard)."
)

MATH_SINGLE_QUIZ_PROMPT = """
You are an expert in mathematics education. Generate a math word problem that involves a real-life situation 
requiring solving for two variables in a system of linear equations.

1. The problem can involve solving for one variable when another variable is given (e.g., x + 2y = 10, where y = 3). 
   Ensure to provide similar examples in your problem statement.
2. Ensure that the problem is logically sound and does not contain negative numbers.
3. Provide four options for the solution, ensuring that there is always one correct answer, which is not necessarily the first option.
4. Each option should include a detailed explanation. For incorrect options, provide the specific incorrect calculation steps (e.g., "x = 10 - 2*3 = 5", but this ignores the sign change) and explain why these lead to the wrong result. For the correct option, show the correct steps and the reasoning behind the correct answer.
5. When generating multiple problems, ensure there is a differentiation in difficulty levels and introduce variety in the problems.

The response should be in the following JSON format:
{format_instructions}
"""

MATH_MULTIPLE_QUIZZES_PROMPT = MATH_SINGLE_QUIZ_PROMPT.replace(
    "Generate a math word problem",
    "Generate {num_quizzes} different math word problems. These problems must incorporate varying levels of complexity and **must not** include any indication of difficulty level while ensuring logical consistency without negative numbers."
)