# main.py
from server import Server  # Import the Server class itself


def main():
    server = Server('your IP adress', 12345)
    server.start()


if __name__ == '__main__':
    main()
