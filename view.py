import pygame

from model import Model


class View:
    def __init__(self):
        self.model = Model.getInstance()
        self.screen = pygame.display.set_mode((576, 1024))

    def showBG(self):
        self.screen.blit(self.model.bg_surface, (0, 0))

    def f1(self):
        if self.model.game_active:
            # Bird
            self.screen.blit(self.model.rotated_bird, self.model.bird_rect)

            # Pipes
            self.draw_pipes(self.model.pipe_list)

            # Score
            self.score_display('main_game')
        else:
            self.screen.blit(self.model.game_over_surface, self.model.game_over_rect)
            self.score_display('game_over')

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                self.screen.blit(self.model.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.model.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def score_display(self, game_state):
        if game_state == 'main_game':
            self.model.score_surface = self.model.game_font.render(str(int(self.model.score)), True, (255, 255, 255))
            self.model.score_rect = self.model.score_surface.get_rect(center=(288, 100))
            self.screen.blit(self.model.score_surface, self.model.score_rect)
        if game_state == 'game_over':
            self.model.score_surface = self.model.game_font.render(f'Score: {int(self.model.score)}', True, (255, 255, 255))
            self.model.score_rect = self.model.score_surface.get_rect(center=(288, 100))
            self.screen.blit(self.model.score_surface, self.model.score_rect)

            self.model.high_score_surface = self.model.game_font.render(f'High score: {int(self.model.high_score)}', True, (255, 255, 255))
            self.model.high_score_rect = self.model.high_score_surface.get_rect(center=(288, 850))
            self.screen.blit(self.model.high_score_surface, self.model.high_score_rect)