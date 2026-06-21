import asyncio
import os
import gradio as gr
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

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

def find_nearby_clinics(location: str) -> str:
    """Finds nearby hospitals or clinics based on a user's location in Pakistan."""
    city = location.lower()
    
    # Mock database of major hospitals in key Pakistani cities
    hospitals = {
        "karachi": "1. Aga Khan University Hospital\n2. Liaquat National Hospital\n3. Jinnah Postgraduate Medical Centre (JPMC)",
        "lahore": "1. Shaukat Khanum Memorial Cancer Hospital\n2. Mayo Hospital\n3. Doctors Hospital & Medical Center",
        "islamabad": "1. Shifa International Hospital\n2. Pakistan Institute of Medical Sciences (PIMS)\n3. Quaid-e-Azam International Hospital",
        "peshawar": "1. Lady Reading Hospital\n2. Khyber Teaching Hospital\n3. Hayatabad Medical Complex",
        "quetta": "1. Bolan Medical Complex Hospital\n2. Civil Hospital Quetta\n3. Akram Hospital"
    }
    
    for key, value in hospitals.items():
        if key in city:
            return f"Here are some major hospitals in {key.capitalize()}:\n{value}"
            
    return f"I couldn't find specific hospitals in my database for '{location}'. However, please search Google Maps for 'hospitals near me' or proceed to your nearest district hospital."

# Global agent for local testing
agent_instance = None

async def init_agent():
    global agent_instance
    if agent_instance is None:
        config = LocalAgentConfig(
            system_instructions=SYSTEM_PROMPT,
            tools=[find_nearby_clinics]
        )
        agent_instance = Agent(config)
        await agent_instance.__aenter__()

async def chat_fn(message, history):
    await init_agent()
    
    text_input = ""
    file_inputs = []
    
    if isinstance(message, dict):
        text_input = message.get("text", "")
        file_inputs = message.get("files", [])
    else:
        text_input = message
        
    # Combine content for the agent
    content = []
    if text_input:
        content.append(text_input)
    for f in file_inputs:
        content.append(f)
        
    if not content:
        return "Please provide some text or audio input."
        
    if len(content) == 1:
        content = content[0]
        
    response = await agent_instance.chat(content)
    return await response.text()

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🩺 MediGuide Triage Chatbot")
    gr.Markdown("An AI-powered symptom triage assistant supporting multiple languages (English, Urdu, Pashto, Sindhi, Punjabi, Balochi).")
    
    gr.ChatInterface(
        fn=chat_fn,
        multimodal=True,
        textbox=gr.MultimodalTextbox(show_label=False, file_types=["audio"]),
        title="MediGuide",
        description="Type your symptoms or use the microphone to record them."
    )

if __name__ == "__main__":
    demo.launch()
