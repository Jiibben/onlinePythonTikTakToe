import socket
from time import sleep
import utilities
import tiktaktoe_local


game = tiktaktoe_local.TikTakToe(3,3)

IP = socket.gethostbyname(socket.gethostname())
PORT = 50505

ADDR = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

game.print_grid()

client.connect(ADDR)

sign = ""

while True:
    a = client.recv(2048)
    if len(a) > 0:
        msg = utilities.load_message(a)
        if msg["command"] == "play":
            case = list(input(f"enter a case: ").split(" "))
            game.fill_case(sign, int(case[0]), int(case[1]))
            game.print_grid()

            if game.check_win(sign):
                client.send(utilities.create_message("move_noc",case))
                sleep(0.5)
                client.send(utilities.create_message("win"))
            else:
                client.send(utilities.create_message("move", case))
        elif msg["command"] == "sign":
            print(f"you're sign {msg['message']}")
            sign = msg["message"]
        elif msg["command"] == "update":
            x,y,s= msg["message"]
            game.fill_case(s, int(x),int(y))
            game.print_grid()                 
        elif msg["command"] == "player_win":
            print(msg["message"])
        