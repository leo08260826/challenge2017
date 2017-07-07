import pygame as pg

DIR_U  = 1
DIR_RU = 2
DIR_R  = 3
DIR_RD = 4
DIR_D  = 5
DIR_LD = 6
DIR_L  = 7
DIR_LU = 8

ACTION_0 = 0 # power throw / barrier
ACTION_1 = 1 # stun / mask
ACTION_2 = 2 # general throw

SKILLCARD_0 = 0 # invisible
SKILLCARD_1 = 1 # empty power
SKILLCARD_2 = 2 # stun all enermy

# [up, right, down, left, chmod, act0, act1,act2 ]
PlayerKeys = [
    [pg.K_w, pg.K_d, pg.K_s, pg.K_a, pg.K_c, pg.K_v, pg.K_b, pg.K_n],
    [pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHTBRACKET, pg.K_LEFTBRACKET, pg.K_p, pg.K_o],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1]
]

# up = 1, right = 2, down = 4, left = 8 -> RU = 3, RD = 6, LU = 9, LD = 12
DirHash = [0, DIR_U, DIR_R, DIR_RU, DIR_D, 0, DIR_RD, 0, DIR_L, DIR_LU, 0, 0, DIR_LD, 0, 0, 0]