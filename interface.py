import gradio as gr
import requests
import json

API_BASE_URL = "http://localhost:8080"  # Ensure this port matches your FastAPI application

def generate_history_quizzes(test_cases):
    """
    Generate history quizzes based on the provided test cases.

    Args:
        test_cases (str): JSON formatted string containing history test cases.

    Returns:
        str: Formatted string of generated history quizzes or error message.
    """
    try:
        # Convert input JSON string to Python dictionary
        test_cases_json = json.loads(test_cases)

        # If the input is a single test case, convert it to a list
        if isinstance(test_cases_json, dict):
            test_cases_json = [test_cases_json]

    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please check your input."

    # Send request to generate history quizzes
    response = requests.post(
        f"{API_BASE_URL}/generate/history/",
        json={"cases": test_cases_json}
    )
    
    if response.status_code == 200:
        quizzes = response.json().get("quizzes", [])
        formatted_quizzes = ""
        for idx, quiz in enumerate(quizzes):
            formatted_quizzes += f"Quiz {idx + 1}: {quiz['question']}\n"
            for option in quiz['options']:
                correctness = "Correct" if option['isCorrect'] else "Incorrect"
                formatted_quizzes += f"- {option['content']} ({correctness}): {option['reason']}\n"
            formatted_quizzes += "\n"
        return formatted_quizzes
    else:
        return f"Error: {response.text}"

def generate_math_quiz(test_case):
    """
    Generate a math quiz based on the provided test case.

    Args:
        test_case (str): JSON formatted string containing a math test case.

    Returns:
        str: Formatted string of the generated math quiz or error message.
    """
    try:
        # Convert input JSON string to Python dictionary
        test_case_json = json.loads(test_case)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please check your input."

    # Send request to generate math quiz
    response = requests.post(
        f"{API_BASE_URL}/generate/math/",
        json=test_case_json
    )
    
    if response.status_code == 200:
        quiz = response.json().get("quiz", {})
        formatted_quiz = f"Quiz: {quiz['question']}\n"
        for option in quiz['options']:
            correctness = "Correct" if option['isCorrect'] else "Incorrect"
            formatted_quiz += f"- {option['content']} ({correctness}): {option['reason']}\n"
        return formatted_quiz
    else:
        return f"Error: {response.text}"

def generate_combined_quizzes(history_test_case, math_test_case, num_quizzes):
    """
    Generate combined history and math quizzes based on the provided test cases.

    Args:
        history_test_case (str): JSON formatted string containing history test case.
        math_test_case (str): JSON formatted string containing math test case.
        num_quizzes (int): Number of quizzes to generate.

    Returns:
        str: Formatted string of generated combined quizzes or error message.
    """
    try:
        # Convert input JSON strings to Python dictionaries
        history_test_case_json = json.loads(history_test_case)
        math_test_case_json = json.loads(math_test_case)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please check your input."

    # Send request to generate combined quizzes
    response = requests.post(
        f"{API_BASE_URL}/generate/quizzes/?num_quizzes={num_quizzes}",
        json={
            "history_test_case": history_test_case_json,
            "math_test_case": math_test_case_json
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        history_quizzes = data.get("history_quiz", [])
        math_quizzes = data.get("math_quiz", [])

        formatted_output = "History Quizzes:\n"
        for idx, quiz in enumerate(history_quizzes['quizzes']):
            formatted_output += f"Quiz {idx + 1}: {quiz['question']}\n"
            for option in quiz['options']:
                correctness = "Correct" if option['isCorrect'] else "Incorrect"
                formatted_output += f"- {option['content']} ({correctness}): {option['reason']}\n"
            formatted_output += "\n"

        formatted_output += "-" * 300 + "\n\n"  # Separator line

        formatted_output += "Math Quizzes:\n"
        for idx, quiz in enumerate(math_quizzes['quizzes']):
            formatted_output += f"Quiz {idx + 1}: {quiz['question']}\n"
            for option in quiz['options']:
                correctness = "Correct" if option['isCorrect'] else "Incorrect"
                formatted_output += f"- {option['content']} ({correctness}): {option['reason']}\n"
            formatted_output += "\n"

        return formatted_output
    else:
        return f"Error: {response.text}"

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Quiz Generation Interface")

    # Tab for History Quizzes
    with gr.Tab("History Quizzes"):
        history_input = gr.Textbox(
            label="Enter History Test Cases (JSON format)",
            placeholder='[{"content": "Reformation", "keywords": ["Martin Luther", "Roman Catholic Church"]}]'
        )
        history_output = gr.Textbox(label="Generated History Quizzes", interactive=False)
        gr.Button("Generate History Quizzes").click(
            generate_history_quizzes,
            inputs=history_input,
            outputs=history_output
        )

    # Tab for Math Quiz
    with gr.Tab("Math Quiz"):
        math_input = gr.Textbox(
            label="Enter Math Test Case (JSON format)",
            placeholder='{"content": "Solve x if x + 2 = 5"}'
        )
        math_output = gr.Textbox(label="Generated Math Quiz", interactive=False)
        gr.Button("Generate Math Quiz").click(
            generate_math_quiz,
            inputs=math_input,
            outputs=math_output
        )

    # Tab for Combined Quizzes
    with gr.Tab("Combined Quizzes"):
        combined_history_input = gr.Textbox(
            label="Enter History Test Case (JSON format)",
            placeholder='{"content": "Reformation", "keywords": ["Martin Luther", "Roman Catholic Church"]}'
        )
        combined_math_input = gr.Textbox(
            label="Enter Math Test Case (JSON format)",
            placeholder='{"content": "Solve x if x + 2 = 5"}'
        )
        num_quizzes_input = gr.Slider(
            label="Number of Quizzes",
            minimum=1,
            maximum=5,
            value=3,
            step=1
        )
        combined_output = gr.Textbox(label="Generated Combined Quizzes", interactive=False)
        gr.Button("Generate Combined Quizzes").click(
            generate_combined_quizzes,
            inputs=[combined_history_input, combined_math_input, num_quizzes_input],
            outputs=combined_output
        )

# Launch the Gradio interface with sharing option
demo.launch(share=True)
