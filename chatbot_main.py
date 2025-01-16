import tkinter as tk
from tkinter import scrolledtext, simpledialog
import chatbot_core

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Swarn Sah Chatbot")

        # Load agent names and responses
        self.agent_name = chatbot_core.get_random_agent_name("agent_names.txt")
        self.responses = chatbot_core.load_responses("config.json")

        # Chat header
        self.header = tk.Label(root, text=f"Welcome to Swarn Sah Chatbot!\nI am {self.agent_name}, your virtual assistant.",
                                font=("Arial", 12), bg="lightblue", pady=10)
        self.header.pack(fill=tk.X)

        # Chat history
        self.chat_history = scrolledtext.ScrolledText(root, state="disabled", wrap=tk.WORD, height=15, width=60, font=("Arial", 10))
        self.chat_history.pack(pady=10)

        # User input
        self.user_input = tk.Entry(root, font=("Arial", 12))
        self.user_input.pack(fill=tk.X, padx=10, pady=5)
        self.user_input.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message, font=("Arial", 12))
        self.send_button.pack(pady=5)

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12))
        self.exit_button.pack(pady=5)

        # Greeting
        self.user_name = None
        self.greet_user()

    def greet_user(self):
        self.user_name = tk.simpledialog.askstring("Name", "Please enter your name:")
        if not self.user_name:
            self.user_name = "Guest"
        self.display_message(f"Hello, {self.user_name}! How can I help you today?", is_agent=True)

    def send_message(self, event=None):
        user_text = self.user_input.get().strip().lower()
        if not user_text:
            return

        # Display user message
        self.display_message(user_text, is_agent=False)

        # Exit conditions
        if user_text in ["bye", "quit", "exit"]:
            self.display_message(f"Goodbye, {self.user_name}! Have a great day!", is_agent=True)
            self.root.quit()
            return

        # Generate agent response
        response = chatbot_core.detect_keywords(user_text, self.user_name, self.responses)
        self.display_message(response, is_agent=True)

        # Log the session
        chatbot_core.log_session(user_text, response)

    def display_message(self, message, is_agent):
        self.chat_history.configure(state="normal")
        if is_agent:
            self.chat_history.insert(tk.END, f"{self.agent_name}: {message}\n")
        else:
            self.chat_history.insert(tk.END, f"You: {message}\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.yview(tk.END)
        self.user_input.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()