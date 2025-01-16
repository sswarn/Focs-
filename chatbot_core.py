import json
import random
from tkinter import messagebox


def get_random_agent_name(file_name):
    """Load agent names from a file and return a random one."""
    try:
        with open(file_name, "r") as file:
            names = [line.strip() for line in file.readlines()]
        return random.choice(names)
    except FileNotFoundError:
        return "Agent"  # Default name if file is missing


def load_responses(file_name):
    """Load responses from a JSON file."""
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Response configuration file not found!")
        return {}


def detect_keywords(user_input, user_name, responses):
    """Detect keywords and return an appropriate response."""
    for keyword, response in responses.items():
        if keyword in user_input:
            return response.replace("{user_name}", user_name)  # Personalize response

    # Default random response
    random_responses = [
        "That's an interesting question!",
        "Let me think about that for a moment.",
        f"Can you elaborate on that, {user_name}?",
        "I'm not sure I understand, but I'd love to help!"
    ]
    return random.choice(random_responses)


def log_session(user_input, response):
    """Log the session to a file."""
    with open("chat_log.txt", "a") as log_file:
        log_file.write(f"User: {user_input}\nAgent: {response}\n\n")