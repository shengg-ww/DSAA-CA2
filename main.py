import turtle
from program import ProgramControl
import turtle
import networkx as nx


class MainProgram(ProgramControl):
    def __init__(self):
        super().__init__()
        with open('city001.txt', 'r') as file:
            self.city_map = [line.strip() for line in file.readlines()]

        # Map dimensions
        self.rows = len(self.city_map)
        self.cols = len(self.city_map[0])

        # # Screen setup
        self.screen = turtle.Screen()
        self.screen.title('DSAA CA2')
        self.screen.setup(width=800, height=600)
        self.screen.setworldcoordinates(0, 0, self.cols, self.rows)
        self.screen.tracer(0, 0)

        self.write_text()
        self.draw_map()

        # Create the custom player turtle shape
        self.shape = ((0, 10), (-10, -10), (0, -5), (10, -10), (0, 10))
        self.screen.register_shape("arrow", self.shape)

        # Create the player turtle
        self.player = turtle.Turtle()
        self.player.shape('arrow')
        self.player.color('red')
        self.player.penup()
        self.player.speed(0)

        # Find the starting position 's'
        for y in range(self.rows):
            for x in range(self.cols):
                if self.city_map[y][x] == 's':
                    self.player.goto(x + 0.5, self.rows - y - 0.5)
                    break

        # Key bindings
        self.screen.listen()
        self.screen.onkey(self.up, 'Up')
        self.screen.onkey(self.down, 'Down')
        self.screen.onkey(self.left, 'Left')
        self.screen.onkey(self.right, 'Right')
        self.screen.onkey(self.calculate_shortest_path, 'f')
        self.screen.onkey(self.autopilot_mode, 'g')
        self.screen.onkey(self.pause_mode, 'p')
        self.screen.onkey(self.hide_path,'h')
        self.screen.onkey(self.reset,'r')
        self.screen.onkey(self.quit_program,'q')


        # Update the screen
        self.screen.update()

    def get_current_position(self):
        x, y = self.player.position()
        return int(x - 0.5), int(self.rows - y - 0.5)

    def write_text(self):
        self.turtle.penup()
        self.turtle.goto(self.cols / 2, self.rows + 1)
        self.turtle.write("COFFEE~GO~DRONE: Done by Sheng Wei, Joon Yi, Clemens DAAA/2A/02", align="center", font=("Arial", 16, "bold"))
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
        self.update_status_text("DRONE STATUS= Manual Mode: Use arrow keys to navigate (press 'f' to calculate shortest path)")
        # Draw the map
        for y in range(self.rows):
            for x in range(self.cols):
                char = self.city_map[y][x]
                if char == 'X':
                    self.draw_cell(x, self.rows - y - 1, 'grey')
                elif char == 's':
                    self.draw_cell(x, self.rows - y - 1, 'lightgreen')
                    self.draw_circle(x, self.rows - y - 1, 'S', color='lightgreen', border_color='darkgreen', border_thickness=5)
                elif char == 'e':
                    self.draw_cell(x, self.rows - y - 1, 'turquoise')
                    self.draw_circle(x, self.rows - y - 1, 'e', color='turquoise', border_color='darkblue', border_thickness=5)
                else:
                    self.draw_cell(x, self.rows - y - 1, 'white')
                    self.turtle.penup()
                    self.turtle.goto(x + 0.5, self.rows - y - 1 + 0.5)
                    self.turtle.pendown()

        # Draw grid lines
        self.turtle.color('black')

        # Set the pensize for thicker grid lines
        self.turtle.pensize(3)

        for x in range(self.cols + 1):
            self.turtle.penup()
            self.turtle.goto(x, 0)
            self.turtle.pendown()
            self.turtle.goto(x, self.rows)

        for y in range(self.rows + 1):
            self.turtle.penup()
            self.turtle.goto(0, y)
            self.turtle.pendown()
            self.turtle.goto(self.cols, y)

    def up(self):
        x, y = self.player.position()
        new_x, new_y = x, y + 1
        self.player.setheading(90)  # Face up
        
        if self.is_valid_move(new_x, new_y):
            self.player.goto(new_x, new_y)
        self.screen.update()

    def down(self):
        x, y = self.player.position()
        new_x, new_y = x, y - 1 
        self.player.setheading(270)  # Face down
        if self.is_valid_move(new_x, new_y):
            self.player.goto(new_x, new_y)
        self.screen.update()

    def left(self):
        x, y = self.player.position()
        new_x, new_y = x - 1, y 
        self.player.setheading(180)  # Face left
        if self.is_valid_move(new_x, new_y):
            self.player.goto(new_x, new_y)
        self.screen.update()

    def right(self):
        x, y = self.player.position()
        new_x, new_y = x + 1, y
        self.player.setheading(0)  # Face right
        if self.is_valid_move(new_x, new_y):     
            self.player.goto(new_x, new_y)
        self.screen.update()

    def is_valid_move(self, x, y):
        map_x, map_y = int(x), int(self.rows - y)
        if 0 <= map_x < self.cols and 0 <= map_y < self.rows:
            return self.city_map[map_y][map_x] != 'X'
        return False

if __name__ == "__main__":
    program = MainProgram()
    turtle.done()
