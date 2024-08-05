import turtle
from DroneLinkedList import DroneLinkedList
from drone import BaseDrone
from SWindiv import SpecialControl
from program import ProgramControl


class MainProgram(ProgramControl, SpecialControl):
    def __init__(self):
        super().__init__()
        with open('city001.txt', 'r') as file:
            self.city_map = [line.strip() for line in file.readlines()]

        # Map dimensions
        self.rows = len(self.city_map)
        self.cols = len(self.city_map[0])

        # Screen setup
        self.screen = turtle.Screen()
        self.screen.clear()
        self.screen.title('DSAA CA2')
        self.screen.setup(width=800, height=600)
        self.screen.setworldcoordinates(0, 0, self.cols, self.rows)
        self.screen.tracer(0, 0)

        self.write_text()
        self.draw_map()

        # Create the custom player turtle shape
        self.shape = ((0, 10), (-10, -10), (0, -5), (10, -10), (0, 10))
        self.screen.register_shape("arrow", self.shape)

        # Initialize drones linked list
        self.drones = DroneLinkedList()

        # needed for hiding/showing path function
        self.autopilot_finished = False
        self.path_visible = True  # Track visibility state of path circles
        self.path_circles = []  # Store references to path circles

        # Find the starting position 's'
        self.start_pos = None
        for y in range(self.rows):
            for x in range(self.cols):
                if self.city_map[y][x] == 's':
                    self.start_pos = (x + 0.5, self.rows - y - 0.5)
                    break
            if self.start_pos:
                break

        # Find the target position 'e'
        self.target_pos = None
        for y in range(self.rows):
            for x in range(self.cols):
                if self.city_map[y][x] == 'e':
                    self.target_pos = (x + 0.5, y)
                    break
            if self.target_pos:
                break

        # Initialize player drone
        self.player = BaseDrone("Original Drone", self.start_pos, self.target_pos, "red", self.screen)
        self.drones.append(self.player)

        self.current_drone_node = self.drones.head  # Start with player drone
        self.screen.listen()

        # Setup screen control function
        self.screen_control()

        # State Variable to track weather state
        self.is_weather = False

    def screen_control(self):
        self.screen.onkey(self.up, 'Up')
        self.screen.onkey(self.down, 'Down')
        self.screen.onkey(self.left, 'Left')
        self.screen.onkey(self.right, 'Right')
        self.screen.onkey(self.calculate_shortest_path, 'f')
        self.screen.onkey(self.autopilot_mode, 'g')
        self.screen.onkey(self.pause_mode, 'p')
        self.screen.onkey(self.hide_path, 'h')
        self.screen.onkey(self.reset, 'r')
        self.screen.onkey(self.continue_program, 'c')
        self.screen.onkey(self.quit_program, 'q')

        # Additional feature 1 (SW)
        self.screen.onkey(self.add_drone, '+')
        self.screen.onkey(self.switch_drone, 't')
        self.screen.onkey(self.delete_drone, 'BackSpace')
        self.screen.onscreenclick(self.choose_end, 1)  # Left mouse click

        # Additional feature 2 (SW)
        self.screen.onkey(self.weather_randomizer, 'w')
        self.screen.onkey(self.disable_weather, 's')

        # Update the screen
        self.draw_map()
        self.screen.update()
    def is_in_hurricane_zone(self, x, y):
        return (x, y) in self.affected_cells

    def up(self):
        new_x, new_y = self.get_new_position(0, 1)
        if not self.is_in_hurricane_zone(new_x, new_y):
            self.drones.get_current_drone().move_up(self.city_map)

    def down(self):
        new_x, new_y = self.get_new_position(0, -1)
        if not self.is_in_hurricane_zone(new_x, new_y):
            self.drones.get_current_drone().move_down(self.city_map)

    def left(self):
        new_x, new_y = self.get_new_position(-1, 0)
        if not self.is_in_hurricane_zone(new_x, new_y):
            self.drones.get_current_drone().move_left(self.city_map)

    def right(self):
        new_x, new_y = self.get_new_position(1, 0)
        if not self.is_in_hurricane_zone(new_x, new_y):
            self.drones.get_current_drone().move_right(self.city_map)

    def get_current_position(self):
        x, y = self.drones.get_current_drone().turtle.position()
        return int(x - 0.5), int(self.rows - y - 0.5)

    def get_new_position(self, dx, dy):
        current_x, current_y = self.get_current_position()
        new_x = current_x + dx
        new_y = current_y + dy
        return new_x, new_y


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
                elif char == 'e':
                    self.draw_cell(x, self.rows - y - 1, 'turquoise')
                    self.draw_circle(x, self.rows - y - 1, 'e', color='turquoise', text_color='black',border_color='blue', border_thickness=5)
                elif char == 's':
                    self.draw_cell(x, self.rows - y - 1, 'lightgreen')
                    self.draw_circle(x, self.rows - y - 1, 'S', color='lightgreen', text_color='black', border_color='darkgreen', border_thickness=5)
                
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



if __name__ == "__main__":
    program = MainProgram()
    turtle.done()
