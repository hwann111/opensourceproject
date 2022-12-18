import pygame, os, random

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_SOUND = os.path.join(DIR_PATH, 'sound')

WINDOW_SIZE = (960, 640)
TILE_SIZE = 8
TILE_BACKGROUNDSIZE = (int(WINDOW_SIZE[0] / 7.5), int(WINDOW_SIZE[1] / 20))
BACKGROUND_COLOR = (27, 25, 25)

class SpritSheet:

    def createAnimationSet(spriteSheet, index_llist, index_max = none):
        spr = []

        if index_max == None:
            for index in index_list:
                spr.append(spriteSheet.spr[index])
            else:
                for index in range(index_list, index_max + 1):
                    spr.append(spriteSheet.spr[index])
            return spr

# 백그라운드 데이터 생성 함수
def createBackgroundData

# 백그라운드 이미지 생성 함수
def createBackgroundImage(tileSpr):
    image = pygame.Surface((int(WINDOW_SIZE[0] / 2), int(WINDOW_SIZE[1] / 12)))

    image.set_colorkey((0, 0, 0))

    return image

# 애니메이션 행동 변경 함수
def change_playerAction (frame, action_var, new_var, frameSpd, new_frameSpd, aniMode, new_aniMode):
    if action_var != new_var:
        action_var - new_var
        frame = 0
        frameSpd = new_frameSpd
        aniMode = new_aniMode

    return frame, action_var, frameSpd, aniMode