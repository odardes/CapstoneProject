from gui import gui
from Car.car import *
from gui import car, screen, pygame_clock, instructions_list
from config import *

pygame.init()
pygame.display.set_caption("Car Simulation")

# Draw grid to represent distance, every grid is 10 cm apart
def drawGrid(surface):
    gap = config.DISPLAY_WIDTH // config.ROWS
    x = 0
    y = 0
    for i in range(config.ROWS):
        x += gap
        y += gap
        pygame.draw.line(surface, config.WHITE, (x, 0), (x, config.DISPLAY_WIDTH))
        pygame.draw.line(surface, config.WHITE, (0, y), (config.DISPLAY_WIDTH, y))

img = pygame.image.load("Images/gray_car.png")

def main_loop():
    # Draws the car on start
    car.img = pygame.transform.rotate(car.img, 0)

    close_button = False
    while not close_button:
        """
        Render and update the GUI part using the non-blocking .update() method instead of
        the blocking .mainloop() function, so that Tkinter can be rendered simultaneously with pygame,
        the try-except block is just there so that an error message doesn't get outputted to the console
        when the program is ended
        """
        try:
            gui.update()
        except Exception:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_button = True
                break

        screen.fill(config.BLACK)
        if len(instructions_list) > 0 and car.target == float("inf") and abs(car.smoothing_angle) >= abs(math.degrees(instructions_list[0][1])) + abs(car.prev_angle):
            car.updateValue(instructions_list[0][0], instructions_list[0][1], instructions_list[0][2])
            print(car)

        if len(instructions_list) > 0 and car.x_velocity == 0 and car.y_velocity == 0:
            print(car.smoothing_angle, -math.degrees(instructions_list[0][1]) - car.prev_angle)
            car.smoothing_angle += -math.degrees(car.angle)
            if math.degrees(instructions_list[0][1]) > 0 and car.prev_angle >= 0 and car.smoothing_angle > -math.degrees(instructions_list[0][1]) - (car.prev_angle):
                car.smoothing_angle -= 2
                car.img = pygame.transform.rotate(pygame.transform.scale(img, (200, 100)), car.smoothing_angle)
            if math.degrees(instructions_list[0][1]) < 0 and car.prev_angle <= 0 and car.smoothing_angle < -math.degrees(instructions_list[0][1]) - (car.prev_angle):
                car.smoothing_angle += 2
                car.img = pygame.transform.rotate(pygame.transform.scale(img, (200, 100)), car.smoothing_angle)

        car.render()
        # Writes the new values on the console when the car reaches where it
        # needs to reach and move according to new entry.
        if len(instructions_list) > 0 and abs(car.smoothing_angle) >= abs(math.degrees(instructions_list[0][1])) + abs(car.prev_angle):
            car.move()

        if car.has_reached_target() and len(instructions_list) > 0 and abs(car.smoothing_angle) >= abs(math.degrees(instructions_list[0][1]) + abs(car.prev_angle)):
            # removes the executed instruction and reset the car value
            instructions_list.pop(0)
            car.updateValue(0, 0, float("inf"))
            car.smoothing_angle = 0
            car.prev_angle = math.degrees(car.angle)
            print("Switching direction and speed")

        # Moves the car and drawing the movement paths
        if not(car.x_velocity == 0  and car.y_velocity == 0):
            car.paths.append((car.x + car.img.get_width()/2, car.y + car.img.get_height()/2))
        [pygame.draw.circle(screen, (255, 0, 0), x, 2) for x in car.paths]


        # Draws the grids on the screen
        drawGrid(screen)

        pygame.display.update()
        pygame.display.flip()

        # Time.deltatime
        pygame_clock.tick(config.FPS)

if __name__ == '__main__':
    main_loop()
