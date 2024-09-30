# Quiz Generator - LLM-based History and Math Quiz Generation

This project is designed to generate history and math quizzes using a Large Language Model (LLM) via **AzureChatOpenAI** and LangChain. The system is flexible and modular, allowing easy customization of prompts, quiz generation logic, and interaction through an API and a Gradio interface.

## Project Structure

- **quiz_generator.py**  
  This file constructs the `QuizGenerator` and `HistoryQuizGenerator` using AzureChatOpenAI with LangChain. It contains the core logic for generating quizzes based on prompts and models.

- **main.py**  
  Demonstrates the use of the system with three test cases:
  1. `history_question` - Generates a history quiz.
  2. `math_question` - Generates a math quiz.
  3. `generate_quizzes` - Handles the generation of multiple quizzes on history and math questions.

- **prompts/**  
  Contains the prompt templates used for quiz generation. These are customizable and can be modified easily to adjust quiz formats or add new types of quizzes.

- **schema.py**  
  Defines the expected response schema for the LLM-generated quizzes. This ensures that the model output matches the required format.

- **app.py**  
  Uses FastAPI to create a backend API. You can test the quiz generation system through the Swagger UI provided by FastAPI for easy interaction and debugging.

- **models/**  
  Contains data models for the API, ensuring proper request and response formatting.

- **interface.py**  d
  Implements a simple interactive platform using Gradio, allowing users to generate quizzes through a user-friendly web interface.

- **requirements.txt**  
  Lists the dependencies required to run the project. Ensure that you have all necessary packages installed.

- **.env**  
  This file is required to store your Azure OpenAI API keys and other relevant configuration information, which you need to set up manually.

## Setup Instructions

Follow the steps below to set up the project:

### Step 1: Create a virtual environment and install Python 3.11
First, make sure you have Python 3.11 installed on your system. Then create a virtual environment:

```bash
mkvirtualenv -p python3.11 test_quiz_generator
```

### Step 2: Install dependencies
Install the required packages listed in requirements.txt:

```bash
pip install -r requirements.txt
```

### Step 3: Set up .env file
Create a .env file in the root directory of your project and add your Azure OpenAI API keys and other necessary configurations.

### Step 4: Run the FastAPI server
Create a .env file in the root directory of your project and add your Azure OpenAI API keys and other necessary configurations.
You can now access the FastAPI Swagger UI at http://localhost:8080/docs to interact with the API.

```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

### Step 5: Run the Gradio interface
To launch the Gradio interface for generating quizzes.
This will launch a Gradio web interface, allowing you to interact with the quiz generator through a user-friendly UI.

```bash
python interface.py
```
