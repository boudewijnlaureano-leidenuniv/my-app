from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
import sys

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Set API key for OpenAI
OpenAI.api_key = API_KEY

client=OpenAI()

assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4o",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

if run.status == 'completed': 
  # Retrieve all messages in the thread and convert to a list
  messages = list(client.beta.threads.messages.list(thread_id=thread.id))

  # Collect and reverse the messages for correct order display
  formatted_messages = []
  for msg in reversed(messages):  # Reverse order here
      role = msg.role.capitalize()  # Capitalize the role (User or Assistant)
      content = msg.content[0].text.value if msg.content and msg.content[0].type == 'text' else ''
      formatted_messages.append(f"{role}:\n{content}\n")
  
  # Display all messages in the correct order
  for formatted_message in formatted_messages:
      print(formatted_message)

else:
  print("Run status:", run.status)
