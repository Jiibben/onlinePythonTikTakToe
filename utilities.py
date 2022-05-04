import json

def create_message(command="test", message=""):
    return json.dumps({"command":command, "message":message}).encode('utf-8')

def load_message(b_msg):
    return json.loads(b_msg.decode('utf-8'))




