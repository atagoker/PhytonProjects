import socket
import json


def main():
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    username = input("Enter your username: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        init_message = json.dumps({"command": "connect", "username": username})
        client_socket.sendall(init_message.encode('utf-8'))
        print(f"Connected to the server at {host}:{port}. You can start sending messages!")

        while True:
            message_content = input("Enter message (type 'quit' to exit): ")
            if message_content.lower() == 'quit':
                break

            if message_content.startswith('/msg'):
                parts = message_content.split(' ', 2)
                if len(parts) < 3:
                    print("Invalid private message format. Use: /msg recipient message")
                    continue
                recipient, actual_message = parts[1], parts[2]
                message = json.dumps({
                    "command": "SendMsg",
                    "from": username,
                    "to": recipient,
                    "message": actual_message
                })
            else:
                message = json.dumps({
                    "command": "SendMsg",
                    "from": username,
                    "message": message_content
                })

            client_socket.sendall(message.encode('utf-8'))


if __name__ == '__main__':
    main()
