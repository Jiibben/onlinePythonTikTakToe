import threading
import socket
from time import sleep
import utilities


lock = threading.Lock()
IP = socket.gethostbyname(socket.gethostname())
PORT = 50505

ADDR = (IP, PORT)


SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)


players_list = []

def handle_player_connection(conn, addr, player, pcount):

    while True:
        a = conn.recv(2048)
        if len(a) > 0:
            lock.acquire()
            msg = utilities.load_message(a)

            if msg["command"] == "test":
                print("test")

            elif msg["command"] == "name":
                player["name"] = msg["message"]

            elif msg["command"] == "move":
                msg["message"].append(player["sign"])
                broadcast(utilities.create_message("update", msg["message"]),player)
                sleep(0.5)
                broadcast(utilities.create_message("play"), player)
            elif msg["command"] == "move_noc":
                msg["message"].append(player["sign"])
                broadcast(utilities.create_message("update", msg["message"]),player)
            elif msg["command"] == "win":
                emit(utilities.create_message("player_win", f'{player["sign"]} won'))
            lock.release()


def broadcast(msg, sender):
    for i in players_list:
        if i["conn"] is not sender["conn"]:
            i["conn"].send(msg)

def emit(msg):
    for i in players_list:
        i["conn"].send(msg)

def start_server():
    player_count = 0
    SERVER.listen()


    while player_count <2:
        conn, addr = SERVER.accept()

        p = {"conn":None, "name":"", "sign": "x" if player_count == 0 else "o"}
        p["conn"] = conn
        players_list.append(p)
        conn.send(utilities.create_message("sign", p["sign"]))
        thread = threading.Thread(target=handle_player_connection, args=(conn, addr, p, player_count))
        thread.start()
        player_count +=1
    
    broadcast(utilities.create_message("play"), p)
    
try:
    start_server()

finally:
    SERVER.close()