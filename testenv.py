
import pygame
import tkMessageBox
from globes import *

 
class Player(pygame.sprite.Sprite):

 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super(Player, self).__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 40
        self.image = PLAYERWALK1
        self.image = pygame.transform.scale(self.image, (int(30*2), int(54*2)))
        self.orientation = 1
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

        # frame variables
        self.frame = 0
        self.frame_timer = 0
        self.frame_time = 100
        self.frame_ct = 6
        self.stopped = True
        self.grounded = True
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

        # Check for enemy collision
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            self.rect.x = 130 + self.level.world_shift
            self.rect.y = 165

        #Animate Walk
        if self.frame_timer > self.frame_time and self.stopped == False and  self.grounded == True:
            self.frame_timer -= self.frame_time
            self.frame = (self.frame + 1) % self.frame_ct
            
            self.image = PLAYERWALKFRAMES[self.frame]
            self.image = pygame.transform.scale(self.image, (int(27*2), int(54*2)))
            if self.orientation == 0:
                self.image = pygame.transform.flip(self.image, True, False)
        if self.stopped == False and self.grounded == True:
            self.frame_timer += DELTA

    def trigger_press(self):
        trigger_hit_list = pygame.sprite.spritecollide(self, self.level.trigger_list, True)
        for trigger in trigger_hit_list:
            for switch in trigger.triggeredtriggers:
                switch.rect.x += self.level.world_shift
                self.level.trigger_list.add(switch)
            trigger.activate()
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
            self.grounded = True
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.image = PLAYERWALK1
            self.image = pygame.transform.scale(self.image, (int(27*2), int(54*2)))
            self.rect.x = 130 + self.level.world_shift
            self.rect.y = 165
            self.orientation = 1
            self.grounded = True
 
    def jump(self):
        """ Called when user hits 'jump' button. """
        self.image = PLAYERJUMP1
        self.image = pygame.transform.scale(self.image, (int(27*2), int(54*2)))
        if(self.orientation == 0):
            self.image = pygame.transform.flip(self.image, True, False)
            
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
            self.grounded = False
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        if self.grounded == True:
            self.stopped = False
        if(self.orientation == 1):
            self.image = pygame.transform.flip(self.image, True, False)
            self.orientation = 0
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        if self.grounded == True:
            self.stopped = False
        if(self.orientation == 0):
            self.image = pygame.transform.flip(self.image, True, False)
            self.orientation = 1
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.stopped = True
        self.change_x = 0
 
class Spike(pygame.sprite.Sprite):
    def __init__(self, width,height, x, y, spiketype):

        super(Spike, self).__init__()
 
        
        
        self.spikeimg = pygame.image.load('spikes02.png')
        self.spikeimg = pygame.transform.scale(self.spikeimg, (int(width), int(height)))
        self.image = pygame.Surface([width, height], pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        
        self.image.blit(self.spikeimg, (0,0), (0, 0, width, height))
        
       
 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = None
        

class Trigger(pygame.sprite.Sprite):
    def __init__(self, x, y, ):

        super(Trigger,self).__init__()
        self.image = pygame.Surface([20, 20])
        self.image = SPIKE1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.objects = pygame.sprite.Group()
        self.triggeredtriggers = pygame.sprite.Group()

    def activate(self):
        for obj in self.objects:
            obj.activate()
            
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height, offsety, plattype):

        super(Platform, self).__init__()
 
        
        self.width = width
        self.height = height
        self.platimg = plattype
        self.platimg = pygame.transform.scale(self.platimg, (int(width), int(height)))
        self.image = pygame.Surface([width, height], pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        
        self.image.blit(self.platimg, (0,0), (0, offsety, width, height))
        
       
 
        self.rect = self.image.get_rect()
   
class Enemy(Platform):
    change_x = 0
    change_y = 0
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
    player = None
    level = None

    frame = 0
    frame_timer = 0
    frame_time = 100
    frame_ct = 16
    def update(self):
        # Move left/right
        self.rect.x += self.change_x

        # Move up/down
        self.rect.y += self.change_y
 
        
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

        #update frame
        if self.frame_timer > self.frame_time:
            self.frame_timer -= self.frame_time
            self.frame = (self.frame + 1) % self.frame_ct

            
            self.platimg = ENEMYFRAMES[self.frame][0]
            self.platimg = pygame.transform.scale(self.platimg, (int(self.width), int(self.height)))
            self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA,32)
            self.image = self.image.convert_alpha()
            
            self.image.blit(self.platimg, (0,0), (0, ENEMYFRAMES[self.frame][4], self.width, self.height))
            
           
     
        
        self.frame_timer += DELTA
        #test code to observe hitbox
        #pygame.draw.rect(screen, BLUE, self.rect)
        #pygame.display.flip()
 
 
 
