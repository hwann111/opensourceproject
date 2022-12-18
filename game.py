import pygame, sys
from datafile import *
from pygame.locals import *
pygame.init()

pygame.display.set_caption('거북목 방지 게임') #화면 타이틀
clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

spriteSheet_player = SpriteSheet('spriteSheet1.png', 16, 16, 8, 8, 12) #스프라이트 시트에서 이미지 로드
spriteSheet_enemy = SpriteSheet('spriteSheet2.png', 8, 8, 16, 16, 37)
spriteSheet_background = SpritSheet('spriteSheet3.png', 8, 8, 16, 16,87)

spr_player = {}
spr_player['stay'] = createAnimationSet(spriteSheet_player, [0])
spr_player['attacked'] = createAnimationSet(spriteSheet_player, [9, 10, 11])

spr_enemy = {}
spr_enemy['stay'] = createAnimationSet(spriteSheet_player, [0])
spr_enemy['attack'] = createAnimationSet(spriteSheet_player, [9, 10, 11])

createBackgroundData()
backgroundImage = createBackgroundImage(spriteSheet_background)

player_rect = pygame.Rect((TILE_MAPiSIZE[0] * 4, TILE_MAPSIZE[1] * 4 - 14), (6, 14)) # 플레이어 화면에서 고정
player_movement = [0, 0]
player_vspeed = 0
player_flytime = 0 # 공중에 뜬 시간

player_action = 'stay'
player_frame = 0
player_framespeed = 1
player_frametimer = 0
player_animationMode = True #애니메이션 모드 (한번만)

# 게임 구동
while True:
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))

    screen.blit(spriteSheet_player.spr[0], (320, 240))
    screen.blit(spriteSheet_enemy_.spr[0], (320, 240))

# 플레이어
    player_movement = [0, 0]
    player_movement[1] += player_vspeed

    player_vspeed += 0.2
    if player_vspeed > 3;
        player_vspeed = 3

# 적
    enemy_movement = [0, 0]
    enemy_movement[1] += player_vspeed

    enemy_vspeed += 0.2
    if enemy_vspeed > 3;
        enemy_vspeed = 3

# 이벤트
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60) #60프레임 제한