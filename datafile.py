import pygame, os, random

DIR_PATH = os.path.dirname(__file__) # 파일 위치
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_FONT = os.path.join(DIR_PATH, 'font')

WINDOW_SIZE = (960, 640)
TILE_SIZE = 8
TILE_BACKGROUNDSIZE = (int(WINDOW_SIZE[0] / 7.5), int(WINDOW_SIZE[1] / 20))
BACKGROUND_COLOR = (27, 25, 25)
DEAFAULT_FONT_NAME = "a인생책방T.ttf"

# 스프라이트 시트 클래스
class SpritSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()

    return spr

#텍스트 드로우 함수
def draw_text(screen, text, size, color, x, y):
    gameFont = pygame.font.Font(os.path.join(DIR_FONT, DEFAULT_FONT_NAME), size)
    text_surface = gameFont.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (round(x), round(y))
    screen.blit(text_surface, text_rect)

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