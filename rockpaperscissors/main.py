import pygame
import pygame as game
import pygame.math as math
from pygame.time import Clock
import random
import os


class Object(pygame.sprite.Sprite):
    def __init__( self, image_filename, x, y ,element):
        ### Called when the sprite is created.  Do initialisation here.
        pygame.sprite.Sprite.__init__(self)
        self.element = element
        self.image       = pygame.transform.scale(pygame.image.load( image_filename ).convert_alpha(),(width_object, height_object))    # the image used

        self.rect        = self.image.get_rect()                                 # bounding rectangle for collision
        self.rect.center = ( x, y )                                              # Initial position
        self.vel    = pygame.math.Vector2( random.uniform(-1,1), random.uniform(-1,1)).normalize() * 3 # move randomly

    def update(self,sprite_group):
        ### Called to move, or change the state of the sprite
        self.rect.move_ip(self.vel)
        # make sure we're still on the screen, if not - wrap around
        if self.rect.left < 0 or self.rect.right > width:
            self.vel.reflect_ip(pygame.math.Vector2(1, 0))
        if self.rect.top < 0 or self.rect.bottom > height:
            self.vel.reflect_ip(pygame.math.Vector2(0, 1))

        for sprite in sprite_group:
            if sprite != self:
                if self.rect.colliderect(sprite.rect):
                    # print('collision')
                    normal = pygame.math.Vector2()
                    if self.element == 'rock' and sprite.element=='paper':
                        self.element = 'paper'
                        self.image = pygame.transform.scale(pygame.image.load( os.path.join('assets', 'paper.png') ).convert_alpha(),(width_object, height_object))

                    elif self.element == 'scissors' and sprite.element=='rock':
                        self.element = 'rock'
                        self.image = pygame.transform.scale(pygame.image.load( os.path.join('assets', 'rock.png') ).convert_alpha(),(width_object, height_object))
                    elif self.element == 'paper' and sprite.element=='scissors':
                        self.element = 'scissors'
                        self.image = pygame.transform.scale(pygame.image.load( os.path.join('assets', 'scissors.png') ).convert_alpha(),(width_object, height_object))
                    collision_y = sprite.rect.centery - self.rect.centery
                    collision_x = sprite.rect.centerx - self.rect.centerx
                    tangent = pygame.math.Vector2(-normal.y, normal.x)
                    if abs(collision_x) > abs(collision_y):
                        if collision_x > 0:
                            # Collision occurred on the right side of rect1
                            # print("Collision occurred on the right side of rect1")
                            self.vel.reflect_ip(pygame.math.Vector2(1, 0))
                        else:
                            # Collision occurred on the left side of rect1
                            # print("Collision occurred on the left side of rect1")
                            self.vel.reflect_ip(pygame.math.Vector2(1, 0))
                    else:
                        if collision_y > 0:
                            # Collision occurred on the bottom side of rect1
                            # print("Collision occurred on the bottom side of rect1")
                            self.vel.reflect_ip(pygame.math.Vector2(0, 1))
                        else:
                            # Collision occurred on the top side of rect1
                            # print("Collision occurred on the top side of rect1")
                            self.vel.reflect_ip(pygame.math.Vector2(0, 1))
                    # if normal.length()>0:
                    #     normal = normal.normalize()
                    #     self.vel.reflect_ip(normal)
                    #     sprite.vel.reflect_ip(normal)
                    # reflect the velocities
                    # calculate the direction away from the other sprite


width,height = 300,500
width_object = 20
height_object = 20
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("First Game!")
pygame.init()
fps = 30
def main():
    sprite_group = pygame.sprite.Group()
    for i in range(random.randint(5,9)):
        # Random position within the middle 80% of screen
        while True:
            pos_x = random.randint(50, width-50)
            pos_y = random.randint(50, height-50)
            obj = Object(os.path.join('assets', 'rock.png'), pos_x, pos_y,'rock')
            if not pygame.sprite.spritecollideany(obj, sprite_group):
                break
        sprite_group.add( obj )
    for i in range(random.randint(5,9)):
        # Random position within the middle 80% of screen
        while True:
            pos_x = random.randint(50, width - 50)
            pos_y = random.randint(50, height - 50)
            obj = Object(os.path.join('assets', 'scissors.png'), pos_x, pos_y, 'scissors')
            if not pygame.sprite.spritecollideany(obj, sprite_group):
                break
        sprite_group.add(obj)
    for i in range(random.randint(5,9)):
        # Random position within the middle 80% of screen
        while True:
            pos_x = random.randint(50, width - 50)
            pos_y = random.randint(50, height - 50)
            obj = Object(os.path.join('assets', 'paper.png'), pos_x, pos_y, 'paper')
            if not pygame.sprite.spritecollideany(obj, sprite_group):
                break
        sprite_group.add(obj)
    pygame.mixer.music.load(os.path.join('assets', 'Yarin Primak - Galaxy Groove.mp3'))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        win.fill((255, 255, 255))
        sprite_group.update(sprite_group)
        a=check_if_won(sprite_group)
        sprite_group.draw(win)
        if a:
            print(a)
            won(a)
            break
        pygame.display.flip()

    main()


def won(a):
    image = pygame.transform.scale(pygame.image.load( os.path.join('assets',  a+'.png') ).convert_alpha(),(100, 100))
    image_rect = image.get_rect()
    image_rect.centerx = width // 2
    image_rect.centery = height // 2
    win.blit(image, image_rect)
    pygame.display.update()
    pygame.mixer.music.stop()
    pygame.time.delay(5000)

def check_if_won(sprite_group):
    sprites = sprite_group.sprites()
    for i in range(len(sprite_group)-1):
        if sprites[i].element != sprites[i+1].element:
            return ''

    return sprites[0].element


if __name__ == "__main__":
    main()
