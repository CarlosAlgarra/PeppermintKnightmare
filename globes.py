import pygame

pygame.init()
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (174, 198, 207)

# Time delta constant for frames
DELTA = 0
 
# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

# Images
SPIKE1 = pygame.image.load('spikes.png')
SPIKE1 =pygame.transform.scale(SPIKE1, (45,45))
SPIKE2 = pygame.image.load('spikes02.png')


GROUND1 = pygame.image.load('ground01.png')
GROUND2 = pygame.image.load('ground02.png')
GROUND3 = pygame.image.load('ground03.png')
GROUND4 = pygame.image.load('ground04.png')
GROUND5 = pygame.image.load('ground05.png')
GROUND6 = pygame.image.load('ground06.png')
GROUND7 = pygame.image.load('ground07.png')
GROUND8 = pygame.image.load('ground08.png')
GROUND9 = pygame.image.load('ground09.png')


ENEMY1 = pygame.image.load('spikedEnemy010001.png')
ENEMY2 = pygame.image.load('spikedEnemy010002.png')
ENEMY3 = pygame.image.load('spikedEnemy010003.png')
ENEMY4 = pygame.image.load('spikedEnemy010004.png')
ENEMY5 = pygame.image.load('spikedEnemy010005.png')
ENEMY6 = pygame.image.load('spikedEnemy010006.png')
ENEMY7 = pygame.image.load('spikedEnemy010007.png')
ENEMY8 = pygame.image.load('spikedEnemy010008.png')
ENEMY9 = pygame.image.load('spikedEnemy010009.png')
ENEMY10 = pygame.image.load('spikedEnemy010010.png')
ENEMY11 = pygame.image.load('spikedEnemy010011.png')
ENEMY12 = pygame.image.load('spikedEnemy010012.png')
ENEMY13 = pygame.image.load('spikedEnemy010013.png')
ENEMY14 = pygame.image.load('spikedEnemy010014.png')
ENEMY15 = pygame.image.load('spikedEnemy010015.png')
ENEMY16 = pygame.image.load('spikedEnemy010016.png')


PLAYERJUMP1 = pygame.image.load('mainChar_jump0001.png')
PLAYERWALK1 = pygame.image.load('mainChar_walk0001.png')
PLAYERWALK2 = pygame.image.load('mainChar_walk0002.png')
PLAYERWALK3 = pygame.image.load('mainChar_walk0003.png')
PLAYERWALK4 = pygame.image.load('mainChar_walk0004.png')
PLAYERWALK5 = pygame.image.load('mainChar_walk0005.png')
PLAYERWALK6 = pygame.image.load('mainChar_walk0006.png')


MENU = pygame.image.load('menu.png')
INSTR = pygame.image.load('instructions.png')


BACKGROUND = pygame.image.load('BG.png').convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))


#(image, width, height, offsetx, offsety)
ENEMYFRAMES = [(ENEMY1, 300, 230, 0, 0),
             (ENEMY2, 300, 230, 0, 0),
             (ENEMY3, 300, 230, 0, 0),
             (ENEMY4, 300, 230, 0, 0),
             (ENEMY5, 300, 230, 0, 0),
             (ENEMY6, 300, 230, 0, 0),
             (ENEMY7, 300, 230, 0, 0),
             (ENEMY8, 300, 230, 0, 0),
             (ENEMY9, 300, 230, 0, 0),
             (ENEMY10, 300, 230, 0, 0),
             (ENEMY11, 300, 230, 0, 0),
             (ENEMY12, 300, 230, 0, 0),
             (ENEMY13, 300, 230, 0, 0),
             (ENEMY14, 300, 230, 0, 0),
             (ENEMY15, 300, 230, 0, 0),
             (ENEMY16, 300, 230, 0, 0), 
             ]
PLAYERWALKFRAMES = [PLAYERWALK1,
                    PLAYERWALK2,
                    PLAYERWALK3,
                    PLAYERWALK4,
                    PLAYERWALK5,
                    PLAYERWALK6
                    ]
