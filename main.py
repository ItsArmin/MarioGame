"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
 
Explanation video: http://youtu.be/BCxWJgN4Nnc
 
Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""


# IMPLEMENT SCROLLING AND ENEMIES!
 
#import pygame, constants
import pygame, constants, mario, sprite

# added: coin class
class Coin(pygame.sprite.Sprite):

    def __init__(self):

        # load coin sprite images
        super().__init__()

        # frame array
        self.frames = []

        # added: load sprite sheet
        self.sprite = pygame.image.load("coinTest.png").convert()

        # addes: frame var for animation and timer
        self.curFrame = 0
        self.timer = 0

        # added: load images from sheet

        # add to frames
        image = sprite.get_image(self, 0, 0, 14, 16, constants.GREEN)
        self.frames.append(image)
        image = sprite.get_image(self, 14, 0, 14, 16, constants.GREEN)
        self.frames.append(image)
        image = sprite.get_image(self, 28, 0, 14, 16, constants.GREEN)
        self.frames.append(image)        
        image = sprite.get_image(self, 42, 0, 14, 16, constants.GREEN)
        self.frames.append(image)

        # added: set starting sprite
        self.image = self.frames[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    # update coin 
    def update(self):
        self.animate()


    def animate(self):
        # control animation speed with timer
        self.timer += 1

        if self.timer % 5 == 0:
            self.curFrame += 1

            # see if frame limit reached for either direction
            if self.curFrame == len(self.frames):
                self.curFrame = 0

            # edit image to be current frame
            self.image = self.frames[self.curFrame]

# added: coin class
class Goomba(pygame.sprite.Sprite):

    def __init__(self):

        # load coin sprite images
        super().__init__()

        # frame array
        self.frames = []

        # death bool
        self.dead = False

        # added: load sprite sheet
        self.sprite = pygame.image.load("goomba_new.png").convert()

        # addes: frame var for animation and timer
        self.curFrame = 0
        self.timer = 1

        # added: load images from sheet

        # add to frames
        frameCount = 0
        while frameCount < 3:
            image = sprite.get_image(self, frameCount*16, 0, 16, 16, constants.GREEN)
            self.frames.append(image)
            frameCount += 1

        # added: set starting sprite
        self.image = self.frames[0]

        # added: var for moving speed
        self.change_x = -2

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()


    # update coin 
    def update(self):
        self.move()
        self.animate()

        if self.dead == True:
            self.die()

    def move(self):
        self.rect.x += self.change_x

    def animate(self):
        # control animation speed with timer
        self.timer += 1

        if self.timer % 5 == 0:
            self.curFrame += 1

            # see if frame limit reached for either direction
            if self.curFrame == len(self.frames) - 1:
                self.curFrame = 0

            # edit image to be current frame
            self.image = self.frames[self.curFrame]

    def die(self):
        self.image = self.frames[2]
        self.change_x *= 0

        self.timer += 1

        if self.timer % 15 == 0:
            self.kill()

# added: generic enemy class (SAVE FOR LATER)
"""class Enemy(pygame.sprite.Sprite):

    def __init__(self):

        # make generic 30 x 30 red block for now
        super().__init__()

        self.image = pygame.Surface([30, 30])
        self.image.fill(constants.RED)

        self.rect = self.image.get_rect()

        # Set speed vector of object
        self.change_x = 0
        self.change_y = 0

        # objects we can hit in level
        self.level = None

    def update(self):
        self.calc_grav()

        # See if we hit anything (x direction)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

                # Check and see if we hit any platforms (y direction)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0 

    def calc_grav(self):
        #Calculate effect of gravity.
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height """
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.GREEN)
 
        self.rect = self.image.get_rect()
 
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(constants.SKY)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Mario Test")
 
    player = mario.Mario()
    coin1 = Coin()
    coin2 = Coin()
    goomba = Goomba()

    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # create lists for all sprites and coins
    active_sprite_list = pygame.sprite.Group()
    object_list = pygame.sprite.Group()

    # add current level to player's level (for collision detection)
    player.level = current_level

    # initialize player
    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # initialize coins
    coin1.rect.x = 400
    coin1.rect.y = constants.SCREEN_HEIGHT - (coin1.rect.height * 1.5)
    active_sprite_list.add(coin1)
    object_list.add(coin1) 

    coin2.rect.x = 440
    coin2.rect.y = constants.SCREEN_HEIGHT - (coin2.rect.height * 1.5)
    active_sprite_list.add(coin2)
    object_list.add(coin2)

    # initialize Goomba
    goomba.rect.x = 600
    goomba.rect.y = constants.SCREEN_HEIGHT - goomba.rect.height
    active_sprite_list.add(goomba)
    object_list.add(goomba)

    # added: play music
    #pygame.mixer.music.load("cenaTheme.wav")
    #pygame.mixer.music.play(-1,0)

    # added: coin sound effect
    # sound effect
    coinSound = pygame.mixer.Sound("coinSound.wav")

    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not player.crouching:
                    player.go_left()
                if event.key == pygame.K_RIGHT and not player.crouching:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_DOWN:
                    if not player.running:
                        player.crouching = True
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_DOWN:
                    player.crouching = False

        # Update all sprites
        active_sprite_list.update()

        # check if coins collected
        for obj in object_list:

            # what do to if colliding with object
            if player.rect.colliderect(obj):

                # if coin, collect it
                if isinstance(obj, Coin):
                    object_list.remove(obj)
                    active_sprite_list.remove(obj)
                    coinSound.play()

                # if goomba, only destroy if jumped on from top
                if isinstance(obj, Goomba):
                    if player.change_y > 0:
                        player.jump()
                        obj.dead = True

                    else:
                        goomba.change_x = -goomba.change_x
                        player.stop()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > constants.SCREEN_WIDTH:
            player.rect.right = constants.SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()
