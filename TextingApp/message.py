import json


class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

    def to_json(self):
        return json.dumps({"sender": self.sender, "content": self.content})

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Message(data['sender'], data['content'])


if __name__ == "__main__":
    msg = Message("user1", "Hello, world!")
    json_msg = msg.to_json()
    print(json_msg)
    received_msg = Message.from_json(json_msg)
    print(f"Received Message from {received_msg.sender}: {received_msg.content}")
