import requests
import json
import base64
from loguru import logger
from tqdm import tqdm
import time

# MemoryManager class to manage context and conversation memory
class MemoryManager:
    def __init__(self, max_tokens=12000):
        """
        Initialize the MemoryManager with a maximum token limit.
        Args:
        max_tokens (int): Maximum number of tokens allowed in memory before older entries are removed.
        """
        self.memory = []  # List to store conversation history
        self.max_tokens = max_tokens  # Maximum token limit
        self.data_story = ""  # Narrative or story about the uploaded images
        self.tagged_entries = {}  # Dictionary to store tagged memory entries

    def set_data_story(self, story: str):
        """
        Set a data story related to the images or the conversation context.
        Args:
        story (str): The story or description about the image data.
        """
        self.data_story = story
        self.add_to_memory(f"Initial Image Data Story: {story}")  # Add the story to memory

    def add_to_memory(self, entry: str, tags=None):
        """
        Add new entries to the memory and manage the token count.
        Args:
        entry (str): The new conversation or context entry to add to memory.
        tags (optional): Tags to associate with the memory entry.
        """
        self.memory.append(entry)  # Add the new entry to memory
        if tags:
            # If there are tags, store them with the index of the memory entry
            self.tagged_entries[len(self.memory) - 1] = tags

        # Ensure the memory does not exceed the token limit
        while self.get_token_count() > self.max_tokens:
            # If memory exceeds the limit, remove the oldest entry (excluding the very first one)
            if len(self.memory) > 1:
                self.memory.pop(1)
                # Remove associated tags if present
                if len(self.memory) - 1 in self.tagged_entries:
                    del self.tagged_entries[len(self.memory) - 1]
            else:
                break

    def get_token_count(self):
        """
        Calculate the total token count for the memory.
        Returns:
        int: The total number of tokens in memory.
        """
        # Split entries into tokens (words) and sum their lengths
        return sum(len(entry.split()) for entry in self.memory)

    def get_memory(self):
        """
        Get the current memory as a single concatenated string.
        Returns:
        str: The concatenated memory entries.
        """
        return "\n".join(self.memory)  # Return the memory as a joined string

# Function to convert an image file to base64 encoding
def image_to_base64(image_path):
    """
    Convert an image to base64 encoding.
    Args:
    image_path (str): Path to the image file.
    Returns:
    str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        # Read and encode the image file in base64
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# Function to generate a response from the model, sending a prompt and optional image data
def generate_response(prompt, image_base64_list=None):
    """
    Generate a response from the model based on the prompt and images.
    Args:
    prompt (str): The text prompt for the model.
    image_base64_list (list): List of base64 encoded images to be analyzed.
    Returns:
    dict: The JSON response from the model.
    """
    API_URL = "http://localhost:11434/api/generate"  # Update with your API URL if necessary
    MODEL = "minicpm-v:latest"  # The specific model to use

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "model": MODEL,  # Specify the model
        "prompt": prompt,  # Provide the prompt
        "stream": False,  # Set to True if streaming responses are needed
        "format": "json"  # Request JSON format for the response
    }

    # If images are provided, include them in the request payload
    if image_base64_list:
        data["images"] = image_base64_list  # Include the base64 encoded images

    logger.info("Sending request to model for prompt evaluation.")
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        logger.info(f"Full model response: {response}")  # Log the full response for debugging
        if response.status_code == 200:
            return response.json()  # Return the response JSON if successful
        else:
            logger.error(f"Failed with status code {response.status_code}")
            return None
    except Exception as e:
        logger.exception(f"Exception occurred while trying to get a response: {e}")
        return None

# Main function to manage the conversation loop
def main():
    """
    Main function that manages user input, image uploading, and model interaction.
    It also tracks conversation history using the MemoryManager.
    """
    logger.add("chatbot_log.log", rotation="1 MB")  # Log rotation with Loguru

    print("Welcome to the chat! Type 'exit' to end the conversation.")

    # Initialize the memory manager
    memory_manager = MemoryManager()
    image_base64_list = []  # List to hold base64 encoded images
    conversation_history = []  # List to track the conversation history

    # Ask the user if they want to upload images
    image_input = input("Do you want to upload images for the conversation? (y/n): ")
    if image_input.lower() == 'y':
        # Allow multiple images to be uploaded
        while True:
            image_path = input("Enter the path to your image (or type 'done' to finish): ")
            if image_path.lower() == 'done':
                break
            try:
                # Convert the image to base64 and add it to the list
                image_base64 = image_to_base64(image_path)
                image_base64_list.append(image_base64)
                logger.info(f"Image uploaded successfully: {image_path}")
                print("Image uploaded successfully!")
            except Exception as e:
                logger.error(f"Failed to upload image: {e}")
                print(f"Failed to upload image: {e}")

    # Automatically generate an initial overview if images were uploaded
    if image_base64_list:
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
        print("\nAnalyzing uploaded images...")
        for _ in tqdm(range(100), desc="Processing images..."):
            time.sleep(0.02)

        response = generate_response(system_instruction, image_base64_list)
        if response:
            image_overview = response.get("response", "No overview generated.")
            print("\n[Initial Image Analysis]")
            print(f"  {image_overview}\n")
            logger.info(f"Initial image analysis: {image_overview}")
            memory_manager.set_data_story(image_overview)  # Store the overview as the initial story
        else:
            print("[Error] Failed to generate an image analysis.")
            return

    # Main chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            logger.info("Conversation ended by the user.")
            print("Goodbye!")
            break

        # Add the user's input to memory
        memory_manager.add_to_memory(f"You: {user_input}")
        conversation_history.append({"role": "user", "content": user_input})  # Track conversation

        # Generate the prompt from the current memory and the user input, and include image references
        prompt = f"User asked: {user_input}. Based on the uploaded images and the current conversation: {memory_manager.get_memory()}, provide a detailed response."

        # Progress bar to simulate evaluation progress
        for _ in tqdm(range(100), desc="Evaluating prompt..."):
            time.sleep(0.02)  # Simulating some delay for the progress bar

        # Generate the response from the model using the current prompt and any uploaded images
        response = generate_response(prompt, image_base64_list)
        if response:
            model_response = response.get("response", "No response from model.")
            if not model_response:
                logger.warning("Received empty response from the model.")
            memory_manager.add_to_memory(f"Model: {model_response}")  # Add model response to memory
            conversation_history.append({"role": "model", "content": model_response})
            print(f"Model: {model_response}")
            logger.info(f"Model response: {model_response}")
        else:
            print("Failed to get a response from the model.")
            logger.warning("Model failed to generate a response.")

    # Print the conversation history in a formatted JSON structure
    print(json.dumps(conversation_history, indent=2))
    logger.info("Conversation history logged.")

if __name__ == "__main__":
    main()