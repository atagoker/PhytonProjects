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
            'filename': 'chat_server.log',
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

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, addr, server):
        super().__init__()
        self.client_socket = client_socket
        self.addr = addr
        self.server = server
        self.username = None
        self.is_registered = False

    def run(self):
        while True:
            try:
                message_dict = self.receive()
                if message_dict:
                    logger.debug(f"Received message from {self.addr}: {message_dict}")  # Log received message
                    command = message_dict.get('command')
                    if command == 'connect':
                        self.username = message_dict['username']
                        self.is_registered = True
                        self.server.clients[self.username] = self
                        self.server.broadcast({"sender": "Server", "content": f"{self.username} has joined the chat."}, sender=self)
                        self.server.broadcast_users()
                    elif command == 'SendMsg':
                        content = message_dict['message']
                        if 'to' in message_dict:
                            recipient = message_dict['to']
                            self.handle_private_message(recipient, content)
                        else:
                            self.server.broadcast({"sender": self.username, "content": content}, sender=self)
            except (ConnectionResetError, ConnectionAbortedError) as e:
                logger.error(f"Connection closed with {self.addr} due to error: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error with {self.addr}: {e}")
                break
        self.cleanup()

    def handle_private_message(self, recipient, msg_content):
        if recipient in self.server.clients:
            private_msg = {"sender": self.username, "content": msg_content, "to": recipient}
            self.server.send_private_message(private_msg, recipient)
            logger.debug(f"Private message sent from {self.username} to {recipient}")  # Log private message
        else:
            self.client_socket.sendall(json.dumps({"sender": "Server", "content": f"Private message recipient {recipient} not found."}).encode('utf-8'))
            logger.warning(f"Private message recipient {recipient} not found.")  # Log warning if recipient not found

    def receive(self):
        try:
            message_json = self.client_socket.recv(1024).decode('utf-8')
            if not message_json:
                raise ConnectionResetError("Connection closed by the client.")
            return json.loads(message_json) if message_json else {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON message: {e}")
            return {}
        except ConnectionResetError as e:
            raise e
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            return {}

    def cleanup(self):
        if self.username in self.server.clients:
            del self.server.clients[self.username]
        self.server.broadcast({"sender": "Server", "content": f"{self.username} has left the chat."}, sender=self)
        self.server.broadcast_users()
        self.client_socket.close()
        logger.info(f"Cleaned up {self.addr}")

class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.clients = {}
        self.messages = []  # Example storage for messages

    def start(self):
        while True:
            try:
                self.server_socket.bind((self.host, self.port))
                break
            except socket.error as e:
                logger.error(f"Port {self.port} is already in use. Trying another port.")
                self.port += 1

        self.server_socket.listen()
        logger.info(f"Server started on {self.host}:{self.port}, waiting for connections...")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                logger.info(f"Connected by {addr}")
                client_handler = ClientHandler(client_socket, addr, self)
                client_handler.start()
        except KeyboardInterrupt:
            logger.info("Server is shutting down.")
        finally:
            self.server_socket.close()

    def broadcast(self, message, sender=None):
        message_json = json.dumps(message).encode('utf-8')
        for username, client in self.clients.items():
            if client != sender:
                client.client_socket.sendall(message_json)
        logger.debug(f"Broadcast message: {message}")  # Log broadcast messages

    def send_private_message(self, message, recipient):
        message_json = json.dumps(message).encode('utf-8')
        if recipient in self.clients:
            self.clients[recipient].client_socket.sendall(message_json)
        logger.debug(f"Sent private message to {recipient}: {message}")  # Log private messages

    def broadcast_users(self):
        user_list = list(self.clients.keys())
        user_list_message = json.dumps({"users": user_list}).encode('utf-8')
        for client in self.clients.values():
            client.client_socket.sendall(user_list_message)
        logger.debug(f"Broadcast users list: {user_list}")  # Log user list broadcast


if __name__ == "__main__":
    try:
        HOST, PORT = '192.168.1.19', 12345  # Updated initial IP address
        server = Server(HOST, PORT)
        server.start()
    except Exception as e:
        logger.critical("Critical error in main: %s", str(e))
