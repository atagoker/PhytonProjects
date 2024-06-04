import threading
import json


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
                    command = message_dict.get('command')
                    if command == 'connect':
                        self.username = message_dict['username']
                        self.is_registered = True
                        self.server.clients[self.username] = self
                        self.server.broadcast({"sender": "Server", "content": f"{self.username} has joined the chat."},
                                              sender=self)
                    elif command == 'SendMsg':
                        content = message_dict['message']
                        if 'to' in message_dict:
                            recipient = message_dict['to']
                            self.handle_private_message(recipient, content)
                        else:
                            self.server.broadcast({"sender": self.username, "content": content}, sender=self)
            except Exception as e:
                print(f"Connection closed with {self.addr} due to error: {e}")
                break
        self.cleanup()

    def handle_private_message(self, recipient, msg_content):
        if recipient in self.server.clients:
            private_msg = {"sender": self.username, "content": msg_content}
            self.server.send_private_message(private_msg, recipient)
            print(f"Private message sent from {self.username} to {recipient}")
        else:
            print(f"Private message recipient {recipient} not found.")

    def receive(self):
        message_json = self.client_socket.recv(1024).decode('utf-8')
        return json.loads(message_json) if message_json else {}

    def cleanup(self):
        if self.username in self.server.clients:
            del self.server.clients[self.username]
        self.server.broadcast({"sender": "Server", "content": f"{self.username} has left the chat."}, sender=self)
        self.client_socket.close()
        print(f"Cleaned up {self.addr}")
