# program_control.py

import turtle
import networkx as nx
from SWindiv import SpecialControl
from drone import BaseDrone
from DroneLinkedList import DroneLinkedList

class ProgramControl(SpecialControl):
    def __init__(self):


        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()

        self.circle = turtle.Turtle()
        self.circle.speed(0)
        self.circle.hideturtle()

        self.spiral = turtle.Turtle()
        self.spiral.speed(0)
        self.spiral.hideturtle()

        self.status_turtle = turtle.Turtle()
        self.status_turtle.speed(0)
        self.status_turtle.hideturtle()

        self.yellow_circles = []
        self.is_paused = False
        self.affected_cells = set()
        self.path_visible = False


    def update_status_text(self, text):
        self.status_turtle.clear()
        self.status_turtle.penup()
        self.status_turtle.goto(self.cols / 2, self.rows + 0.5)
        self.status_turtle.write(text, align="center", font=("Arial", 12, "normal"))
        self.screen.update()

    def draw_spiral(self, x, y, spiral_size=0.0005, iterations=180):
        self.spiral.penup()
        self.spiral.goto(x + 0.5, y + 0.5)
        self.spiral.setheading(0)
        self.spiral.pendown()

        for i in range(iterations):
            self.spiral.forward(spiral_size * i)
            self.spiral.right(15)

        self.spiral.penup()

    def draw_circle(self, x, y, letter=None, color='', text_color='black', border_color='', border_thickness=2):
        self.circle.penup()
        self.circle.goto(x + 0.5, y + 0.25)

        self.circle.pencolor(border_color)
        self.circle.pensize(border_thickness)
        self.circle.fillcolor(color)

        self.circle.pendown()
        self.circle.begin_fill()
        self.circle.circle(0.3)
        self.circle.end_fill()
        self.circle.penup()

        if letter:
            self.circle.goto(x + 0.5, y + 0.3)
            self.circle.pendown()
            self.circle.color(text_color)
            self.circle.write(letter, align="center", font=("Arial", 24, "bold"))

        if color == 'yellow':
            self.yellow_circles.append(self.circle)

        self.circle.pensize(0.5)
        self.circle.pencolor('black')

    def clear_yellow_circles(self):
        for circle in self.yellow_circles:
            circle.clear()
        for y in range(self.rows):
            for x in range(self.cols):
                char = self.city_map[y][x]
                if char == 'e':
                    self.draw_circle(x, self.rows - y - 1, 'e', color='turquoise', text_color='black', border_color='darkblue', border_thickness=5)
                elif char == 's':
                    self.draw_circle(x, self.rows - y - 1, 'S', color='lightgreen', text_color='black', border_color='darkgreen', border_thickness=5)

    def calculate_shortest_path(self):
        self.clear_yellow_circles()  # Clear previous yellow circles
        self.path_visible = True
        # Clear status messages or other necessary parts of the screen
        self.status_turtle.clear()
        self.screen.update()

        start = self.get_current_position()
        current_drone = self.drones.get_current_drone()
        end = current_drone.target_pos

        if start and end:
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))

            G = nx.grid_2d_graph(self.rows, self.cols)

            for x in range(self.rows):
                for y in range(self.cols):
                    if self.city_map[x][y] == 'X' or (y, x) in self.affected_cells:
                        G.remove_node((x, y))

            for drone in self.drones:
                if drone != current_drone:
                    drone_pos = (int(drone.turtle.xcor() - 0.5), int(self.rows - drone.turtle.ycor() - 0.5))
                    if (drone_pos[1], drone_pos[0]) in G:
                        G.remove_node((drone_pos[1], drone_pos[0]))

            try:
                path = nx.shortest_path(G, source=(start[1], start[0]), target=(end[1], end[0]), weight=None, method='dijkstra')
                current_drone.path = [(x, y) for y, x in path]


                # to store the path of circles
                self.path_circles = []

                # to store the path of circles
                self.path_circles = []

                for node in current_drone.path:
                    circle = self.draw_circle(node[0], self.rows - node[1] - 1, color='yellow', border_color='black', border_thickness=4)
                    self.path_circles.append(circle)

                self.update_status_text("DRONE STATUS= Ready to take off in autopilot mode (press 'g')")
                return path
            except nx.NetworkXNoPath:
                self.update_status_text("DRONE STATUS= No path found. Manual Control may be required")
                return None
            
    def autopilot_mode(self):
        current_drone = self.drones.get_current_drone()
        if not current_drone.path:
            self.update_status_text("No path to follow. Please calculate the path first (press 'f').")
            return

        self.update_status_text(f"Automatic Pilot: {current_drone.name} following pre-calculated path. Press 'p' to toggle pause/resume.")
        steps = 0

        for i in range(len(current_drone.path) - 1):
            while self.is_paused:
                self.update_status_text("Paused. Press 'p' to resume.")
                self.screen.update()
                turtle.time.sleep(0.1)

            current_pos = current_drone.path[i]
            next_pos = current_drone.path[i + 1]

            if next_pos[1] > current_pos[1]:
                current_drone.turtle.penup()
                current_drone.turtle.setheading(270)
            elif next_pos[1] < current_pos[1]:
                current_drone.turtle.penup()
                current_drone.turtle.setheading(90)
            elif next_pos[0] > current_pos[0]:
                current_drone.turtle.penup()
                current_drone.turtle.setheading(0)
            elif next_pos[0] < current_pos[0]:
                current_drone.turtle.penup()
                current_drone.turtle.setheading(180)

            current_drone.turtle.goto(next_pos[0] + 0.5, self.rows - next_pos[1] - 0.5)
            self.screen.update()
            turtle.time.sleep(0.5)
            steps += 1

        end_pos = current_drone.path[-1]
        current_drone.turtle.goto(end_pos[0] + 0.5, self.rows - end_pos[1] - 0.5)
        self.screen.update()

        self.update_status_text(f"Automatic Pilot: {current_drone.name} reached destination {end_pos} in {steps} steps. Press 'c' to continue.")

    def pause_mode(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.update_status_text("Paused. Press 'p' to resume.")
        else:
            self.update_status_text("Resumed. Press 'p' to pause.")

    def hide_path(self):
        # check whether path is visible
        if self.path_visible: 
            for circle in self.path_circles:
                circle.clear() #clear the drawings (hide)
                circle.hideturtle()
            self.path_visible = False #update visibility to false
        else:
            for node in self.drones[self.current_drone_index].path:
                circle = self.draw_circle(node[0], self.rows - node[1] - 1, color='yellow', border_color='black', border_thickness=4)
                self.path_circles.append(circle) #redraw and store the new circle
            self.path_visible = True #update visibility to true
        self.screen.update()
        
    def quit_program(self):
        turtle.bye()

    def continue_program(self):
        if self.is_paused:
            return
        self.draw_map()
        self.screen.update()
        self.update_status_text('Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)')

    def reset(self):
        if self.is_paused:
            return
        self.screen.clear()
        turtle.tracer(0)

        with open('city001.txt', 'r') as file:
            self.city_map = [line.strip() for line in file.readlines()]

        self.draw_map()
        self.write_text()

        self.player = BaseDrone("Original Drone", self.start_pos, self.target_pos, "red", self.screen)
        self.drones = DroneLinkedList()
        self.drones.append(self.player)
        self.current_drone_index = 0

        self.screen_control()