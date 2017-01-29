# Mario class (for player)

import pygame, constants, sprite

class Mario(pygame.sprite.Sprite):

    def __init__(self):

        # parent constructor
        super().__init__()

        """ Init constants and variables """
        # States for Mario 
        self.standing = self.big = True
        self.walking = self.running = self.jumping = self.highJumping = self.falling = self.crouching = self.small = False
        self.direction = "R"

        # sprite arrays (big and small Mario)
        self.bigR_frames = []
        self.bigL_frames = []

        self.smallR_frames = []
        self.smallL_frames = []

        # frame constants (for big Mario)
        self.turnFrame = 4
        self.jumpFrame = 5
        self.crouchFrame = 6
        self.moveFrame = 3
        
        # frame vars for animation and timer
        self.frames = self.bigR_frames   # current set of frames to be using
        self.curFrame = 0
        self.timer = 0

        """ Load images from sprite sheet""" 

        # Big Mario

        # load sprite sheet
        self.sprite = pygame.image.load("bigMario_blue.png").convert()  # sprite is attribute of this class constructor

        # add to right frames with loop
        frameCount = 0
        while frameCount < 6:   # load each standing sprite
            image = sprite.get_image(self, frameCount*16, 0, 16, 28, constants.GREEN)
            self.bigR_frames.append(image)
            frameCount += 1

        # load crouch sprite
        image = sprite.get_image(self, frameCount*16, 10, 16, 18, constants.GREEN)
        self.bigR_frames.append(image)   

        # add to left (just flip frames of right)
        for frame in self.bigR_frames:
            temp = pygame.transform.flip(frame, True, False)
            self.bigL_frames.append(temp)
    
        # set starting sprite
        self.image = self.bigR_frames[self.curFrame]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

    # update Mario
    def update(self):
        # Gravity
        self.calc_grav()

        # run only if on ground
        if self.running == True and self.jumping == False and self.crouching == False:
            self.walk()

        # see if running
        if abs(self.change_x) > 0 and not self.jumping:
            self.running = True
            self.standing = False

        else:
            self.running = False
            self.standing = True

        # Move left/right
        self.rect.x += self.change_x

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
 
        # see if on ground
        if self.change_y == 0:
            self.jumping = False

        # display standing sprite
        if self.running == False and self.jumping == False:
            self.stand()

        # display standing sprite
        if self.crouching == True:
            self.crouch()
            self.rect.y += self.change_y

        else: # Move up/down
            self.rect.y += self.change_y

        if self.jumping:
            # determine what sprite to use for jumping
            if self.crouching:
                if self.direction == "R":
                    self.image = self.bigR_frames[self.crouchFrame]
                else:
                    self.image = self.bigL_frames[self.crouchFrame] 

            elif self.direction == "R":
                self.image = self.bigR_frames[self.jumpFrame]
            else:
                self.image = self.bigL_frames[self.jumpFrame]
     
        # Check and see if we hit any platforms (y direction)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.jumping = False
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
        
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height


    # standing function
    def stand(self):
        self.frames = self.decideFrames()
        self.image = self.frames[0]

    # running function
    def walk(self):
        # change frame based on direction
        self.frames = self.decideFrames()

        # control animation speed with timer and frame direction
        self.timer += 1

        if self.timer % 4 == 0:
            self.curFrame += 1

            print (self.curFrame)

            # see if move frame limit (3) reached for either direction
            if self.curFrame > self.moveFrame:
                self.curFrame = 0

            self.image = self.frames[self.curFrame]

    def jump(self):

        # move up 2 pixels for start of jump
        self.jumping = True
        self.rect.y += 2

        # add platforms to list to check if open space above and end first part of jump
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # if no platforms hit, jump up
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.direction = "L"
        self.running = True
        while self.change_x > -4:
            self.change_x -= .1


    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.direction = "R"
        self.running = True
        while self.change_x < 4:
            self.change_x += .1

 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.running = False
        self.change_x = 0

    def crouch(self):
        # crouch based on direction
        if self.direction == "R":
            self.image = self.bigR_frames[self.crouchFrame]
        else:
            self.image = self.bigL_frames[self.crouchFrame]

        self.change_y += 20

    # function that decides what frames to be using for anything
    def decideFrames(self):
        # check based on direction and size
        if self.direction == "R":
            if self.big == True:
                return self.bigR_frames
            else:
                return self.smallR_frames

        else:
            if self.big == True:
                return self.bigL_frames
            else:
                return self.smallL_frames


