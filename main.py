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
        self.rect.center += self.vel_vector*6




    def data(self):
        radars = self.radars
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            input[i] = int(radar[1])
        return input

def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)



def eval_genomes(genomes, config):
    global cars, ge, nets
  

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(TRACK, (0, 0))

        for i, car in enumerate(cars):
            print(car.sprite.data())
            output = nets[i].activate(car.sprite.data())
            #print(output)
            if output[0] > 0.7:
                car.sprite.direction = -1
            if output[1] > 0.7:
                car.sprite.direction = 1
            if output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0
                
                
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




if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
