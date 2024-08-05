import turtle

# create a drone class (this is to make the creation of drones easier in the additional implementation)
class BaseDrone:
    def __init__(self, name, start_pos, target_pos, color, screen,):
        self.name = name
        self.position = start_pos
        self.screen = screen
        self.turtle = turtle.Turtle()
        self.turtle.shape('arrow')
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.goto(start_pos)
        self.target_pos = target_pos  
        self.turtle.pendown()
        self.path = [] 

    def move_up(self,city_map):
            self.turtle.penup()  # Ensure the pen is up before moving
            x, y = self.turtle.position()
            new_x, new_y = x, y + 1
            self.turtle.setheading(90)  # Face up
            if self.is_valid_move(new_x, new_y,city_map):
                self.turtle.goto(new_x, new_y)
            self.screen.update()

    def move_down(self,city_map):
            self.turtle.penup()  # Ensure the pen is up before moving
            x, y = self.turtle.position()
            new_x, new_y = x, y - 1
            self.turtle.setheading(270)  # Face down
            if self.is_valid_move(new_x, new_y,city_map):
                self.turtle.goto(new_x, new_y)
            self.screen.update()

    def move_left(self,city_map):
            self.turtle.penup()  # Ensure the pen is up before moving
            x, y = self.turtle.position()
            new_x, new_y = x - 1, y
            self.turtle.setheading(180)  # Face left
            if self.is_valid_move(new_x, new_y,city_map):
                self.turtle.goto(new_x, new_y)
            self.screen.update()

    def move_right(self,city_map):
            self.turtle.penup()  # Ensure the pen is up before moving
            x, y = self.turtle.position()
            new_x, new_y = x + 1, y
            self.turtle.setheading(0)  # Face right
            if self.is_valid_move(new_x, new_y,city_map):
                self.turtle.goto(new_x, new_y)
            self.screen.update()

    def is_valid_move(self, x, y, city_map):
        rows, cols = len(city_map), len(city_map[0])
        map_x, map_y = int(x), int(rows - y)
        if 0 <= map_x < cols and 0 <= map_y < rows:
            return city_map[map_y][map_x] != 'X'
        return False

