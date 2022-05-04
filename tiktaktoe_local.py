import json

class TikTakToe:
    def __init__(self, height, width):

        self.__height = height
        self.__width = width
        self.__grid = [["n" for x in range(self.__width)] for y in range(self.__height)]
        self.__emptysign = "n"
        
    def print_grid(self):
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__grid[y][x] == self.__emptysign:
                    print(" ", end="")
                else:
                    print(self.__grid[y][x], end="")
                if x != self.__width -1:
                    print(" | ", end="")
            if y != self.__height -1:
                print("\n" + "+".join(["--" if i == 0 or i == self.__width -1 else "---" for i in range(self.__width)]))
        print("\n")

    def fill_case(self, tick, x,y):
        if x < self.__width and y < self.__height and self.__get_case(x,y) == self.__emptysign :
            self.__grid[y][x] = tick
        else:
            raise IndexError("Outside of grid")


    def save_json(self):
        return json.dumps(self.__grid)

    def __get_case(self, x,y):
        return self.__grid[y][x]
    
    def load_json(self,js):
        self.__grid = json.loads(js)
        

    def check_win(self, sign):
        a = []
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__get_case(x,y) != self.__emptysign:
                    a.append(self.__check_para(x,y, sign))
                    a.append(self.__check_vert(x,y,sign))
                    a.append(self.__check_horiz(x,y,sign))
                    a.append(self.__check_para2(x,y, sign))
        return any(a)
    
    def check_draw(self, sign):
        if not self.check_win(sign):
            for y in range(self.__height):
                for x in range(self.__width):
                    self.__get_case(x,y)

    
    def __check_para(self, x, y, sign):
        a = []
        for d in range(3):
            if x + d < self.__width and y + d < self.__height:
                a.append(self.__get_case(x + d, y + d))
        return len(a) == 3 and (a[0] == a[1] == a[2] == sign)
    
    def __check_para2(self, x, y, sign):
        a = []
        for d in range(3):
            if x + d < self.__width and y - d >= 0:
                a.append(self.__get_case(x + d , y - d))
        return len(a) == 3 and (a[0] == a[1] == a[2] == sign)

    def __check_vert(self,x,y,sign):
        a = []
        for d in range(3):
            if x  < self.__width and y + d < self.__height:
                a.append(self.__get_case(x, y + d))
        return len(a) == 3 and (a[0] == a[1] == a[2] == sign)

    def __check_horiz(self,x,y,sign):
            a = []
            for d in range(3):
                if x  + d < self.__width and y < self.__height:

                    a.append(self.__get_case(x +d, y))
            return len(a) == 3 and (a[0] == a[1] == a[2] == sign)


if __name__ == "__main__":
    game = TikTakToe(150,30)

    p1 = {"sign": "x", "name" : "Jibb"}
    p2 = {"sign": "o", "name" : "Toto"}

    players = [p1, p2]
    run = 0
    running = True
    while running:
        #player handling
        player = players[run % 2]
        sign = player["sign"]
        name = player["name"]

        #print game board
        game.print_grid()

        # ask for input to place 
        while True:
            try:
                x,y = tuple(input(f"It's {name} turn place {sign}: ").split(" "))
                print(int(x), int(y))
                game.fill_case(sign, int(x),int(y))
                break
            except IndexError:
                print("Not inside board")
            except TypeError:
                print("position must be integrals")
            except ValueError:
                print("you must provide a placement")
        #check win
        if game.check_win(sign):
            print(f"Player {name} wins aka {sign}")
            break

        #next turn
        run +=1