import turtle
import networkx as nx

class ProgramControl:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()

        self.status_turtle = turtle.Turtle()
        self.status_turtle.speed(0)
        self.status_turtle.hideturtle()
        

    def update_status_text(self, text):
        self.status_turtle.clear()
        self.status_turtle.penup()
        self.status_turtle.goto(self.cols / 2, self.rows + 0.5)
        self.status_turtle.write(text, align="center", font=("Arial", 12, "normal"))
        self.screen.update()

    def draw_circle(self, x, y, letter=None, color='yellow', border_color='black', border_thickness=2):
        self.turtle.penup()
        self.turtle.goto(x + 0.5, y + 0.25)
        self.turtle.pendown()
        self.turtle.pensize(border_thickness)
        self.turtle.fillcolor(color)
        self.turtle.begin_fill()
        self.turtle.pencolor(border_color)
        self.turtle.circle(0.3)
        self.turtle.end_fill()
        if letter:
            self.turtle.penup()
            self.turtle.goto(x + 0.5, y + 0.3)
            self.turtle.pendown()
            self.turtle.color("black")
            self.turtle.write(letter, align="center", font=("Arial", 24, "bold"))
        self.turtle.pensize(1)  # Reset pen size

    def calculate_shortest_path(self):

        start = self.get_current_position()
        end = None

        for y in range(self.rows):
            for x in range(self.cols):
                if self.city_map[y][x] == 'e':
                    end = (x, y)

        if start and end:
            G = nx.grid_2d_graph(self.rows, self.cols)
            
            # Remove nodes that are obstacles
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.city_map[y][x] == 'X':
                        G.remove_node((y, x))

            # Use Dijkstra's algorithm to find the shortest path
            try:
                path = nx.shortest_path(G, source=(start[1], start[0]), target=(end[1], end[0]), weight=None, method='dijkstra')
                # Convert the path back to the format (x, y)
                self.path = [(x, y) for y, x in path]
                
                for node in self.path:
                    self.draw_circle(node[0], self.rows - node[1] - 1, color='yellow', border_color='black', border_thickness=4)
                
                self.update_status_text("DRONE STATUS= Ready to take off in autopilot mode (press 'g')")
                return path
            except nx.NetworkXNoPath:
                self.update_status_text("DRONE STATUS= No path found")
                return None
            
    def autopilot_mode(self):
        if not self.path:
            self.update_status_text("No path to follow. Please calculate the path first (press 'f').")
            return

        self.update_status_text("Automatic Pilot: Following pre-calculated path. Press 'p' to toggle pause/resume.")
        steps = 0
        for i in range(len(self.path) - 1):
            current_pos = self.path[i]
            next_pos = self.path[i + 1]

            # Determine the direction to turn
            if next_pos[1] > current_pos[1]:  # Moving up
                self.player.setheading(270)
            elif next_pos[1] < current_pos[1]:  # Moving down
                self.player.setheading(90)
            elif next_pos[0] > current_pos[0]:  # Moving right
                self.player.setheading(0)
            elif next_pos[0] < current_pos[0]:  # Moving left
                self.player.setheading(180)

            self.player.goto(next_pos[0] + 0.5, self.rows - next_pos[1] - 0.5)
            self.screen.update()
            turtle.time.sleep(0.5)  
            steps += 1

        # Final update to reach the end position
        end_pos = self.path[-1]
        self.player.goto(end_pos[0] + 0.5, self.rows - end_pos[1] - 0.5)
        self.screen.update()
        
        self.update_status_text(f"Automatic Pilot: Destination {end_pos} reached in {steps} steps. Press 'c' to continue.")
    
    def pause_mode(self):
        pass

    def hide_path(self):
        if self.path:
            self.draw_map()  # Redraw the map without the path
            self.path = []  # Clear the stored path

    def quit_program(self):
        pass

    def reset(self):
        pass