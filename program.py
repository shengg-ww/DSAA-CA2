import turtle
import networkx as nx
from SWindiv import SpecialControl

class ProgramControl(SpecialControl):
    def __init__(self):

        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()

        self.circle = turtle.Turtle()
        self.circle.speed(0)
        self.circle.hideturtle()

        self.status_turtle = turtle.Turtle()
        self.status_turtle.speed(0)
        self.status_turtle.hideturtle()

        # List to track yellow circles
        self.yellow_circles = []
        

    def update_status_text(self, text):
        self.status_turtle.clear()
        self.status_turtle.penup()
        self.status_turtle.goto(self.cols / 2, self.rows + 0.5)
        self.status_turtle.write(text, align="center", font=("Arial", 12, "normal"))
        self.screen.update()

    def draw_circle(self, x, y, letter=None, color='', text_color='black', border_color='', border_thickness=2):
        self.circle.penup()
        self.circle.goto(x + 0.5, y + 0.25)
        
        # Set the pen color and fill color
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
        
        self.circle.pensize(0.5)  # Reset pen size
        self.circle.pencolor('black')  # Reset pen color to default

    def clear_yellow_circles(self):
        for circle in self.yellow_circles:
            circle.clear()
        for y in range(self.rows):
            for x in range(self.cols):
                char = self.city_map[y][x]
                if char == 'e':
                    self.draw_circle(x, self.rows - y - 1, 'e', color='turquoise',text_color='black', border_color='darkblue', border_thickness=5)
                elif char=='s':
                    self.draw_circle(x, self.rows - y - 1, 'S', color='lightgreen',text_color='black', border_color='darkgreen', border_thickness=5)
        

    def calculate_shortest_path(self):
        self.clear_yellow_circles()  # Clear previous yellow circles

        # Clear status messages or other necessary parts of the screen
        self.status_turtle.clear()
        self.screen.update()

        start = self.get_current_position()
        current_drone = self.drones[self.current_drone_index]
        end = current_drone.target_pos  # Use the target position of the current drone

        if start and end:
            start = (int(start[0]), int(start[1]))  # Ensure start coordinates are integers
            end = (int(end[0]), int(end[1]))  # Ensure end coordinates are integers

            G = nx.grid_2d_graph(self.rows, self.cols)

            # Remove nodes that are obstacles
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.city_map[y][x] == 'X':
                        G.remove_node((y, x))

            # Remove nodes that correspond to the positions of other drones
            for drone in self.drones:
                if drone != current_drone:
                    drone_pos = (int(drone.turtle.xcor() - 0.5), int(self.rows - drone.turtle.ycor() - 0.5))
                    if (drone_pos[1], drone_pos[0]) in G:
                        G.remove_node((drone_pos[1], drone_pos[0]))

            # Use Dijkstra's algorithm to find the shortest path
            try:
                path = nx.shortest_path(G, source=(start[1], start[0]), target=(end[1], end[0]), weight=None, method='dijkstra')
                # Convert the path back to the format (x, y)
                current_drone.path = [(x, y) for y, x in path]  # Store the path in the current drone's path attribute

                for node in current_drone.path:
                    self.draw_circle(node[0], self.rows - node[1] - 1, color='yellow', border_color='black', border_thickness=4)

                self.update_status_text("DRONE STATUS= Ready to take off in autopilot mode (press 'g')")
                return path
            except nx.NetworkXNoPath:
                self.update_status_text("DRONE STATUS= No path found. Manual Control may be required")
                return None


    def autopilot_mode(self):
        current_drone = self.drones[self.current_drone_index]
        if not current_drone.path:
            self.update_status_text("No path to follow. Please calculate the path first (press 'f').")
            return

        self.update_status_text(f"Automatic Pilot: {current_drone.name} following pre-calculated path. Press 'p' to toggle pause/resume.")
        steps = 0

        for i in range(len(current_drone.path) - 1):
            current_pos = current_drone.path[i]
            next_pos = current_drone.path[i + 1]

            # Determine the direction to turn
            if next_pos[1] > current_pos[1]:  # Moving up
                current_drone.turtle.penup()  # Ensure the pen is up before moving
                current_drone.turtle.setheading(270)
            elif next_pos[1] < current_pos[1]:  # Moving down
                current_drone.turtle.penup()  # Ensure the pen is up before moving
                current_drone.turtle.setheading(90)
            elif next_pos[0] > current_pos[0]:  # Moving right
                current_drone.turtle.penup()  # Ensure the pen is up before moving
                current_drone.turtle.setheading(0)
            elif next_pos[0] < current_pos[0]:  # Moving left
                current_drone.turtle.penup()  # Ensure the pen is up before moving
                current_drone.turtle.setheading(180)

            current_drone.turtle.goto(next_pos[0] + 0.5, self.rows - next_pos[1] - 0.5)
            self.screen.update()
            turtle.time.sleep(0.5)
            steps += 1

        # Final update to reach the end position
        end_pos = current_drone.path[-1]
        current_drone.turtle.goto(end_pos[0] + 0.5, self.rows - end_pos[1] - 0.5)
        self.screen.update()

        self.update_status_text(f"Automatic Pilot: {current_drone.name} reached destination {end_pos} in {steps} steps. Press 'c' to continue.")
    def pause_mode(self):
        # help to pause # clemens section to do 
        pass

    def hide_path(self):
        # help to hide it
        self.circle.hideturtle()

    def quit_program(self):
        # quit the program
        turtle.bye()

    def continueProgram(self):
        self.draw_map()
        self.screen.update()
        self.update_status_text('Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)')
         
    def reset(self):
        # help to reset to starting position, almost correct now
        self.draw_map()
        self.update_status_text('Program Resetted. Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path) ')
        self.screen.update()

