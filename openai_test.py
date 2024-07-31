#sk-proj-oJ90ayJJp94Y0mg7iSscT3BlbkFJVEL3hZ7kP6XeJvVstayT
import openai

openai.api_key = "sk-proj-SE0HLH27YshBsku7JhccT3BlbkFJRsPqjXMrnVHxt5YQndzd"

try:
    response = openai.Embedding.create(
        input="Hello, world",
        model="text-embedding-ada-002"
    )
    print("OpenAI API test successful")
    print(response)
except Exception as e:
    print(f"OpenAI API test failed: {e}")