class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
    trigger_cx = 0
    trigger_cy = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

        #test code to observe hitbox
        #pygame.draw.rect(screen, BLUE, self.rect)
        #pygame.display.flip()
            
    def activate(self):
        self.change_x = self.trigger_cx
        self.change_y = self.trigger_cy

    def deactivate(self):
        self.change_x = 0
        self.change_y = 0
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.trigger_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
     
        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.trigger_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)

        #drawing the background causes a lot of lag
        screen.blit(BACKGROUND, (0,0))
        
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.trigger_list.draw(screen)
        
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:
        """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for trigger in self.trigger_list:
            trigger.rect.x += shift_x

    def iteratespikes(self, width, height, start, end, y, spiketype):
        amount = end - start
        amount1 = int(amount/width)
        remaining = int(amount%width)
        posinit = start

       

        while amount1 != 0:
            block = Spike(width, height, posinit, y, spiketype)
            block.level = self
            self.enemy_list.add(block)
            posinit += width
            amount1 -=1
        if remaining != 0:
            block = Spike(remaining, height, posinit, y, spiketype)
            block.level = self
            self.enemy_list.add(block)
            posinit += width
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1500
 
        # Array with width, height, x, y, and y offset for image
        level = [#[1, SCREEN_HEIGHT*2, 0, -SCREEN_HEIGHT,10],
                 #[1, SCREEN_HEIGHT*2, SCREEN_WIDTH*5, -SCREEN_HEIGHT,10],
                 [210, 210, 0, 350,30, GROUND1],
                 [256, 120, 525, 280,15, GROUND2 ],
                 [256, 120, 750, 280,15, GROUND2],
                 [256, 120, 975, 280,15, GROUND2],
                 [256, 120, 525, 620,15, GROUND2 ],
                 [256, 120, 750, 620,15, GROUND2],
                 [256, 120, 975, 620,15, GROUND2],
                 [256, 120, 2500, 100,15, GROUND2 ],
                 [256, 120, 2725, 100,15, GROUND2],
                 [256, 120, 2950, 100,15, GROUND2],
                 [256, 120, 4300, 115,15, GROUND2 ],
                 [256, 120, 4525, 115,15, GROUND2],
                 [256, 120, 4750, 115,15, GROUND2],
                 [256, 50, 4300, 400+65,15, GROUND2 ],
                 [256, 50, 4525, 400+65,15, GROUND2],
                 [256, 50, 4750, 400+65,15, GROUND2],
                 [300, 120, 1625, 280,15, GROUND2 ],
                 [256, 120, 5150, 175,15, GROUND2 ],
                 [256, 120, 5375, 175,15, GROUND2 ],
                 [256, 120, 5700, 250,15, GROUND2 ],
                 [256, 120, 5925, 250,15, GROUND2 ],
                 [256, 120, 6250, 325,15, GROUND2 ],
                 [256, 120, 6475, 325,15, GROUND2 ],
                 [15, 220, 4288, 200,15, GROUND1 ]
                 ]

        #Create Enemies Here
        #Sample Enemy
        enemy = Enemy(117, 90,0, ENEMY1)
        enemy.rect.x = 645
        enemy.rect.y = 195
        enemy.boundary_left = 525
        enemy.boundary_right = 1100
        enemy.change_x=5
        enemy.player = self.player
        enemy.level = self
        self.enemy_list.add(enemy)

        enemy = Enemy(117, 90,0, ENEMY1)
        enemy.rect.x = 645
        enemy.rect.y = 195
        enemy.boundary_left = 525
        enemy.boundary_right = 1100
        enemy.change_x=3
        enemy.player = self.player
        enemy.level = self
        self.enemy_list.add(enemy)

        enemy = Enemy(143, 110,0, ENEMY1)
        enemy.rect.x = 2500
        enemy.rect.y = 5
        enemy.boundary_left = 2500
        enemy.boundary_right = 3100
        enemy.change_x=5
        enemy.player = self.player
        enemy.level = self
        self.enemy_list.add(enemy)

        enemy = Enemy(143, 110,0, ENEMY1)
        enemy.rect.x = 2500
        enemy.rect.y = 5
        enemy.boundary_left = 2500
        enemy.boundary_right = 3100
        enemy.change_x=2
        enemy.player = self.player
        enemy.level = self
        #self.enemy_list.add(enemy)

        enemy = Enemy(125, 100,0,ENEMY1)
        enemy.rect.x = 4300
        enemy.rect.y = 10
        enemy.boundary_left = 4300
        enemy.boundary_right = 4900
        enemy.change_x=3
        enemy.player = self.player
        enemy.level = self
        #self.enemy_list.add(enemy)

        enemy = Enemy(125, 100,0, ENEMY1)
        enemy.rect.x = 4300
        enemy.rect.y = 10
        enemy.boundary_left = 4300
        enemy.boundary_right = 4900
        enemy.change_x=5
        enemy.player = self.player
        enemy.level = self
        self.enemy_list.add(enemy)


 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], platform[4], platform[5])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        #add triggers
        trigger1 = Trigger(0, 330)
        trigger2 = Trigger(540, 600)
        self.trigger_list.add(trigger2)
        trigger3 = Trigger(2850, 375)
        self.trigger_list.add(trigger3)
        trigger4 = Trigger(4350, 380)
        self.trigger_list.add(trigger4)
        trigger5 = Trigger(6700, 313)
        self.trigger_list.add(trigger5)
        

        trigger2.triggeredtriggers.add(trigger1)
        
        # Add a custom moving platform
        block = MovingPlatform(100, 20,10, GROUND3)
        block.rect.x = 317
        block.rect.y = 40
        block.boundary_top = 40
        block.boundary_bottom = 540
        block.trigger_cy = 8
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        trigger2.objects.add(block)

        block = MovingPlatform(100, 20,10, GROUND3)
        block.rect.x = 1400
        block.rect.y = 50
        block.boundary_top = 50
        block.boundary_bottom = 240
        block.trigger_cy = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        trigger1.objects.add(block)

        block = MovingPlatform(15, 220,10, GROUND4)
        block.rect.x = 520
        block.rect.y = 450
        block.boundary_top = 400
        block.boundary_bottom = 940
        block.trigger_cy = 8
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        trigger2.objects.add(block)

        block = MovingPlatform(100, 20,10, GROUND1)
        block.rect.x = 2300
        block.rect.y = 50
        block.boundary_top = 50
        block.boundary_bottom = 540
        block.trigger_cy = 8
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        trigger2.objects.add(block)

        block = MovingPlatform(100, 20,10, GROUND4)
        block.rect.x = 3500
        block.rect.y = 75
        block.boundary_left = 3200
        block.boundary_right = 4000
        block.trigger_cx=8
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        trigger3.objects.add(block)


        block = MovingPlatform(15, 220,10, GROUND1)
        block.rect.x = 5000
        block.rect.y = 200
        block.boundary_top = 50
        block.boundary_bottom = 940
        block.trigger_cy = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        trigger5.objects.add(block)

        block = MovingPlatform(1500, 15,10, GROUND1)
        block.rect.x = 5150
        block.rect.y = -3
        block.boundary_left = 4900
        block.boundary_right = 6300
        block.change_x = 8
        block.player = self.player
        block.level = self
        #self.platform_list.add(block)


        block = MovingPlatform(200, 20,10, GROUND1)
        block.rect.x = 6300
        block.rect.y = 550 +65
        block.boundary_left = 5000
        block.boundary_right = 6800
        block.trigger_cx= 8
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        trigger5.objects.add(block)

        block = MovingPlatform(256, 120,15, GROUND2)
        block.rect.x = 2500
        block.rect.y = 380
        block.boundary_top = 380
        block.boundary_bottom = 800
        block.change_y = 3
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(256, 120,15, GROUND2)
        block.rect.x = 2725
        block.rect.y = 380
        block.boundary_top = 360
        block.boundary_bottom = 800
        block.change_y = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(256, 120,15, GROUND2)
        block.rect.x = 2950
        block.rect.y = 380
        block.boundary_top = 380
        block.boundary_bottom = 800
        block.change_y = 3
        block.player = self.player
        block.level = self
        self.platform_list.add(block)






        #add spikes
        self.iteratespikes(75,75,530, 1240, 370, SPIKE2)

        self.iteratespikes(75,75,2500, 3200, 190, SPIKE2)

        block = Spike(75, 75, 4800, 330+65, SPIKE2)
        self.enemy_list.add(block)

        block = Spike(75, 75, 4600, 330+65, SPIKE2)
        self.enemy_list.add(block)

        block = Spike(75, 75, 4400, 330+65, SPIKE2)
        self.enemy_list.add(block)

        block = Spike(75, 75, 5150, 150, SPIKE2)
        self.enemy_list.add(block)

        block = Spike(75, 75, 5350, 150, SPIKE2)
        self.enemy_list.add(block)
        
        block = Spike(75, 75, 5550, 150, SPIKE2)
        self.enemy_list.add(block)

        block = Spike(75, 75, 5700, 225, SPIKE2)
        self.enemy_list.add(block)

        block = Spike(75, 75, 5900, 225, SPIKE2)
        self.enemy_list.add(block)
        
        block = Spike(75, 75, 6100, 225, SPIKE2)
        self.enemy_list.add(block)
        
        block = Spike(75, 75, 6250, 300, SPIKE2)
        self.enemy_list.add(block)
        
        block = Spike(75, 75, 6550, 300, SPIKE2)
        self.enemy_list.add(block)
        


        
        







 
 
def main():
    """ Main Program """
 
    pygame.display.set_caption("Peppermint Knight")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))

 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    #original values x = 130, y = 240
    player.rect.x = 130
    player.rect.y = 240
    active_sprite_list.add(player)

    
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # Menu Counter
    menuCounter = 0
 
    # -------- Main Program Loop -----------
    while not done:
        if menuCounter == 0:
            
            while(menuCounter == 0):
                screen.blit(MENU, (0,0))
                mouse_pos = pygame.mouse.get_pos()
                
                
                
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True
                    elif event.type == pygame.MOUSEBUTTONDOWN and 780 > mouse_pos[0] > 650 and 600 > mouse_pos[1] > 560:
                        menuCounter = 3
                        start_time = pygame.time.get_ticks()
                    elif event.type == pygame.MOUSEBUTTONDOWN and 1150 > mouse_pos[0] > 875 and 600 > mouse_pos[1] > 560:
                        menuCounter = 2
     
            
                
                    #print str(mouse_pos[0]) +" "+ str(mouse_pos[1])
                    clock.tick(60)
                    pygame.display.flip()

                if done == True:
                    break
                
                
        elif menuCounter == 2:
            while(menuCounter == 2):
                screen.blit(INSTR, (0,0))
                mouse_pos = pygame.mouse.get_pos()
                
                
                
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True
                    elif event.type == pygame.MOUSEBUTTONDOWN and 275 > mouse_pos[0] > 50 and 145 > mouse_pos[1] > 40:
                        menuCounter = 0
     
            
                
                    #print str(mouse_pos[0]) +" "+ str(mouse_pos[1])
                    clock.tick(60)
                    pygame.display.flip()
                if done == True:
                    break

        
            


        elif menuCounter == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT :
                        player.go_left()
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player.go_right()
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_e or event.key == pygame.K_x:
                        player.trigger_press()
     
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and player.change_x < 0:
                        player.stop()
                    if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and player.change_x > 0:
                        player.stop()
                    if event.key == pygame.K_SPACE:
                        player.change_y += 2.75
                        player.image = PLAYERWALK1
                        player.image = pygame.transform.scale(player.image, (int(27*2), int(54*2)))
                        if (player.orientation == 0):
                            player.image = pygame.transform.flip(player.image, True, False)

            global DELTA
            DELTA = pygame.time.get_ticks() - start_time
            start_time = pygame.time.get_ticks()
             
            # Update the player.
            active_sprite_list.update()

     
            # Update items in the level
            current_level.update()

            
     
            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shift_world(-diff)
     
            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 220:
                diff = 120 - player.rect.left
                player.rect.left = 120
                current_level.shift_world(diff)
 
 
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
     
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
            # Limit to 60 frames per second
            clock.tick(60)
     
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            if not level_list[0].trigger_list:
                menuCounter = 0
                tkMessageBox.showinfo(title="Peppermint Knightmare", message="YOU WON! (Who are we kidding... no one will ever read this).")
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()
