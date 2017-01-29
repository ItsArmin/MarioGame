# General Sprite functions for all sprite classes
import pygame

# added in: get image of THE sprite with top-left x & y coordinates, along with dimensions of image segment
def get_image(theSprite, x, y, w, h, transparentColor):
    image = pygame.Surface([w, h])
    rect = image.get_rect()

    # put sprite sheet onto image surface based on inputs
    image.blit(theSprite.sprite, (0,0), (x, y, w, h))

    # add transparency
    image.set_colorkey(transparentColor)

    # enlarge sprites for screen
    image = pygame.transform.scale(image, (int(rect.width*2), int(rect.height*2)))

    # return parsed image
    return image

