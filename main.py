import pygame
import os
import random
import math
import sys
import neat

pygame.init()

SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 1016

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TRACK = pygame.image.load(os.path.join("Assets", "track.png"))


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets", "oldcar.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(490, 820))
        self.center = self.rect.center
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []

    def update(self, screen):
        self.radars.clear()
        self.rotate(screen)
        self.drive()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(SCREEN, radar_angle)
        self.data()
        self.collision(screen)

    def drive(self):
        self.rect.center += self.vel_vector * 6

    def collision(self, screen):
        len = 40
        collision_point_right = [
            int(
                self.rect.center[0]
                + math.cos(math.radians(360 + 18 - self.angle)) * len
            ),
            int(
                self.rect.center[1]
                + math.sin(math.radians(360 + 18 - self.angle)) * len
            ),
        ]
        collision_point_left = [
            int(
                self.rect.center[0]
                + math.cos(math.radians(360 - 18 - self.angle)) * len
            ),
            int(
                self.rect.center[1]
                + math.sin(math.radians(360 - 18 - self.angle)) * len
            ),
        ]

        if screen.get_at(collision_point_right) == pygame.Color(
            2, 105, 31, 255
        ) or screen.get_at(collision_point_left) == pygame.Color(2, 105, 31, 255):
            self.alive = False
            print("collision")

        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_left, 4)

    def rotate(self, screen):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def data(self):
        radars = self.radars
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            input[i] = int(radar[1])
        return input


def eval_genomes(genomes, config):
    global cars, ge, nets

    clock = pygame.time.Clock()

    cars = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        SCREEN.blit(TRACK, (0, 0))

        for car in cars:
            car.update(SCREEN)
            car.draw(SCREEN)

        if len(cars) == 0:
            break

        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if not car.sprite.alive:
                remove(i)

        clock.tick(30)
        pygame.display.update()


def run(config_path):
    global pop

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
