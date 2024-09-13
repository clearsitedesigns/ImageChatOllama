import streamlit as st
import requests
import json
import base64
from loguru import logger
import time
from PIL import Image
import io

class MemoryManager:
    def __init__(self, max_tokens=12000):
        self.memory = []
        self.max_tokens = max_tokens
        self.data_story = ""
        self.tagged_entries = {}

    def set_data_story(self, story: str):
        self.data_story = story
        self.add_to_memory(f"Initial Image Data Story: {story}")

    def add_to_memory(self, entry: str, tags=None):
        self.memory.append(entry)
        if tags:
            self.tagged_entries[len(self.memory) - 1] = tags

        while self.get_token_count() > self.max_tokens:
            if len(self.memory) > 1:
                self.memory.pop(1)
                if len(self.memory) - 1 in self.tagged_entries:
                    del self.tagged_entries[len(self.memory) - 1]
            else:
                break

    def get_token_count(self):
        return sum(len(entry.split()) for entry in self.memory)

    def get_memory(self):
        return "\n".join(self.memory)

def image_to_base64(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

def generate_response(prompt, image_base64_list=None):
    API_URL = "http://localhost:11434/api/generate"
    MODEL = "minicpm-v:latest"

    headers = {'Content-Type': 'application/json'}
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    if image_base64_list:
        data["images"] = image_base64_list

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed with status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Exception occurred while trying to get a response: {e}")
        return None

def main():
    st.set_page_config(page_title="Image Analysis and Chat", layout="wide")
    st.title("Image Analysis and Chat")

    # Custom CSS for styling
    st.markdown("""
        <style>
        .stImage {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
        }
        .chat-message.user {
            background-color: #2b313e;
        }
        .chat-message.bot {
            background-color: #475063;
        }
        .chat-message .avatar {
            width: 20%;
        }
        .chat-message .message {
            width: 80%;
            padding: 0 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    memory_manager = MemoryManager()
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'image_base64_list' not in st.session_state:
        st.session_state.image_base64_list = []

    # Sidebar for image upload
    with st.sidebar:
        st.header("Image Upload")
        uploaded_files = st.file_uploader("Choose images...", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        
        if uploaded_files:
            st.session_state.image_base64_list = [image_to_base64(file) for file in uploaded_files]
            st.success(f"{len(uploaded_files)} image(s) uploaded successfully!")

            # Display thumbnails of uploaded images
            for idx, file in enumerate(uploaded_files):
                img = Image.open(file)
                st.image(img, caption=f"Image {idx+1}", use_column_width=True, clamp=True)

        if st.session_state.image_base64_list and st.button("Analyze Images"):
            with st.spinner("Analyzing images..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                system_instruction = """
                Analyze the uploaded images and provide an overview of the content. 
                Ignore metadata and make sure the content is always in JSON format. 
                The JSON should include the following fields:
                {
                    "num_images": <number of images analyzed>,
                    "overall_description": <a brief overall description of all images>,
                    "images": [
                        {
                            "main_subject": <main subject of the image>,
                            "colors": <dominant colors in the image>,
                            "setting": <setting or background of the image>,
                            "notable_elements": <list of notable elements or objects in the image>
                        },
                        ...
                    ]
                }
                """
                response = generate_response(system_instruction, st.session_state.image_base64_list)
                if response:
                    image_overview = response.get("response", "No overview generated.")
                    memory_manager.set_data_story(image_overview)
                    st.session_state.image_analysis = json.loads(image_overview)
                else:
                    st.error("Failed to generate an image analysis.")

    # Main area with tabs for analysis and chat
    tab1, tab2 = st.tabs(["Image Analysis", "Chat"])
    
    with tab1:
        st.header("Image Analysis")
        if 'image_analysis' in st.session_state:
            st.json(st.session_state.image_analysis)
        else:
            st.info("No image analysis available. Please upload and analyze images using the sidebar.")

    with tab2:
        st.header("Chat")
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.conversation_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            memory_manager.add_to_memory(f"You: {user_input}")

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_input)

            prompt = f"User asked: {user_input}. Based on the uploaded images and the current conversation: {memory_manager.get_memory()}, provide a detailed response."

            with st.spinner("Generating response..."):
                response = generate_response(prompt, st.session_state.image_base64_list)
                
            if response:
                model_response = response.get("response", "No response from model.")
                memory_manager.add_to_memory(f"Model: {model_response}")
                st.session_state.conversation_history.append({"role": "assistant", "content": model_response})
                
                with chat_container:
                    with st.chat_message("assistant"):
                        st.markdown(model_response)
            else:
                st.error("Failed to get a response from the model.")

if __name__ == "__main__":
    main()