# special_control.py

from drone import BaseDrone
from DroneLinkedList import DroneLinkedList
import random
import turtle


class SpecialControl(BaseDrone):
    def __init__(self, name, start_pos, target_pos, color, screen):
        super().__init__(name, start_pos, target_pos, color, screen)
        self.drones = DroneLinkedList()
        self.drones.append(self)  # Add the initial drone (self) to the linked list

    def delete_drone(self):
        current_drone_node = self.drones.current
        if current_drone_node and current_drone_node != self.drones.head:
            removed_drone = current_drone_node.drone
            
            # Remove the end point 'e' from the city map
            if removed_drone.target_pos:
                prev_x, prev_y = removed_drone.target_pos
                if self.city_map[prev_y][prev_x] == 'e':
                    self.city_map[prev_y] = self.city_map[prev_y][:prev_x] + '.' + self.city_map[prev_y][prev_x + 1:]

            self.drones.delete(current_drone_node)
            removed_drone.turtle.hideturtle()
            self.update_status_text(f'Deleted Drone {removed_drone.name}')
            self.screen.update()
        elif current_drone_node == self.drones.head:
            self.update_status_text('Cannot delete the Original Drone.')
        else:
            self.update_status_text('Cannot delete the last remaining drone.')

    def add_drone(self):
        new_drone = BaseDrone(
            name=f"Drone {len(self.drones) + 1}",
            start_pos=self.start_pos,
            target_pos=None,
            color="purple",
            screen=self.screen
        )
        self.drones.append(new_drone)
        self.update_status_text(f"Added new drone: {new_drone.name}")

    def switch_drone(self):
        self.drones.switch_to_next()
        current_drone = self.drones.get_current_drone()
        if current_drone:
            self.update_status_text(f"Switched control to: {current_drone.name}")

    def choose_end(self, x, y):
        if self.drones.current == self.drones.head:
            self.update_status_text("Cannot set end point for the first drone.")
            return

        grid_x = int(x)
        grid_y = self.rows - int(y) - 1

        if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
            if self.city_map[grid_y][grid_x] == 'X':
                self.update_status_text(f"Cannot set end point on an obstacle at: ({grid_x}, {grid_y})")
                return

            current_drone = self.drones.get_current_drone()
            if current_drone.target_pos:
                prev_x, prev_y = current_drone.target_pos
                if self.city_map[prev_y][prev_x] == 'e':
                    self.city_map[prev_y] = self.city_map[prev_y][:prev_x] + '.' + self.city_map[prev_y][prev_x + 1:]

            self.city_map[grid_y] = self.city_map[grid_y][:grid_x] + 'e' + self.city_map[grid_y][grid_x + 1:]
            current_drone.target_pos = (grid_x, grid_y)
            self.draw_map()
            self.screen.update()

    def weather_randomizer(self):
        weather = ['Hurricane']
        self.weather_condition = random.choice(weather)
        self.is_weather = not self.is_weather
        if self.is_weather:
            self.update_status_text(f'{self.weather_condition} has been applied')
            if self.weather_condition == 'Rainy':
                self.draw_rain()
            elif self.weather_condition == 'Hurricane':
                self.draw_hurricane()

        next_duration = random.randint(10000, 30000)
        if next_duration < 10000:
            self.update_status_text('Hurricane is clearing up...')
        self.screen.ontimer(self.weather_randomizer, next_duration)

    def disable_weather(self):
        self.draw_map()
        self.screen.update()
        self.update_status_text('Weather Randomizer has been disabled')

    def draw_hurricane(self):
        center_x = random.randint(1, self.cols - 2)
        center_y = random.randint(1, self.rows - 2)
        radius = 3

        player_position = self.get_current_position()

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                new_x = center_x + dx
                new_y = center_y + dy
                if (0 <= new_x < self.cols and 0 <= new_y < self.rows and
                        self.city_map[new_y][new_x] == '.' and (new_x, new_y) != player_position):
                    self.affected_cells.add((new_x, new_y))
                    self.draw_spiral(new_x, self.rows - new_y - 1)

        duration = random.randint(5000, 15000)
        self.screen.ontimer(self.clear_hurricane, duration)

    def clear_hurricane(self):
        self.continue_program()
        self.screen.update()
        self.affected_cells.clear()
        self.update_status_text('Hurricane has passed')

    def draw_rain(self):
        pass