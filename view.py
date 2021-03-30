import pygame

from model import Model


class View:
    def __init__(self):
        self.model = Model.getInstance()

    def showBG(self):
        self.model.screen.blit(self.model.bg_surface, (0, 0))

    def f1(self):
        if self.model.game_active:
            # Bird
            self.model.screen.blit(self.model.rotated_bird, self.model.bird_rect)

            # Pipes
            self.draw_pipes(self.model.pipe_list)

            # Score
            self.score_display('main_game')

            if self.model.score_played == False:
                self.model.get_score_played().play()
        else:
            if self.model.game_over_played == False:
                self.model.get_death_sound().play()

            self.model.screen.blit(self.model.game_over_surface, self.model.game_over_rect)
            self.score_display('game_over')

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                self.model.screen.blit(self.model.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.model.pipe_surface, False, True)
                self.model.screen.blit(flip_pipe, pipe)

    def score_display(self, game_state):
        if game_state == 'main_game':
            self.model.score_surface = self.model.game_font.render(str(int(self.model.score)), True, (255, 255, 255))
            self.model.score_rect = self.model.score_surface.get_rect(center=(288, 100))
            self.model.screen.blit(self.model.score_surface, self.model.score_rect)
        if game_state == 'game_over':
            self.model.score_surface = self.model.game_font.render(f'Score: {int(self.model.score)}', True,
                                                                   (255, 255, 255))
            self.model.score_rect = self.model.score_surface.get_rect(center=(288, 100))
            self.model.screen.blit(self.model.score_surface, self.model.score_rect)

            self.model.high_score_surface = self.model.game_font.render(f'High score: {int(self.model.high_score)}',
                                                                        True, (255, 255, 255))
            self.model.high_score_rect = self.model.high_score_surface.get_rect(center=(288, 850))
            self.model.screen.blit(self.model.high_score_surface, self.model.high_score_rect)

    def draw_floor(self):
        self.model.screen.blit(self.model.floor_surface, (self.model.floor_x_pos, 900))
        self.model.screen.blit(self.model.floor_surface, (self.model.floor_x_pos + 576, 900))

    def play_flap_sound(self):
        if self.model.game_active and self.model.event_type == pygame.KEYDOWN:
            self.model.flap_sound.play()






