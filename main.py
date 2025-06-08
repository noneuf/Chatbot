import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import gradio.themes as themes


# =========================
# 🔧 Configuration
# =========================

# Load environment variables
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
PROFILE_PATH = "/etc/secrets/user_profile.txt"

# =========================
# 📄 Load User Profile
# =========================

def load_user_profile(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

USER_PROFILE = load_user_profile(PROFILE_PATH)

# =========================
# 🧠 Compose System Message
# =========================

BASE_SYSTEM_MESSAGE = USER_PROFILE + "\n\n" + (
    "You are a helpful assistant. In addition to answering questions, you can help others understand the user’s work, "
    "reflect on their projects, answer technical questions, and describe their experience. "
    "Always refer to the user in the third person. Be professional, clear, and helpful in your answers."
    "For antying related to the user, use the information provided in the user profile and if you don't know the answer, respond with 'I don't know' or 'I am not sure'. "
)

# =========================
# 🤖 OpenAI Client Setup
# =========================

openai = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# 💬 Chat Function
# =========================

def chat_function(message, history):
    system_message = BASE_SYSTEM_MESSAGE

    messages = [{"role": "system", "content": system_message}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response


# =========================
# 🖥️ Launch Gradio UI
# =========================

my_theme = themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
    radius_size="lg",
    font=["Inter", "sans-serif"]
)

gr.ChatInterface(
    fn=chat_function,
    title="🤖 Personal Assistant",
    description="Ask anything about Nathan's assistant.",
    theme=my_theme,
    type="messages"
).launch(server_name="0.0.0.0", server_port=8080)
