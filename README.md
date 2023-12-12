# Jarvis Voice Assistant

Jarvis is a Python-based voice assistant that enables hands-free control of various tasks through voice commands. It features a web interface for status monitoring and interaction.

## Features

- **Voice Commands:** Control Jarvis using voice commands for tasks like sending WhatsApp messages, searching Wikipedia, playing videos on YouTube, providing weather updates, and more.
- **Web Interface:** Monitor Jarvis's status and system information through a web interface.
- **Flask Integration:** Use Flask for the web interface and communication with the voice assistant.
- **Selenium:** Automate browser actions for tasks like sending WhatsApp messages and searching Google.

## Prerequisites

- Python 3.x
- Pipenv (for managing Python virtual environment)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Jarvis-Voice-Assistant.git
    cd Jarvis-Voice-Assistant
    ```

2. Install dependencies using requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask application:

    ```bash
    python app.py
    ```

4. Open your browser and navigate to [http://localhost:5000](http://localhost:5000) to access the web interface.

## Usage

1. Ensure that the Flask application is running.
2. No need to run jarvis.py separately.
3. Jarvis will now respond to voice commands and perform various tasks.

## Supported Commands

- **Time:** Get the current time.
- **Date:** Get today's date.
- **WhatsApp:** Send a message to a contact on WhatsApp.
- **Wikipedia:** Search and retrieve information from Wikipedia.
- **Google:** Perform a Google search.
- **YouTube:** Play a video on YouTube.
- **Weather:** Get the current weather update for a specified location.
- **News:** Retrieve the latest news headlines.
- **Read:** Copy the current clipboard content and read it aloud.
- **Open:** Open a specified application.
- **Joke:** Listen to a random joke.
- **Screenshot:** Capture and save a screenshot.
- **Remember/Remind:** Store and retrieve reminders.
- **Password:** Generate a random password.
- **CPU:** Check CPU usage.
- **Battery:** Check battery status.
- **Shutdown/Restart:** Control system shutdown or restart.

## Contributing

Feel free to contribute by opening issues or pull requests. Follow the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines.

## Author

Hemant Raj
