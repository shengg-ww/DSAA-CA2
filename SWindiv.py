from drone import BaseDrone
import random
import turtle

#1: Implement multi drone coordination with independent end points
# 2: Random Event Generator (e.g Rain, Flood, Fog )
# rain slows down drone, flood makes certain areas completely unavailable (requires rerouting), fog reduces visibility
# making pathfinding sluggish and disable autopilot (if u choose to navigate through), also randomly change the endpoint


class SpecialControl(BaseDrone):
    def __init__(self, name, start_pos, target_pos, color, screen):
        # overwrites BaseDrone
        super().__init__(name, start_pos,target_pos, color, screen)
        self.target_pos = target_pos
    
    def delete_drone(self):
        if len(self.drones) > 1:
            removed_drone = self.drones.pop()
            removed_drone.turtle.hideturtle()  # Hide the turtle shape
            self.update_status_text(f'Deleted Drone {removed_drone.name}')
        else:
            self.update_status_text('Cannot delete the last remaining drone.')


    def add_drone(self):
        new_drone = SpecialControl(
            name=f"Drone {len(self.drones)+1}",
            start_pos=(self.start_pos),
            target_pos=None,
            color="purple",
            screen=self.screen
        )
        self.drones.append(new_drone)
        self.update_status_text(f"Added new drone: {new_drone.name}")

    def switch_drone(self):
        self.current_drone_index = (self.current_drone_index + 1) % len(self.drones)
        self.update_status_text(f"Switched control to: {self.drones[self.current_drone_index].name}")

    def choose_end(self, x, y):
        # Prevent end point selection for drone at index 0
        if self.current_drone_index == 0:
            self.update_status_text("Cannot set end point for the first drone.")
            return


        # Convert screen coordinates to grid coordinates
        grid_x = int(x)
        grid_y = self.rows - int(y) - 1

        if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
            # Check if the selected tile is an obstacle
            if self.city_map[grid_y][grid_x] == 'X':
                self.update_status_text(f"Cannot set end point on an obstacle at: ({grid_x}, {grid_y})")
                return

            # Remove the existing end point 'e' if it belongs to the current drone
            current_drone = self.drones[self.current_drone_index]
            if current_drone.target_pos:
                prev_x, prev_y = map(int, current_drone.target_pos)
                if self.city_map[prev_y][prev_x] == 'e':
                    self.city_map[prev_y] = self.city_map[prev_y][:prev_x] + '.' + self.city_map[prev_y][prev_x + 1:]


            # Set the new end point
            self.city_map[grid_y] = self.city_map[grid_y][:grid_x] + 'e' + self.city_map[grid_y][grid_x + 1:]

            # Set the end point for the current drone
            current_drone.target_pos = (grid_x, grid_y)
            
            # Redraw the map
            self.draw_map()
            self.screen.update()

    def weather_randomizer(self):
            # Existing implementation
            weather=['Snow','Rain','Hurricane']
            self.weather_condition = random.choice(weather)
            self.apply_weather_effect()
    

    def apply_weather_effect(self):
        self.update_status_text(f'{self.weather_condition} has been applied')
       
        if self.weather_condition == 'Rainy':
            self.draw_rain()
        elif self.weather_condition == 'Hurricane':
            self.draw_hurricane()

    def draw_hurricane(self):
        hurricane_turtle = turtle.Turtle()
        hurricane_turtle.hideturtle()
        hurricane_turtle.penup()
        hurricane_turtle.speed(0)
        hurricane_turtle.color('white')
    
    def draw_rain(self):
        pass
