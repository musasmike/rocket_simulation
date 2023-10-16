# Importing the necessary packages
import pygame
import math

# Initializing pygame
pygame.init()

WIDTH, HEIGHT = 800, 600  # The width and height of the canvas
# Setting up the UI interface with width and height
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

PLANET_MASS = 100  # planet mass
SHIP_MASS = 5  # ship mass
G = 5  # gravitational constant, the force of gravity
FPS = 60  # Frame per Second
PLANET_SIZE = 50  # radius of the planet
OBJ_SIZE = 5  # radius of the ship
VEL_SCALE = 100  # scale of the velocity

# loads the background image
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
# loads the planet image
PLANET = pygame.transform.scale(pygame.image.load("mars.png"), (PLANET_SIZE, PLANET_SIZE))
# load the second planet image
PLANET_2 = pygame.transform.scale(pygame.image.load("neptune.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

# The colors used
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Planet:
    """
    The Planet class draws the planet on the interface by defining
    the x and y coordinates, and the mass of the planet
    """
    def __init__(self, x, y, mass, planet_choice):
        self.x = x
        self.y = y
        self.mass = mass
        self.planet_choice = planet_choice

    # Draws the planet
    def draw(self):
        win.blit(self.planet_choice, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))


class Spacecraft:
    """
    The Spacecraft class draws and move the spacecraft by using x and y coordinates,
    x and y velocities, and the mass of the ship. The ship is represented as a red
    dot.
    """
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet=None):
        """
        This method calculates the distance between the spacecraft and the planet,
        the gravity force between them, the accelerations, and angle.
        :param planet:
        :return: the speed and direction of the spacecraft and how it's moving.
        """
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance ** 2

        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    # Draws the spacecraft
    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)


def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj


def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS, PLANET)
    planet_2 = Planet(WIDTH // 4, HEIGHT // 4, 110, PLANET_2)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)  # regulate the speed

        mouse_pos = pygame.mouse.get_pos()
        # Loops through different events such as clicking, ...
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))  # Draws the image

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            obj.move(planet_2)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_SIZE
            collided_2 = math.sqrt((obj.x - planet_2.x) ** 2 + (obj.y - planet_2.y) ** 2) <= PLANET_SIZE
            if off_screen or collided or collided_2:
                objects.remove(obj)

        planet.draw()
        planet_2.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
