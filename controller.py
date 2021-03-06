import sys

import pygame
from pygame import event

from model import Model
from view import View


class Controller:
    def __init__(self):
        pygame.init()
        self.model = Model.getInstance()
        self.view = View()

        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)

        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)

    def playGame(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.model.gameStep()
                    # self.view.play_flap_sound()

                if event.type == self.SPAWNPIPE:
                    self.model.extendPipes()

                if event.type == self.BIRDFLAP:
                    self.model.updateBirdIndex()

                self.model.set_current_event(event.type)
                self.view.play_flap_sound()

            self.view.showBG()
            self.model.f1()
            self.view.f1()


            # todo!!!
            # Floor
            self.model.floor_x_pos -= 1
            self.view.draw_floor()
            if self.model.floor_x_pos <= -576:
                self.model.floor_x_pos = 0

            pygame.display.update()
            self.model.clock.tick(100)


if __name__ == '__main__':
    controller = Controller()
    controller.playGame()