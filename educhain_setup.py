from educhain import Educhain, LLMConfig
from langchain_openai import ChatOpenAI
import os

# Set the OPENAI_API_KEY to the OpenRouter key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize ChatOpenAI with OpenRouter base URL and model
deepseek_model = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324:free",
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1
)

# Configure Educhain to use the custom DeepSeek model
deepseek_config = LLMConfig(custom_model=deepseek_model)
client = Educhain(deepseek_config)

# Task 1: Generate Multiple Choice Questions (MCQs)
print("Generating 5 MCQs on Python Programming Basics...")
mcq_questions = client.qna_engine.generate_questions(
    topic="Python Programming Basics",
    num=5,
    question_type="Multiple Choice"
)

print("MCQs generated:")
print(mcq_questions.model_dump_json(indent=2))

# Save MCQs to a JSON file
with open("python_mcqs.json", "w") as f:
    f.write(mcq_questions.model_dump_json(indent=2))
print("MCQs saved to python_mcqs.json")

# Task 2: Generate a Lesson Plan
print("\nGenerating a lesson plan for Python Programming Basics...")
lesson_plan = client.content_engine.generate_lesson_plan(
    topic="Python Programming Basics",
    duration="60 minutes",
    grade_level="Beginner",
    learning_objectives=["Understand basic Python syntax", "Learn about variables and data types", "Introduction to control flow"]
)

print("Lesson plan generated:")
print(lesson_plan.model_dump_json(indent=2))

# Save lesson plan to a JSON file
with open("python_lesson_plan.json", "w") as f:
    f.write(lesson_plan.model_dump_json(indent=2))
print("Lesson plan saved to python_lesson_plan.json")


