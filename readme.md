Here is your text rewritten as Markdown:

# Image Conversational Chatbot with Memory Management and Confidence Metrics
## Overview
This project is a Python-based chatbot that enables users to engage in conversations using both text prompts and images. The chatbot integrates with Ollama, a local model running on your system, to handle multimodal inputs. It features a memory management system to track conversation context over time, ensuring effective conversation flow within a specified token limit. The system is also being developed to include confidence metrics for model responses.

## Table of Contents

### Features
- Multi-Image Understanding
- Memory Management
- Context Preservation
- Confidence Metrics (Under Development)

### Prerequisites
- Python
  - Version: Python 3.10 or higher is required.
- Ollama
  - Installation: Download and install Ollama from ollama.com.
  - Model: Ensure you have the minicpm-v model installed. This is a vision-language model approximately 5.5 GB in size.
- Conda (Optional)
  - Purpose: Recommended for managing your Python environment.
  - Installation: Install Miniconda or Anaconda.

### Setup Instructions
#### Step 1: Install Ollama and Pull the Model
1. **Install Ollama**
   - Download and install: Visit ollama.com to download and install Ollama.
2. **Pull the minicpm-v Model**
   - Command: Open your terminal and run the following command to pull the model:

```bash
ollama run minicpm-v
```
   - Note: Ensure you have sufficient disk space (approximately 5.5 GB).

#### Step 2: Set Up a Conda Environment
1. **Install Conda**
   - Download: If you don't have Conda, install Miniconda or Anaconda.
2. **Create a New Environment**
   - Command: Run the following to create a new Conda environment named `chatbot-env` with Python 3.10:

```bash
conda create --name chatbot-env python=3.10
```
3. **Activate the Environment**
   - Command: Activate the environment using:

```bash
conda activate chatbot-env
```

#### Step 3: Install the Dependencies
1. **Install Packages**: With the Conda environment active, install the required Python packages:

```bash
pip install -r requirements.txt
```
2. **Dependencies**:
   - `requests`: For handling HTTP requests to the Ollama API.
   - `loguru`: For logging conversation history and debugging.
   - `tqdm`: For progress bars during model evaluation and image processing.

#### Step 4: Run the Chatbot Script
1. **Ensure Ollama is Running**: Confirm that Ollama is running on your system.
2. **Run the Script**: Execute the chatbot script:

```bash
python image-chat-ollama.py
```
   - Note: When prompted, provide the full path to your image files. You can upload multiple images.

#### Step 5: Interact with the Chatbot
1. **Upload Images**: When prompted, upload images by providing their file paths.
2. **Ask Questions**: Engage with the chatbot by asking questions related to the images or any text-based prompts.
3. **Conversation Flow**: The MemoryManager will manage the conversation context, enabling dynamic and context-aware interactions.
4. **Exit**: Type `exit` at any time to end the conversation.

## Use Case Potentials
Explore various applications of this chatbot to inspire your own projects. Below are some potential use cases:

### 1. Educational Assistant
Scenario: A teacher uploads images of diagrams or educational materials to help students learn complex concepts through interactive explanations.
Example:
Teacher: "Here is an image of the water cycle. Can you explain each stage?"
Chatbot: "This image depicts the water cycle, including evaporation, condensation, precipitation, and collection..."
Features Used: Multi-image understanding, memory management, context preservation.

### 2. Medical Imaging Analysis
Scenario: A doctor uploads medical images (e.g., X-rays or MRIs) to analyze a patient's condition and receive insights.
Example:
Doctor: "I've uploaded an X-ray of a hand. Can you identify any signs of a fracture?"
Chatbot: "The X-ray shows a potential fracture near the second metacarpal bone..."
Features Used: Multi-image understanding, memory management, confidence metrics.

### 3. Travel and Leisure
Scenario: A traveler uploads images of landmarks to get information, fun facts, and historical context.
Example:
Traveler: "Here's a picture from the Eiffel Tower. Can you tell me its history?"
Chatbot: "The Eiffel Tower, constructed in 1889 for the World's Fair, stands at 324 meters tall..."
Features Used: Multi-image understanding, memory management, context preservation.

## Notes
- **Expectations**: While the chatbot is functional, it may contain bugs and occasional hallucinations. The code includes extensive comments to assist with understanding and troubleshooting.
- **Performance**: The chatbot runs efficiently on systems with sufficient resources. Tested on a Mac with Apple Silicon and 64 GB RAM.
- **Vision Models**: The integration of vision models like minicpm-v into Ollama allows for local execution with decent inference times.
- **Contributions**: Contributions and improvements are welcome. Feel free to explore and expand upon the use cases provided.
