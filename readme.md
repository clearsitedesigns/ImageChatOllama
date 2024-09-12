Image Conversational Chatbot with Memory Management and Confidence Metrics
=====================================================================

I expect there to be bugs, but I think you will quickly see how you can use this in a number of situations.
I provided use cases below to help you explore more and research. 
I expect there to be some hallucinations
The code has more comments then I like, but you wont get lost.
This is by no means perfect!
I love the fact that vision models can run locally now and with decent inference! I run on an Mac 1 with ollama and 64 Ram.
I've loved using MinCPM model in the past, and now its great to have it in ollama.

This project is a Python-based chatbot that allows users to converse with a model using both text prompts and images. The chatbot utilizes a memory management system to track the conversation context over time and ensures that the memory stays within a specified token limit for effective conversation flow. The system now also includes confidence metrics for model responses.

The Script Integrates with Ollama
--------------------------------

The script integrates with Ollama, a local model running on your system, to handle both text and image-based conversational prompts. You can download Ollama from <https://ollama.com/>, and the chatbot script will interact with the Ollama API for generating responses based on the input.

Features
--------

### Multi-image understanding

*   Upload and converse about multiple images in a single conversation.
*   The chatbot automatically analyzes the uploaded images and provides an initial overview.
*   You can continously chat with the image the memory manager will try to keep track of the flow
*   You can ask detailed questions about text what's in it and more. 


### Memory management

*   The `MemoryManager` class tracks conversation context, maintaining a dynamic conversation flow while ensuring the conversation stays within a defined token limit.
*   Older entries are removed when the token limit is reached, allowing long conversations without overwhelming the model.

### Context preservation

*   The memory is used to maintain context, enabling richer, multi-turn conversations.
*   The chatbot remembers past interactions and incorporates them into future responses.

### - NOT YET IN PLACE - Confidence metrics

*   Each response from the model includes a confidence score, providing additional context about the reliability of the answer.
*   Confidence scores help users gauge the model’s certainty in its analysis and responses.
*   Working on this

Prerequisites
--------------

### Python

*   Python 3.10 or higher

### Ollama

*   You need to have Ollama running locally. Download and install Ollama from <https://ollama.com/>.
*   http://ollama.com

### Conda

*   (Optional but recommended) For managing your Python environment.

Setup Instructions
------------------

### Step 1: Set Up Ollama and Pull the Model

#### Install Ollama:

*   Download and install Ollama from here.
*   Pull the `minicpm-v` model, a vision-language model used in this project.
    *   Run the following command in your terminal to pull the model:
        ```bash
ollama run minicpm-v
```
    This model is a multimodal LLM for vision-language understanding. Ensure you have enough disk space as the model is approximately 5.5GB in size.

### Step 2: Set Up a Conda Environment

#### Install Conda:

*   If you don't already have Conda installed, you can install Miniconda or Anaconda.
    *   Follow these steps to set up the environment:
        ```bash
conda create --name chatbot-env python=3.10
```
This will create a Conda environment named `chatbot-env` with Python 3.10.

#### Activate the Conda Environment:

*   Run the following command in your terminal to activate the environment:
    ```bash
conda activate chatbot-env
```
Your terminal should now reflect that you are working within the `chatbot-env` environment.

### Step 3: Install the Dependencies

With the Conda environment active, install the required Python packages by running:

```bash
pip install -r requirements.txt
```

This will install the following dependencies:

*   `requests`: To handle HTTP requests to the Ollama API.
*   `loguru`: For logging conversation history and debugging.
*   `tqdm`: To provide progress bars for model evaluation and image processing.

### Step 4: Run the Script

Ensure that Ollama is running on your system. You can check this by visiting <https://ollama.com/> and setting it up.

Run the chatbot script:

```bash
python image-chat-ollama.py
```

This will start the chatbot, allowing you to upload images, ask questions, and have a conversation with the model.
You will want to past the full path to your image on your system.
You can upload multiple images as well. 


### Step 5: Interact with the Chatbot

When prompted, you can upload multiple images by providing their file paths.
Ask the chatbot questions related to the images or any other text-based prompt.
The chatbot will generate responses based on the images and the conversation context, managed by the `MemoryManager`. Each response will include a confidence score to give you insights into the model’s certainty.
Type 'exit' at any time to end the conversation.

## Use Case Potentials
With a little bit of work you can make this do some pretty cool things.
These are just some quick AI potentials, they haven't been tested. Something to inspire you.

### 1. **Educational Assistant**


*   **Scenario:** A teacher uploads images of diagrams or educational materials and uses the chatbot as a teaching tool to help students learn complex concepts through interactive visual explanations.
*   **Example:**
    *   Teacher: "Here is an image of the water cycle. Can you explain each stage?"
    *   Chatbot: "This image depicts the water cycle. The stages include evaporation, condensation, precipitation, and collection. Evaporation happens when..."
*   **Features used:** Multi-image understanding, memory management, context preservation


### 2. **Medical Imaging Analysis**


*   **Scenario:** A doctor uploads medical images (e.g., X-rays or MRIs) to analyze the patient's condition and get insights from the chatbot.
*   **Example:**
    *   Doctor: "I've uploaded an X-ray of a hand. Can you point out signs of a fracture?"
    *   Chatbot: "This X-ray shows a potential fracture near the second metacarpal..."
*   **Features used:** Multi-image understanding, memory management, confidence metrics


### 3. **Travel and Leisure**


*   **Scenario:** A traveler uploads images of landmarks to get information, fun facts, and historical context about the location from the chatbot.
*   **Example:**
    *   Traveler: "Here's a picture from the Eiffel Tower. Can you tell me its history?"
    *   Chatbot: "The Eiffel Tower, built in 1889 for the World's Fair, stands at 324 meters tall..."
*   **Features used:** Multi-image understanding, memory management, context preservation
