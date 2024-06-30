import queue
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import socket
import threading
import json
import logging
import logging.config

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(name)s[%(process)d] %(levelname)s %(threadName)s[%(thread)d] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'DEBUG'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'chat_client.log',
            'formatter': 'detailed',
            'level': 'DEBUG'
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG'
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat-App")
        self.master.configure(bg='#333333')

        self.message_queue = queue.Queue()
        self.master.after(100, self.process_message_queue)

        # Create a frame to hold the user list and chat area
        self.frame = tk.Frame(master, bg='#333333')
        self.frame.grid(row=0, column=0, sticky='nsew')

        # Create a listbox to display online users
        self.user_listbox = tk.Listbox(self.frame, bg="#2C2F33", fg="#CDD6F4")
        self.user_listbox.grid(row=0, column=0, sticky='ns', padx=10, pady=10)

        # Create a scrolled text area for chat messages
        self.text_area = scrolledtext.ScrolledText(self.frame, state='disabled', bg="#2C2F33", fg="#CDD6F4")
        self.text_area.grid(row=0, column=1, rowspan=2, columnspan=3, sticky='ew', padx=10, pady=10)

        # Create an entry widget for message input
        self.msg_entry = tk.Entry(self.frame, bg="#40444B", fg="#CDD6F4", insertbackground="#CDD6F4")
        self.msg_entry.grid(row=2, column=0, columnspan=3, sticky='ew', padx=10, pady=10)
        self.msg_entry.bind("<Return>", self.send_message_event)

        # Create a button to send messages
        self.send_button = tk.Button(self.frame, text="Send", command=self.send_message, bg="#7289DA", fg="#CDD6F4")
        self.send_button.grid(row=2, column=3, padx=10, pady=10)

        # Create a button for private messages
        self.priv_msg_button = tk.Button(self.frame, text="Private Message", command=self.prepare_private_message, bg="#556B2F", fg="#CDD6F4")
        self.priv_msg_button.grid(row=3, column=0, padx=10, pady=10)

        # Create a button to connect to the server
        self.connect_button = tk.Button(self.frame, text="Connect", command=self.setup_connection, bg="#4CAF50", fg="#CDD6F4")
        self.connect_button.grid(row=3, column=1, padx=10, pady=10)

        self.client_socket = None
        self.username = None
        self.recipient = None

    def setup_connection(self):
        if not self.client_socket:
            self.username = simpledialog.askstring("Username", "Enter your username:", parent=self.master)
            host = simpledialog.askstring("Server IP", "Enter server IP:", initialvalue='your IP address here', parent=self.master)
            port = simpledialog.askinteger("Server Port", "Enter server port:", initialvalue=12345, parent=self.master)
            if host and port and self.username:
                try:
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.connect((host, port))
                    self.client_socket.sendall(json.dumps({"command": "connect",
                                                           "username": self.username}).encode('utf-8'))
                    threading.Thread(target=self.receive_messages, daemon=True).start()
                    messagebox.showinfo("Connection", "Successfully connected to the server.")
                    self.display_message(f"Connected to the server as {self.username}.")
                    logger.info("Connected to the server as %s.", self.username)
                except socket.error as e:
                    messagebox.showerror("Connection Error", f"Failed to connect to server: {str(e)}")
                    self.client_socket = None
                    logger.error("Failed to connect to server: %s", str(e))

    def send_message(self):
        message_content = self.msg_entry.get()
        if message_content:
            if message_content.startswith('/msg'):
                parts = message_content.split(' ', 2)
                if len(parts) >= 3:
                    recipient = parts[1].rstrip(':')
                    message_content = parts[2]
                    message = json.dumps({"command": "SendMsg", "from": self.username, "to": recipient, "message": message_content})
                    try:
                        self.client_socket.sendall(message.encode('utf-8'))
                        self.display_message(f"[You] to [{recipient}]: {message_content}", "#00FF00")
                        self.msg_entry.delete(0, tk.END)
                        self.msg_entry.config(fg="#CDD6F4")
                        logger.debug("Sent private message to %s: %s", recipient, message_content)
                    except Exception as e:
                        self.display_message(f"Failed to send message to {recipient}: {str(e)}")
                        logger.error("Failed to send private message to %s: %s", recipient, str(e))
                else:
                    self.display_message("Invalid private message format.")
                    logger.warning("Invalid private message format.")
            else:
                message = json.dumps({"command": "SendMsg", "from": self.username, "message": message_content})
                try:
                    self.client_socket.sendall(message.encode('utf-8'))
                    self.display_message(f"You: {message_content}")
                    self.msg_entry.delete(0, tk.END)
                    logger.debug("Sent message: %s", message_content)
                except Exception as e:
                    self.display_message(f"Failed to send message: {str(e)}")
                    logger.error("Failed to send message: %s", str(e))

    def send_message_event(self, event):
        self.send_message()
        return 'break'

    def prepare_private_message(self):
        recipient = simpledialog.askstring("Private Message", "Enter the recipient's username:", parent=self.master)
        if recipient:
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.insert(0, f"/msg {recipient}: ")
            self.msg_entry.config(fg="#00FF00")  # Set text color to glowing green
            logger.debug("Preparing private message for %s", recipient)

    def receive_messages(self):
        while True:
            try:
                message_json = self.client_socket.recv(1024).decode('utf-8')
                if not message_json:
                    break
                message = json.loads(message_json)
                if 'users' in message:
                    self.update_user_list(message['users'])
                else:
                    sender = message.get('sender', 'Unknown')
                    content = message.get('content', '')
                    if sender and content:
                        display_message = f"{sender}: {content}"
                        if 'to' in message:
                            recipient = message['to']
                            display_message = f"[{sender}] to [{recipient}]: {content}"
                            self.message_queue.put((display_message, "#00FF00"))
                        else:
                            self.message_queue.put((display_message, "#CDD6F4"))
            except (ConnectionResetError, ConnectionAbortedError, socket.error) as e:
                logger.error("Connection error: %s", str(e))
                break
            except Exception as e:
                self.display_message(f"Error: {str(e)}")
                logger.error("Error receiving messages: %s", str(e))
                break

    def display_message(self, message, color="#CDD6F4"):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n', color)
        self.text_area.tag_config(color, foreground=color)
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def process_message_queue(self):
        try:
            while not self.message_queue.empty():
                message, color = self.message_queue.get_nowait()
                self.display_message(message, color)
        finally:
            self.master.after(100, self.process_message_queue)

    def update_user_list(self, users):
        self.user_listbox.delete(0, tk.END)
        for user in users:
            self.user_listbox.insert(tk.END, user)
        logger.debug("Updated user list: %s", users)


def main():
    try:
        root = tk.Tk()
        app = ChatClient(root)
        root.mainloop()
    except Exception as e:
        logger.critical("Critical error in main: %s", str(e))


if __name__ == '__main__':
    main()
