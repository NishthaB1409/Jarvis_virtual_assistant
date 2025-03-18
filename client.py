from openai import OpenAI
import os
# client = OpenAI()
# defaults to getting the key using os.environ.get("OPEN_API_KEY")
# if you saved the key under a different variable name, you can do something like:
client = OpenAI(
    api_key = "OPENAI_SECRET_KEY",
)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", "content": "You are a virtual assistant named jarvis, skilled in general tasks like alexa and google cloud"
        },
        {
            "role": "user",
            "content": "What is coding? "
        }
    ]
)

print(completion.choices[0].message.content)
    

