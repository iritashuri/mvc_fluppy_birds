import random

import pygame


class Model:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Model.__instance is None:
            Model()
        return Model.__instance

    def __init__(self):
        if Model.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.init()
            Model.__instance = self

    def init(self):
        pygame.init()
        self.can_score = True
        self.game_active = True
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('04B_19.ttf', 40)
        self.initBG()
        self.initFloor()
        self.initBird()
        self.initPipes()
        self.initGameOver()
        self.initSounds()

    def initBG(self):
        # Background definition
        self.bg_surface = pygame.image.load('assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale2x(self.bg_surface)

    def initFloor(self):
        # Floor definition
        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)
        self.floor_x_pos = 0

    def initBird(self):
        # Bird definition
        self.bird_downflap = pygame.transform.scale2x(
            pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(
            pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(100, 512))

    def initPipes(self):
        # Pipes definition
        self.pipe_surface = pygame.image.load('assets/pipe-green.png')
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_list = []
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
        self.pipe_height = [400, 600, 800]

    def initSounds(self):
        # Sounds definition
        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
        self.score_sound_countdown = 100
        self.SCOREEVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SCOREEVENT, 100)

    def initGameOver(self):
        # Game Over definition
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(288, 512))

    def gameStep(self):
        if self.game_active:
            self.bird_movement = 0
            self.bird_movement -= 8
        # flap_sound.play()
        else:
            self.game_active = True
            self.pipe_list.clear()
            self.bird_rect.center = (100, 512)
            self.bird_movement = 0
            self.score = 0

    def extendPipes(self):
        self.pipe_list.extend(self.create_pipe())

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(700, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 350))
        return bottom_pipe, top_pipe

    def updateBirdIndex(self):
        if self.bird_index < 2:
            self.bird_index += 1
        else:
            self.bird_index = 0

        self.bird_surface, self.bird_rect = self.bird_animation()

    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, self.bird_rect.centery))
        return new_bird, new_bird_rect

    def f1(self):
        if self.game_active:
            # Bird
            self.bird_movement += self.gravity
            self.rotated_bird = self.rotate_bird(self.bird_surface)
            self.bird_rect.centery += self.bird_movement
            self.game_active = self.check_collision(self.pipe_list)

            # Pipes
            self.pipe_list = self.move_pipes(self.pipe_list)
            ## self.draw_pipes(self.pipe_list)

            # Score
            self.pipe_score_check()
        else:
            self.high_score = self.update_score(self.score, self.high_score)

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 3, 1)
        return new_bird

    def check_collision(self, pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                # self.death_sound.play()
                self.can_score = True
                return False

        if self.bird_rect.top <= -150 or self.bird_rect.bottom >= 850:
            self.can_score = True
            return False

        return True

    def move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
        return visible_pipes

    def update_score(self, score, high_score):
        if score > high_score:
            high_score = score
        return high_score

    def pipe_score_check(self):
        global score, can_score

        if self.pipe_list:
            for pipe in self.pipe_list:
                if 95 < pipe.centerx < 105 and can_score:
                    score += 1
                    # score_sound.play()
                    can_score = False
                if pipe.centerx < 0:
                    can_score = True