import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI
openai = OpenAI(api_key=openai_api_key)
MODEL = 'gpt-4o-mini'

# System prompt
base_system_message = (
    "You are a helpful assistant in a clothes store. You should try to gently encourage "
    "the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. "
    "If the customer asks for shoes, say they are not on sale, but remind them about hats!"
)

def chat_function(message, history):
    system_message = base_system_message
    if "belt" in message.lower():
        system_message += " We don't sell belts. Recommend other sale items like hats."

    messages = [{"role": "system", "content": system_message}]
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    messages.append({"role": "user", "content": message})

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response

# Create a clean-looking Chat Interface
chat_ui = gr.ChatInterface(
    fn=chat_function,
    title="🛍️ Clothes Store Assistant",
    description="Ask me about items in the store. Hats are on sale! 🎩",
    theme="soft",  # Optional: nice color theme
    retry_btn="🔁 Try again",
    undo_btn="↩️ Undo last",
    clear_btn="🧹 Clear chat"
)

chat_ui.launch()
