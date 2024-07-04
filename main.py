import turtle

class MainProgram:
    def __init__(self):
        with open('city001.txt', 'r') as file:
            self.__city_map = [line.strip() for line in file.readlines()]

        # Map dimensions
        self.__rows = len(self.__city_map)
        self.__cols = len(self.__city_map[0])

        # Screen setup
        self.__screen = turtle.Screen()
        self.__screen.title('DSAA CA2')
        self.__screen.setup(width=800, height=600)
        self.__screen.setworldcoordinates(0, 0, self.__cols, self.__rows)
        self.__screen.tracer(0, 0)

        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()

        self.write_text()
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
        self.__screen.listen()
        self.__screen.onkey(self.up, 'Up')
        self.__screen.onkey(self.down, 'Down')
        self.__screen.onkey(self.left, 'Left')
        self.__screen.onkey(self.right, 'Right')

        # Update the screen
        self.__screen.update()

    def write_text(self):
        self.turtle.penup()
        self.turtle.goto(self.__cols / 2, self.__rows + 1)
        self.turtle.write("COFFEE~GO~DRONE: Done by Joon Yi, Sheng Wei, Clemens DAAA/2A/02", align="center", font=("Arial", 16, "bold"))
        self.turtle.goto(self.__cols / 2, self.__rows)
        self.turtle.write("DRONE STATUS= Manual Mode: Use arrow keys to navigate (press 'f' to calculate shortest path)\n", align="center", font=("Arial", 12, "normal"))
        self.turtle.goto(0, 0)  # Reset position

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
        x, y = self.__player.position()
        new_x, new_y = x, y + 1
        if self.is_valid_move(new_x, new_y):
            self.__player.goto(new_x, new_y)
        self.__screen.update()

    def down(self):
        x, y = self.__player.position()
        new_x, new_y = x, y - 1
        if self.is_valid_move(new_x, new_y):
            self.__player.goto(new_x, new_y)
        self.__screen.update()

    def left(self):
        x, y = self.__player.position()
        new_x, new_y = x - 1, y
        if self.is_valid_move(new_x, new_y):
            self.__player.goto(new_x, new_y)
        self.__screen.update()

    def right(self):
        x, y = self.__player.position()
        new_x, new_y = x + 1, y
        if self.is_valid_move(new_x, new_y):
            self.__player.goto(new_x, new_y)
        self.__screen.update()

    def is_valid_move(self, x, y):
        map_x, map_y = int(x), int(self.__rows - y - 1)
        if 0 <= map_x < self.__cols and 0 <= map_y < self.__rows:
            return self.__city_map[map_y][map_x] != 'X'
        return False

if __name__ == "__main__":
    MainProgram()
    turtle.mainloop()
