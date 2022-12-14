import datetime

import pygame, sys, os
from datafile import *
from pygame.locals import *
import pygame.mixer
from turtle import *
from stretching import *
import math


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption('거북목 방지 게임') #화면 타이틀
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

        self.gameScore = 100 #초기 점수

        # 스프라이트 시트에서 이미지 로드
        self.spriteSheet_player = SpriteSheet('spriteSheet1.png', 16, 16, 8, 8, 12)
        self.spriteSheet_background = SpriteSheet('spriteSheet2.png', 8, 8, 16, 16, 87)

        self.spr_player = {}
        self.spr_player['stay'] = self.spriteSheet_player.createSpriteSet([0])
        self.spr_player['addScore'] = self.spriteSheet_player.createSpriteSet([9, 10, 11])
        self.spr_player['subScore'] = self.spriteSheet_player.createSpriteSet([9, 10, 11])

        self.background = createBackImage(self.spriteSheet_background)

        #self.player_rect = pygame.Rect((TILE_MAPiSIZE[0] * 4, TILE_MAPSIZE[1] * 4 - 14), (6, 14)) # 플레이어 화면에서 고정
        self.player_movement = [0, 0]
        self.player_vspeed = 0 # y 가속도
        self.player_flytime = 0 # 공중에 뜬 시간

        self.player_action = 'stay'
        self.player_frame = 0
        self.player_frameSpeed = 1
        self.player_frameTimer = 0
        self.player_animationMode = True #애니메이션 모드 (한번만)

        # 게임 구동
        self.run()

    def run(self):
        while True:
            self.screen.fill(BACKGROUND_COLOR) #화면 초기화

            self.screen.blit(self.background, (0, 0))

            self.screen.blit(self.spriteSheet_player.spr[0], (320, 240))
            # self.screen.blit(self.spriteSheet_enemy.spr[0], (320, 240))



        # 플레이어
            self.player_movement = [0, 0]
            self.player_movement[1] += self.player_vspeed

            self.player_vspeed += 0.2
            if self.player_vspeed > 3:
                self.player_vspeed = 3

            draw_text(self.screen, "SCORE: " + str(self.gameScore), 8, (238, 238, 230), 200, 140)

        # 적
        #     self.enemy_movement = [0, 0]
        #     self.enemy_movement[1] += self.player_vspeed
        #
        #     self.enemy_vspeed += 0.2
        #     if self.enemy_vspeed > 3:
        #         self.enemy_vspeed = 3

            #자세에 따른 어드벤티지
            minus = math.trunc(minustime)

            # #자세 상태 출력
            # text_color = 255, 255, 255
            # font = pygame.font.SysFont("arial", 30, True, True)
            # text = font.render(twist, True, text_color)
            #
            # self.screen.bilt(text, (100, 100))

        # 이벤트
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.K_1:
                    self.gameScore -= minus

                #if event.type == # 좋은 자세
                #   self.gameScore += 5

            surf = pygame.transform.scale(self.screen, WINDOW_SIZE) # 윈도우 창모드
            self.screen.blit(surf, (0, 0))

            # img = pygame.surfarray.make_surface(image)
            # self.screen.blit(img, (0, 0))

            pygame.display.update()
            self.clock.tick(60) # 60프레임 제한



game = Game() # 게임 실행
