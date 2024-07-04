import turtle

class MainProgram:
    def __init__(self):
        self.__city_map = [
            "XXXXXXXXXXXX",
            "X...X..X..eX",
            "X.X....X.XXX",
            "X..X.X.X.X.X",
            "XX.XXX.X...X",
            "X........X.X",
            "XsXX...X...X",
            "XXXXXXXXXXXX"
        ]
        print('Hello World')
        # Map dimensions
        self.__rows = len(self.__city_map)
        self.__cols = len(self.__city_map[0])

        # Screen setup
        
        self.wn = turtle.Screen()
        self.wn.title("Turtle Keys")
        self.wn.setup(width=600, height=400)
        self.wn.setworldcoordinates(0, 0, self.__cols, self.__rows)
        self.wn.tracer(0, 0) 

        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()

        self.draw_map()

        # Create the player turtle
        self.__player = turtle.Turtle()
        self.__player.shape('triangle')
        self.__player.color('red')
        self.__player.penup()
        self.__player.speed(0)

        # Find the starting position 's'
        for y in range(self.__rows):
            for x in range(self.__cols):
                if self.__city_map[y][x] == 's':
                    self.__player.goto(x + 0.5, self.__rows - y - 0.5)
                    break

        # Key bindings
        self.wn.listen()


        # Update the screen
        self.wn.update()

    def draw_cell(self, x, y, color):
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.pendown()
        self.turtle.fillcolor(color)
        self.turtle.begin_fill()
        for _ in range(4):
            self.turtle.forward(1)
            self.turtle.left(90)
        self.turtle.end_fill()

    def draw_map(self):
        # Draw the map
        for y in range(self.__rows):
            for x in range(self.__cols):
                char = self.__city_map[y][x]
                if char == 'X':
                    self.draw_cell(x, self.__rows - y - 1, 'grey')
                elif char == 's':
                    self.draw_cell(x, self.__rows - y - 1, 'green')
                elif char == 'e':
                    self.draw_cell(x, self.__rows - y - 1, 'blue')
                else:
                    self.draw_cell(x, self.__rows - y - 1, 'white')
                    self.turtle.penup()
                    self.turtle.goto(x + 0.5, self.__rows - y - 1 + 0.5)
                    self.turtle.pendown()

        # Draw grid lines
        self.turtle.color('black')

        # Set the pensize for thicker grid lines
        self.turtle.pensize(3)

        for x in range(self.__cols + 1):
            self.turtle.penup()
            self.turtle.goto(x, 0)
            self.turtle.pendown()
            self.turtle.goto(x, self.__rows)

        for y in range(self.__rows + 1):
            self.turtle.penup()
            self.turtle.goto(0, y)
            self.turtle.pendown()
            self.turtle.goto(self.__cols, y)

    def up(self):
        x, y = self.player.position()
        if self.__city_map[self.__rows - int(y) - 2][int(x)] not in 'X':
            self.__player.setheading(90)
            self.__player.forward(1)

    def down(self):
        x, y = self.player.position()
        if self.__city_map[self.__rows - int(y)][int(x)] not in 'X':
            self.__player.setheading(270)
            self.__player.forward(1)

    def left(self):
        x, y = self.__player.position()
        if self.__city_map[self.__rows - int(y) - 1][int(x) - 1] not in 'X':
            self.__player.setheading(180)
            self.__player.forward(1)

    def right(self):
        x, y = self.__player.position()
        if self.__city_map[self.__rows - int(y) - 1][int(x) + 1] not in 'X':
            self.__player.setheading(0)
            self.__player.forward(1)

if __name__ == "__main__":
    MainProgram()
    turtle.mainloop()
