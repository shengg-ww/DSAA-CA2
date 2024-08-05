from drone import BaseDrone
import random
import turtle
import time

#1: Implement multi drone coordination with independent end points
# 2: Random Event Generator (e.g Hurricane )



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
        weather=['Hurricane']
        self.weather_condition = random.choice(weather)
        self.is_weather= not self.is_weather
        if self.is_weather:
                self.update_status_text(f'{self.weather_condition} has been applied')
                if self.weather_condition == 'Rainy':
                    self.draw_rain()
                elif self.weather_condition == 'Hurricane':
                    self.draw_hurricane()

        # Schedule the next weather randomization
        next_duration = random.randint(10000, 30000)  # Random duration between 5 and 15 seconds in milliseconds
        if next_duration<10000:
            self.update_status_test('Hurricane is clearing up...')
        self.screen.ontimer(self.weather_randomizer, next_duration)

    def disable_weather(self):
        self.draw_map()
        self.screen.update()
        self.update_status_text('Weather Randmonizer has been disabled')

    def draw_hurricane(self):
        # Define a central point for the hurricane
        center_x = random.randint(1, self.cols - 2)
        center_y = random.randint(1, self.rows - 2)
        radius = 3  # Radius around the central point

        player_position = self.get_current_position()

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                new_x = center_x + dx
                new_y = center_y + dy
                if (0 <= new_x < self.cols and 0 <= new_y < self.rows and
                    self.city_map[new_y][new_x] == '.' and (new_x, new_y) != player_position): 
                    self.affected_cells.add((new_x, new_y))  # Add to the set of affected cells to disable autopilot
                    self.draw_spiral(new_x, self.rows - new_y - 1)
                   
    # Set a timer to clear the hurricane after a random duration
        duration = random.randint(5000, 15000)  # Random duration between 5 and 15 seconds in milliseconds
        self.screen.ontimer(self.clear_hurricane, duration)

    def clear_hurricane(self):
        self.continueProgram()
        self.screen.update()
        self.affected_cells.clear()
        self.update_status_text('Hurricane has passed')


   

    def draw_rain(self):
        pass

