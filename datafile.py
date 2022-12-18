import pygame, os, random

DIR_IMAGE = 'img'
DIR_FONT = 'font'

WINDOW_SIZE = (960, 640)
TILE_SIZE = 8
TILE_BACKGROUNDSIZE = (int(WINDOW_SIZE[0] / 7.5), int(WINDOW_SIZE[1] / 20))
BACKGROUND_COLOR = (27, 25, 25)
DEAFAULT_FONT_NAME = "a인생책방T.ttf"

# 스프라이트 시트 클래스
class SpriteSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()
        self.spr = []
        self.width = width
        self.height = height

        for i in range(max_index):  # 스프라이트 시트의 각 인덱스에 자른 이미지 저장
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0),
                       ((i % max_row) * width, (i // max_col) * height, width, height))
            image.set_colorkey((0, 0, 0))
            self.spr.append(image)

    # 스프라이트 세트 생성 함수
    def createSpriteSet(self, index_list, index_max = None):
        spr = []

        if index_max == None:
            for index in index_list:
                spr.append(self.spr[index])
        else:
            for index in range(index_list, index_max + 1):
                spr.append(self.spr[index])
        return spr

#텍스트 드로우 함수
def draw_text(screen, text, size, color, x, y):
    gameFont = pygame.font.Font(os.path.join(DIR_FONT, DEAFAULT_FONT_NAME), size)
    text_surface = gameFont.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (round(x), round(y))
    screen.blit(text_surface, text_rect)

# 기본 오브젝트 클래스
class BaseObject:
    def __init__(self, spr, coord, kinds, game):
        self.kinds = kinds
        self.spr = spr
        self.spr_index = 0
        self.game = game
        self.width = spr[0].get_width()
        self.height = spr[0].get_height()
        self.direction = True
        self.vspeed = 0
        self.gravity = 0.2
        self.movement = [0, 0]
        self.rect = pygame.rect.Rect(coord[0], coord[1], self.width, self.height)
        self.frameSpeed = 0
        self.frameTimer = 0

    def physics(self):
        self.movement[0] = 0
        self.movement[1] = 0

        if self.gravity != 0:
            self.movement[1] += self.vspeed

            self.vspeed += self.gravity
            if self.vspeed > 3:
                self.vspeed = 3

    def draw(self):
        self.game.screen_scaled.blit(pygame.transform.flip(self.spr[self.spr_index], self.direction, False)
                                     , (self.rect.x - self.game.camera_scroll[0],
                                        self.rect.y - self.game.camera_scroll[1]))

        if self.kinds == 'enemy' and self.hp < self.hpm:
            pygame.draw.rect(self.game.screen_scaled, (131, 133, 131)
                             , [self.rect.x - 1 - self.game.camera_scroll[0],
                                self.rect.y - 5 - self.game.camera_scroll[1], 10, 2])
            pygame.draw.rect(self.game.screen_scaled, (189, 76, 49)
                             , [self.rect.x - 1 - self.game.camera_scroll[0],
                                self.rect.y - 5 - self.game.camera_scroll[1], 10 * self.hp / self.hpm, 2])

    def animation(self, mode):
        if mode == 'loop':
            self.frameTimer += 1

            if self.frameTimer >= self.frameSpeed:
                self.frameTimer = 0
                if self.spr_index < len(self.spr) - 1:
                    self.spr_index += 1
                else:
                    self.spr_index = 0

# 배경 이미지 생성함수
def createBackImage(tileSpr):
    image = pygame.Surface((int(WINDOW_SIZE[0] / 2), int(WINDOW_SIZE[1] / 12)))
    for row in range(16):
        for col in range(4):
            star_case = random.randrange(-(col + 2), 3)
            if star_case >= 0:
                image.blit(tileSpr.spr[random.randrange(0, 31)]
                           , (row * TILE_SIZE * 2 + random.randrange(-4, 5)
                            , col * TILE_SIZE * 2 + random.randrange(-4, 5)))
    image.blit(tileSpr.spr[31], (24 * TILE_SIZE, 2 * TILE_SIZE))
    image.blit(tileSpr.spr[32], (25 * TILE_SIZE, 2 * TILE_SIZE))
    image.blit(tileSpr.spr[33], (24 * TILE_SIZE, 3 * TILE_SIZE))
    image.blit(tileSpr.spr[34], (25 * TILE_SIZE, 3 * TILE_SIZE))
    image.set_colorkey((0, 0, 0))
    return image

# 애니메이션 행동 변경 함수
def change_playerAction(frame, action_var, new_var, frameSpd, new_frameSpd, aniMode, new_aniMode):
    if action_var != new_var:
        action_var = new_var
        frame = 0
        frameSpd = new_frameSpd
        aniMode = new_aniMode
    return frame, action_var, frameSpd, aniMode