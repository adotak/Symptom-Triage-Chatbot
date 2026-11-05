import asyncio

import gradio as gr
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

from triage_helpers import extract_message_parts, find_nearby_clinics

load_dotenv()

SYSTEM_PROMPT = """You are MediGuide, an AI-powered medical triage assistant designed for patients in Pakistan, particularly in underserved and rural areas with limited access to healthcare.

Your job is to:
1. Ask the user about their symptoms clearly and concisely.
2. Ask 1-2 follow-up questions if needed (age, duration of symptoms, severity).
3. Classify the situation into one of three categories:
   - 🔴 EMERGENCY – Go to the nearest hospital immediately.
   - 🟡 SEE A DOCTOR – Visit a clinic or GP within 24–48 hours.
   - 🟢 HOME CARE – Rest and basic remedies should help.
4. Give a brief, plain-language explanation of why you made that call.
5. If the situation is an EMERGENCY or SEE A DOCTOR, ask the user for their location (City/Area) and use the `find_nearby_clinics` tool to suggest real hospitals/clinics nearby.
6. Always recommend consulting a real doctor for any serious or unclear situation.

Rules:
- Keep responses short and easy to understand.
- Support multiple languages including English, Urdu, Pashto, Sindhi, Punjabi, and Balochi. Respond in whichever language the user writes in.
- Do not overreact to minor symptoms (like a mild headache or common cold), but be extremely cautious with red-flag symptoms (like chest pain, severe bleeding, or difficulty breathing).
- Never diagnose a specific disease. Only assess urgency.
- Never suggest specific medications or dosages.
- Always end your final triage with: *This is not a substitute for professional medical advice.*
"""

agent_instance = None
agent_init_lock = asyncio.Lock()


async def init_agent():
    """Initialize the shared agent once, even when requests arrive together."""
    global agent_instance
    if agent_instance is not None:
        return agent_instance

    async with agent_init_lock:
        if agent_instance is None:
            config = LocalAgentConfig(
                system_instructions=SYSTEM_PROMPT,
                tools=[find_nearby_clinics],
            )
            agent_instance = Agent(config)
            await agent_instance.__aenter__()

    return agent_instance


async def chat_fn(message, history):
    del history
    parts = extract_message_parts(message)
    if not parts:
        return "Please provide your symptoms as text or an audio recording."

    try:
        agent = await init_agent()
        response = await agent.chat(parts[0] if len(parts) == 1 else parts)
        return await response.text()
    except (OSError, RuntimeError, ValueError):
        print("MediGuide could not process a request.", flush=True)
        return (
            "MediGuide is temporarily unavailable. Please contact a healthcare "
            "professional or your nearest hospital directly."
        )


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🩺 MediGuide Triage Chatbot")
    gr.Markdown(
        "An AI-powered symptom triage assistant supporting multiple languages "
        "(English, Urdu, Pashto, Sindhi, Punjabi, Balochi)."
    )

    gr.ChatInterface(
        fn=chat_fn,
        multimodal=True,
        textbox=gr.MultimodalTextbox(show_label=False, file_types=["audio"]),
        title="MediGuide",
        description="Type your symptoms or use the microphone to record them.",
    )


if __name__ == "__main__":
    demo.launch()
