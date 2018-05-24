import pygame
from pygame import *
import random

WIN_WIDTH = 700
WIN_HEIGHT = 512
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
WHITE = (255, 255, 255)
RED = (157, 10, 14)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
DANTEW = 64
DANTEH = 64
BULLET_WIDTH = 40
BULLET_HEIGHT = 6
BULLET2_HEIGHT = 83
BULLET2_WIDTH = 60
BATWIDTH = 40
BATHEIGHT = 20
GRAYWIDTH = 80
GRAYHEIGHT = 128
GARBULLWIDTH = 110
GARBULLHEIGHT = 30
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30


class Game:
    def __init__(self, platforms, entities):
        self.left_up = self.left_down = self.right_up = self.right_down = False
        self.clock = pygame.time.Clock()
        self.platforms = platforms
        self.entities = entities
        self.play = self.madeby = self.storyp1 = self.storyp2 = self.clarify = self.storyp3 = self.end = self.outro = self.play2 = self.storyp4 = self.play3 = self.story5 = self.play4 = False
        self.intro = True


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Dante(Entity):
    def __init__(self, x, y, container):
        Entity.__init__(self)
        self.container = container
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.image.load("images/Stand.png")
        self.image = pygame.transform.scale(self.image, (DANTEW, DANTEH))
        self.rect = Rect(x, y, 64, 64)

    def update(self, up, down, left, right, running, shooting, platforms, player, bullet_group, loop_counter, huey_group, run, bullet2_group, platform_group, num, graygroup):
        if up:
            if self.onGround:
                self.yvel -= 9
        if running:
            self.xvel = 12
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if self.onGround == False:
            self.yvel += 0.4
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        if shooting:
            if loop_counter % 20 == 0:
                bullet = Bullet(player)
                bullet_group.add(bullet)
        self.rect.left += self.xvel
        self.collide(self.xvel, 0, platforms, run, platform_group)
        self.rect.top += self.yvel
        self.onGround = False
        if run.play2 == True:
            if self.rect.y >= 470:
                self.kill()
                music_intro.stop()
                music_2.stop()
                music_3.stop()
                music_4.stop()
                run.play = run.storyp1 = run.storyp2 = run.clarify = run.storyp3 = run.intro = run.play2 = False
                run.outro = True

        # do y-axis collisions
        self.collide(0, self.yvel, platforms, run, platform_group)

        collision = pygame.sprite.spritecollide(self, huey_group, True)
        collision2 = pygame.sprite.spritecollide(self, bullet2_group, True)
        collision3 = pygame.sprite.spritecollide(self, graygroup, True)
        if collision or collision2 or collision3:
            self.kill()
            music_intro.stop()
            music_2.stop()
            run.play = run.play2 = run.play3 = run.play4 = False
            run.outro = True


        self.rect.clamp_ip(self.container)

    def collide(self, xvel, yvel, platforms, run, player):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    run.play = False
                    run.storyp3 = True
                    player.up = player.down = player.left = player.right = player.running = player.shooting = False
                    music_intro.stop()
                    music_2.stop()
                    music_2.play(-1)
                    music_3.stop()
                    music_4.stop()
                if isinstance(p, ExitBlock2):
                    run.play2 = False
                    run.storyp4 = True
                    player.up = player.down = player.left = player.right = player.running = player.shooting = False
                    music_intro.stop()
                    music_2.stop()
                    music_3.play(-1)
                    music_4.stop()
                if isinstance(p, ExitBlock3):
                    run.play3 = False
                    run.story5 = True
                    player.up = player.down = player.left = player.right = player.running = player.shooting = False
                    music_intro.stop()
                    music_2.stop()
                    music_3.stop()
                    music_4.play(-1)
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    def setimage(self, up, down, left, right, shooting):
        if right and self.onGround:
            self.image = pygame.image.load("images/run 1.png")
            self.image = pygame.transform.scale(self.image, (DANTEW, DANTEH))

        if left and self.onGround:
            self.image = pygame.image.load("images/run 3.png")
            self.image = pygame.transform.scale(self.image, (DANTEW, DANTEH))

        if up:
            if not self.onGround:
                self.image = pygame.image.load("images/Jump.png")
                self.image = pygame.transform.scale(self.image, (DANTEW, DANTEH))

        if down or self.onGround and left == False and right == False and shooting == False:
            self.image = pygame.image.load("images/Stand.png")
            self.image = pygame.transform.scale(self.image, (DANTEW, DANTEH))

        if shooting:
            self.image = pygame.image.load("images/Jump Shoot.png")
            self.image = pygame.transform.scale(self.image, (DANTEW, DANTEH))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, dante):
        pygame.sprite.Sprite.__init__(self)
        self.dante = dante
        self.image = pygame.image.load("images/stake.png")
        self.image = pygame.transform.scale(self.image, (BULLET_WIDTH, BULLET_HEIGHT))
        self.rect = self.image.get_rect()
        self.set_pos()
        self.speed = 15

    def set_pos(self):
        self.rect.x = self.dante.rect.x + 64
        self.rect.y = self.dante.rect.y + 24

    def update(self):
        self.rect = self.rect.move((self.speed, 0))

        if self.rect.x <= 0:
            self.kill()
        if self.rect.x >= 1100:
            self.kill()

class Bat(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.speed = 10
        self.upspeed = random.randrange(-5, 5)
        self.health = 1
        self.image = pygame.image.load("images/bat.png")
        self.image = pygame.transform.scale(self.image, (BATWIDTH, BATHEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(850, 900)
        self.rect.y = random.randrange(0, 200)

    def update(self, bullet_group):
        self.rect.x -= self.speed
        self.rect.y -= self.upspeed

        collision = pygame.sprite.spritecollide(self, bullet_group, True)
        if collision:
            self.kill()
        if self.rect.x <= 0:
            self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, container, loop_counter, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.loop_counter = loop_counter
        self.container = container
        self.health = 10
        self.speed = random.randrange(1, 4)
        self.image = pygame.image.load("images/zombie.png")
        self.image = pygame.transform.scale(self.image, (DANTEW, DANTEH))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

    def update(self, bullet_group):
        self.rect.x -= self.speed

        collision = pygame.sprite.spritecollide(self, bullet_group, True)
        if collision:
            self.health = self.health - 2
        if self.health == 0:
            self.kill()

class Gargoyle(pygame.sprite.Sprite):
    def __init__(self, container, loop_counter, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.loop_counter = loop_counter
        self.container = container
        self.image = pygame.image.load("images/gargoyle.png")
        self.image = pygame.transform.scale(self.image, (DANTEW/int(1.5), DANTEH/int(1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

class GarBullet(pygame.sprite.Sprite):
    def __init__(self, gargoyle):
        pygame.sprite.Sprite.__init__(self)
        self.gargoyle = gargoyle
        self.image = pygame.image.load("images/fireball left.png")
        self.image = pygame.transform.scale(self.image, (GARBULLWIDTH, GARBULLHEIGHT))
        self.rect = self.image.get_rect()
        self.set_pos()
        self.speed = 10

    def set_pos(self):
        self.rect.x = self.gargoyle.rect.x - 110
        self.rect.y = self.gargoyle.rect.y + 24

    def update(self):
        self.rect = self.rect.move((-self.speed, 0))

        if self.rect.x <= -100:
            self.kill()
        if self.rect.x >= 1100:
            self.kill()

class Gargoyleright(pygame.sprite.Sprite):
    def __init__(self, container, loop_counter, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.loop_counter = loop_counter
        self.container = container
        self.image = pygame.image.load("images/gargoyle right.png")
        self.image = pygame.transform.scale(self.image, (DANTEW/int(1.5), DANTEH/int(1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

class GarBulletright(pygame.sprite.Sprite):
    def __init__(self, gargoyle):
        pygame.sprite.Sprite.__init__(self)
        self.gargoyle = gargoyle
        self.image = pygame.image.load("images/fireball right.png")
        self.image = pygame.transform.scale(self.image, (GARBULLWIDTH, GARBULLHEIGHT))
        self.rect = self.image.get_rect()
        self.set_pos()
        self.speed = 10

    def set_pos(self):
        self.rect.x = self.gargoyle.rect.x
        self.rect.y = self.gargoyle.rect.y + 24

    def update(self):
        self.rect = self.rect.move((self.speed, 0))

        if self.rect.x <= 0:
            self.kill()
        if self.rect.x >= 1100:
            self.kill()


class Gray(pygame.sprite.Sprite):
    def __init__(self, x, y, container, loop_counter):
        pygame.sprite.Sprite.__init__(self)
        self.loop_counter = loop_counter
        self.container = container
        self.health = 100
        self.image = pygame.image.load("images/gray.png")
        self.image = pygame.transform.scale(self.image, (GRAYWIDTH, GRAYHEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, bullet_group, run):
        if self.loop_counter % 20:
            self.rect.x -= random.randrange(-20, 20)
            self.rect.y -= random.randrange(-20, 20)

        collision = pygame.sprite.spritecollide(self, bullet_group, True)
        if collision:
            self.health = self.health - 4
        if self.health == 0:
            self.kill()
            run.play = run.madeby = run.storyp1 = run.storyp2 = run.clarify = run.storyp3  = run.outro = run.play2 = run.storyp4 = run.play3 = run.story5 = run.play4 = False
            run.end = True

        self.rect.clamp_ip(self.container)




class Bullet2(pygame.sprite.Sprite):
    def __init__(self, gray):
        pygame.sprite.Sprite.__init__(self)
        self.gray = gray
        self.image = pygame.image.load("images/slash_new.png")
        self.image = pygame.transform.scale(self.image, (BULLET2_WIDTH, BULLET2_HEIGHT))
        self.rect = self.image.get_rect()
        self.set_pos()
        self.speed = 5

    def set_pos(self):
        self.rect.x = self.gray.rect.x
        self.rect.y = self.gray.rect.x

    def update(self):
        self.rect = self.rect.move((-self.speed, 0))

        if self.rect.x <= 0:
            self.kill()
        if self.rect.x >= 1100:
            self.kill()


class Platform(Entity):
    def __init__(self, x, y, char):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.set_image(char)
        self.rect = Rect(x, y, 32, 32)

    def set_image(self, char):
        if char == "P":
            self.image = pygame.image.load("images/tile.jpg")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "S":
            self.image = pygame.image.load("images/Tile.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "I":
            self.image = pygame.image.load("images/IndoorTile.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()


class BackgroundPlatform(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, char):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32)).convert()
        self.set_image(char)
        self.rect = pygame.Rect(xpos, ypos, 32, 32)

    def set_image(self, char):
        if char == "F":
            self.image = pygame.image.load("images/fence.jpg")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "B":
            self.image = pygame.image.load("images/bush.jpg")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "N":
            self.image = pygame.image.load("images/black.jpg")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "C":
            self.image = pygame.image.load("images/Pillar.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "W":
            self.image = pygame.image.load("images/tile.jpg")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "L":
            self.image = pygame.image.load("images/Window.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "K":
            self.image = pygame.image.load("images/NOTAKECANDLE.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "T":
            self.image = pygame.image.load("images/door top.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "Z":
            self.image = pygame.image.load("images/bones.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "Q":
            self.image = pygame.image.load("images/knight1.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()
        elif char == "M":
            self.image = pygame.image.load("images/knight2.png")
            self.image = pygame.transform.scale(self.image, (32, 32)).convert()

class ExitBlock(Platform):
    def __init__(self, x, y, char):
        Platform.__init__(self, x, y, "E")
        self.image = pygame.image.load("images/door.png")
        self.image = pygame.transform.scale(self.image, (32, 32)).convert()

class ExitBlock2(Platform):
    def __init__(self, x, y, char):
        Platform.__init__(self, x, y, "E")
        self.image = pygame.image.load("images/door.png")
        self.image = pygame.transform.scale(self.image, (32, 32)).convert()


class ExitBlock3(Platform):
    def __init__(self, x, y, char):
        Platform.__init__(self, x, y, "E")
        self.image = pygame.image.load("images/door.png")
        self.image = pygame.transform.scale(self.image, (32, 32)).convert()

backgroundintroinage = pygame.image.load("images/oh the edge.jpg")
titleimage = pygame.image.load("images/title.png")
madeby = pygame.image.load("images/madeby.png")
story1 = pygame.image.load("images/story 1.jpg")
story2 = pygame.image.load("images/story 2.jpg")
story3 = pygame.image.load("images/story 3.jpg")
story4 = pygame.image.load("images/story 4.jpg")
grayintro = pygame.image.load("images/Gray intro.jpg")
clarify = pygame.image.load("images/to clarify.jpg")
GameOver = pygame.image.load("images/GameOver.png")
End = pygame.image.load("images/youwin.png")

pygame.mixer.init(44100, -16, 2, 2048)
music_intro = pygame.mixer.Sound("sound/Vampire Killer.ogg")
music_intro.play(-1)


music_2 = pygame.mixer.Sound("sound/Heart of Fire.ogg")
music_2.play(-1)
music_2.stop()

music_3 = pygame.mixer.Sound("sound/Wicked Child.ogg")
music_3.play(-1)
music_3.stop()

music_4 = pygame.mixer.Sound("sound/Bloody Tears.ogg")
music_4.play(-1)
music_4.stop()

level1 = [
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNPPP",
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNPPP",
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNPPP",
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNPPP",
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNPPP",
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNPPP",
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNSSSSPPP",
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNCNCNPPP",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBCBCBBBT",
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFCFCFFFE",
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFSSSSPPP",
    "FFFFFFFFFFFFFFFFFFFFFFFFFFSSSSSPPP",
    "FFFFFFFFFFFFFFFFFFFFFFFFFSSSSSSPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", ]
level2 = [
    "SSSSWWWWWWWWWWWCWWWWCWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWCWWWWCWWWSWWWWWWWWW",
    "WWWWWWWWWWWWWWWCWWWWCWWWWWWWWWWWWW",
    "WWWWWLLWWWWWWWWCWLLWCWWWWWWWWWLLWW",
    "WWWWWWWWWWWWWWWCWWWWCWWWWWWWWWWWWW",
    "WWWWWKKWWWWWWWWCWKKWCWWWWWWWWWKKWW",
    "WWWQWWWWWWWWWWWCWWWWCWWCWWWIIIWWWI",
    "WKWIIIIIIIIWWWWCWWWWCWWCWWWSSCWWWW",
    "WWWCWWWWCWWWWWWCWWWWCWWIWWWCSCWWWW",
    "WWWCWWWWCWWWWWWCWWWWCWWCWWWCSCWWWT",
    "IIICWWWWCWWWWWWIWWWWCWWCCWWWCSSWZE",
    "SWWCWLLWCKQWWWWWKLLWCWWWWWWCSSWSII",
    "SWWCZZWSSWMWWWWWWWWWCWWWWKWCSSSIII",
    "IIIIIIIIIISSWWWWWWWWCWWWWWWWSIIIII",
    "IIIIIIIIIIISWWWCWWWWCWWWWWWSIIIIII",
    "IIIIIIIIIIIISWWCWWWWCWWWWWSSIIIIII", ]
level3 = [

                "SWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "LLWWWWWWWCWWWWWWWWWKKWWKKWWKKWKKWT",
                "SWWWWZZWWCWWWWWWWWWZZZZZZZWWWWWWWE",
                "SSWWWIIIIIIISSSSSSSIIIIIIIIIIIIIII",
                "SWWWLLLLLCKKCWWWWSWWWWWWWWWWWWWWWS",
                "SWWWWWWWWCWWCWWWWSWWWWWWWWWWWWWISS",
                "SWWWIWWWWWWWCWWWWSWWWWWWWWWWWWWWWS",
                "SWWWWWWWWWWWCWWWWSWWWIWWWWWLLWWWWS",
                "SWWWWWWWWWWWCWWWWSWWWCWWWWWWWWWWWS",
                "SWWWWWWWWWWSIWWWWIWWWCWWWWWIWWWWWS",
                "SWWWWWLLWWWCWWWKWIWWWCWWWWWWWWWWWS",
                "SWWWWWWWWWWKKKKKKIWWWCWWWWWWWWCWWS",
                "SWWWWWSIWWWWWWWKWSWWICWWWWWWWWCWWS",
                "SWWWWWWWWWWCWWIWWSWWWCWWWWWWWWLLSS",
                "SWWWWWWWWWWCWWIWWSWWWCWWWWIWWWWWWS",
                "SWWWKKWWWWWCWIIWWWWWWWWWWWWWWWWWWS",
                "SWWWWWWWWWWCWWSWWZZZWCWWWWWWWWCWWS",
                "SWWWWWWWWIICWWSSIIISISIISIIISIIIIS",
                "SWWWWWWWWCWCWWWWWWWWWWWWWWWWWWWWWS",
                "SWWWWWWWWCWCWWWWWWWWLLWWWWWWWWWWWS",
                "SWIWWWWWWWWCWWWWWWWWWWWWWWWWWWWWWS",
                "SWIIWWWWWWLLWWWWWWWWWWWWWWWWWWWWWS",
                "SWWCWWWWWWWWWWWWWWWWWWWKKWWWWWWWWS",
                "SWWCWWWWWWWWWIWWWWWWWWWWWWWKKWWWWS",
                "SWWCWWWWWWWWWWWWWWWWWWWWWIIIIIIIWS",
                "SWWCWWWWWWWWWWWWWWWWWWWWWWCWWWWWCS",
                "SWWCWWWWKKWWWWWWWWWWWWWWWWCWWWWWCS",
                "SWWCWWWWWWWWWWWWWWWWWWWWIWCWWWWWCS",
                "SWWCWWWWWWWWWWWWWWWWWWWWIWCWLLQQCS",
                "SWWCWWWWWWWWWIIWWWWWWWWWIWCWWWMMCS",
                "SWWCWWWWWWWWWWWWWWWWWWWWIIIIIIIICS",
                "SWWIWWWWWWWWWWWWWWWWWWWWWWWWWWWWCS",
                "SWWWWWWWWWWWWWLLWWWWWWWWWWWWWWWWCS",
                "SWWWWWWWWWWWWWWCWWWWKKWWWWWWKWWWIS",
                "SWWWWWIWWWWWWWWCWWWWWWWWWWWWWWWWWS",
                "SWWWWWWWWWWWWWWCWWWWWWWWWWWWWWWWWS",
                "SWWWWWWWWWWWWWWCWWWWWWWIWWWWWWWWWS",
                "SWWWWWWWWWWWIWWCWWWWWWWCWWWWWWWWWS",
                "SWWWWWWWWWWWWWWCWWWWWWWCWWWWWWIWWS",
                "IWWWWWWIWWWWWWWCWWWWWWWCWWWWWWWWWS",
                "IWWWWWIIWWWWWWWCWWWWWWWCWWWWWWWWWS",
                "SWWWWWWCWWWWWWWIWWWWWWWCWIWWWWWWWS",
                "SWWWWWWCWWWWWWWIWWWWWWWWWWWWWWWWSS",
                "SWWWWWWCWWWWWWWIIWWWWWWWWWWWWWWWIW",
                "SWWWWWWCWWWWWWWWWWWWWWWIWWWIWWWWII",
                "SWWWWWWCWWWWWWWWWWWWWWWCWWWWWWWWWS",
                "SWWWWWWCWWWWWWWWWWIWWWWCWWWWWWWWWS",
                "SWWWWWWCWWWWWWWWWWWWWWWCWWWWWWWWWS",
                "SWWWWWWCWWWWWWWWWWWWWWWCIWWWWWWWSS",
                "SWWWWWWCWWWWWWWWWWWWWWWCLLWWWWWWWS",
                "SWWWWWWCWWWWWWWWWWWWKKWCZZWWWWWWWI",
                "SWWWWWWCWWWWWWWWWWWWIIIIIIWWWWWWWI",
                "SWWWWWWCWWWWWWWWWWWWCWWWWCWWWWWSSS",
                "SWWKKWWCIIIIIWWKKWWWCWWWWCWWZKKWSS",
                "SWWWWQMCCWZZCWWWWWWWCWWWMCWZSSSSSS",
                "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII", ]
level4 = [
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "WWWWWWWWWWWWWWWCWWWWCWWWSWWWWWWWWS",
    "WWWWWWWWWWWWWWWCWWWWCWWWWWWWWWWWWS",
    "WWWWWWWWWWWWWWWCWWWWCWWWWWWWWWWWWS",
    "WWWWWWWWWWWWWWWCWWWWCWWWWWWWWWWWWS",
    "WWWWWKKWWWWWWWWCWKKWCWWWWWWWWWKKWS",
    "WWWWWZZZWWWWWWWCWWWWCWWZWWWWWWCCCS",
    "WWWIIIIIIIIWWWWCWWWWCWWCWWWSSCWWWS",
    "WWWCWWWWCWWWWWWCWWWWCWWIWWWCSCWWWS",
    "WWWCWWWWCWWWWWWCWWWWCWWCZWWCSCZZWS",
    "IIICWWWWCWWWWWWIIIWWCWWCCWWZCSSSZS",
    "SWWCWWWWCWWWWWWWWWWWCWWWWWWCSSWSII",
    "SWWCWQWSSWWWWWWWWWWWCWWWWKWCSSSIII",
    "IIWCWMWWWWWWWWWZWWWWCWWWWWWWSIIIII",
    "IIIIIIIIIIISZZZCZZZZCWZZZZZSIIIIII",
    "IIIIIIIIIIIISSSSSSSSSSSSSSSSIIIIII", ]

pygame.init()

def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Dante Shadeaumire and the Return of Gray")
    timer = pygame.time.Clock()
    loop_counter = 0
    dest = (0, 0)
    fps = 60
    font = pygame.font.SysFont("Britannic Bold", 50)
    text = font.render('Click to Start', True, RED)
    text_rect = text.get_rect()
    text_rect = text_rect.move(WIN_WIDTH / 2 - text_rect.width, WIN_HEIGHT - text_rect.height)
    up = down = left = right = running = shooting = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    bullet2_group = pygame.sprite.Group()
    huey_group = pygame.sprite.Group()
    platforms = []
    num = "1"
    graygroup = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    run = Game(platforms, entities)


    while run.intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.intro = False
                run.madeby = True

        screen.blit(backgroundintroinage, dest)
        screen.blit(titleimage, dest)
        if pygame.time.get_ticks() % 1000 < 500:
            screen.blit(text, text_rect)
        timer.tick(fps)
        pygame.display.flip()

    while run.madeby:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.madeby = False
                run.storyp1 = True

        screen.blit(madeby, dest)
        timer.tick(fps)
        pygame.display.flip()

    while run.storyp1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.storyp1 = False
                run.storyp2 = True

        screen.blit(story1, dest)
        timer.tick(fps)
        pygame.display.flip()

    while run.storyp2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.storyp2 = False
                run.clarify = True

        screen.blit(story2, dest)
        timer.tick(fps)
        pygame.display.flip()

    while run.clarify:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.clarify = False
                run.play = True
                x = 0
                y = 0
                for row in level1:
                    for col in row:
                        if col == "P":
                            p = Platform(x, y, "P")
                            platforms.append(p)
                            entities.add(p)
                            x += 32
                        if col == "S":
                            s = Platform(x, y, "S")
                            platforms.append(s)
                            entities.add(s)
                            x += 32
                        if col == "F":
                            f = BackgroundPlatform(x, y, "F")
                            platform_group.add(f)
                            x += 32
                        if col == "C":
                            c = BackgroundPlatform(x, y, "C")
                            platform_group.add(c)
                            x += 32
                        if col == "N":
                            n = BackgroundPlatform(x, y, "N")
                            platform_group.add(n)
                            x += 32
                        if col == "B":
                            b = BackgroundPlatform(x, y, "B")
                            platform_group.add(b)
                            x += 32
                        if col == "E":
                            e = ExitBlock(x, y, "E")
                            platforms.append(e)
                            entities.add(e)
                            x += 32
                        if col == "I":
                            i = Platform(x, y, "I")
                            platforms.append(i)
                            entities.add(i)
                            x += 32
                        if col == "W":
                            w = BackgroundPlatform(x, y, "W")
                            platform_group.add(w)
                            x += 32
                        if col == "L":
                            l = BackgroundPlatform(x, y, "L")
                            platform_group.add(l)
                            x += 32
                        if col == "T":
                            t = BackgroundPlatform(x, y, "T")
                            platform_group.add(t)
                            x += 32
                        if col == "Q":
                            q = BackgroundPlatform(x, y, "Q")
                            platform_group.add(q)
                            x += 32
                        if col == "M":
                            m = BackgroundPlatform(x, y, "M")
                            platform_group.add(m)
                            x += 32
                    y += 32
                    x = 0
                container = pygame.Rect(0, 0, len(level1[0]) * 32, len(level1 * 32))
                total_level_width = len(level1[0]) * 32
                total_level_height = len(level1) * 32
                player = Dante(64, 416, container)
                entities.add(player)
                camera = Camera(complex_camera, total_level_width, total_level_height)
                zombie = Zombie(container, loop_counter, 600, 352)
                huey_group.add(zombie)
                zombie = Zombie(container, loop_counter, 500, 352)
                huey_group.add(zombie)


        screen.blit(clarify, dest)
        timer.tick(fps)
        pygame.display.flip()

    while run.play:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                running = True
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                running = True
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                shooting = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                shooting = False

        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)
        player.update(up, down, left, right, running, shooting, platforms, player, bullet_group, loop_counter, huey_group, run, bullet2_group, platform_group, num, graygroup)
        player.setimage(up, down, left, right, shooting)
        bullet_group.update()
        bullet2_group.update()

        if loop_counter % 40 == 0:
            bat = Bat(container)
            huey_group.add(bat)
        huey_group.update(bullet_group)

        for p in platform_group:
            screen.blit(p.image, camera.apply(p))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for b in bullet_group:
            screen.blit(b.image, camera.apply(b))
        for b2 in bullet2_group:
            screen.blit(b2.image, camera.apply(b2))
        for h in huey_group:
            screen.blit(h.image, camera.apply(h))

        pygame.display.update()
        loop_counter += 1

    while run.storyp3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                for p in entities:
                    p.kill()
                pygame.sprite.Group.empty(platform_group)
                pygame.sprite.Group.empty(entities)
                pygame.sprite.Group.empty(huey_group)
                pygame.sprite.Group.empty(bullet_group)
                run.storyp3 = False
                run.play2 = True
                player.kill()
                x = 0
                y = 0

                for p in platform_group:
                    p.kill()
                del platforms[:]
                for e in entities:
                    e.kill()

                for row in level2:
                    for col in row:
                        if col == "P":
                            p = Platform(x, y, "P")
                            platforms.append(p)
                            entities.add(p)
                            x += 32
                        if col == "S":
                            s = Platform(x, y, "S")
                            platforms.append(s)
                            entities.add(s)
                            x += 32
                        if col == "F":
                            f = BackgroundPlatform(x, y, "F")
                            platform_group.add(f)
                            x += 32
                        if col == "C":
                            c = BackgroundPlatform(x, y, "C")
                            platform_group.add(c)
                            x += 32
                        if col == "N":
                            n = BackgroundPlatform(x, y, "N")
                            platform_group.add(n)
                            x += 32
                        if col == "B":
                            b = BackgroundPlatform(x, y, "B")
                            platform_group.add(b)
                            x += 32
                        if col == "E":
                            e = ExitBlock2(x, y, "E")
                            platforms.append(e)
                            entities.add(e)
                            x += 32
                        if col == "I":
                            i = Platform(x, y, "I")
                            platforms.append(i)
                            entities.add(i)
                            x += 32
                        if col == "W":
                            w = BackgroundPlatform(x, y, "W")
                            platform_group.add(w)
                            x += 32
                        if col == "L":
                            l = BackgroundPlatform(x, y, "L")
                            platform_group.add(l)
                            x += 32
                        if col == "K":
                            k = BackgroundPlatform(x, y, "K")
                            platform_group.add(k)
                            x += 32
                        if col == "T":
                            t = BackgroundPlatform(x, y, "T")
                            platform_group.add(t)
                            x += 32
                        if col == "Z":
                            z = BackgroundPlatform(x, y, "Z")
                            platform_group.add(z)
                            x += 32
                        if col == "Q":
                            q = BackgroundPlatform(x, y, "Q")
                            platform_group.add(q)
                            x += 32
                        if col == "M":
                            m = BackgroundPlatform(x, y, "M")
                            platform_group.add(m)
                            x += 32
                    y += 32
                    x = 0
                container2 = pygame.Rect(0, 0, len(level2[0]) * 32, len(level2 * 32))
                total_level_width2 = len(level2[0]) * 32
                total_level_height2 = len(level2) * 32
                camera = Camera(complex_camera, total_level_width2, total_level_height2)
                player = Dante(64, 352, container2)
                entities.add(player)
                up = False
                down = False
                left = False
                running = False
                right = False
                shooting = False
                gargoyle = Gargoyle(container, loop_counter, 868, 200)
                huey_group.add(gargoyle)
                gargoylel = Gargoyleright(container, loop_counter, 300, 400)
                huey_group.add(gargoylel)
                zombie = Zombie(container, loop_counter, 325, 352)
                huey_group.add(zombie)

        screen.blit(story3, dest)
        pygame.display.flip()


# SECOND LEVEL


    while run.play2:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                running = True
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                running = True
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                shooting = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                shooting = False

        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        if loop_counter % 150 == 0:
            garbullet = GarBullet(gargoyle)
            bullet2_group.add(garbullet)
        if loop_counter % 150 == 0:
            garbulletr = GarBulletright(gargoylel)
            bullet2_group.add(garbulletr)

        camera.update(player)
        player.update(up, down, left, right, running, shooting, platforms, player, bullet_group, loop_counter, huey_group, run, bullet2_group, platform_group, num, graygroup)
        player.setimage(up, down, left, right, shooting)
        bullet_group.update()
        huey_group.update(bullet_group)
        bullet2_group.update()

        for p in platform_group:
            screen.blit(p.image, camera.apply(p))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for b in bullet_group:
            screen.blit(b.image, camera.apply(b))
        for b2 in bullet2_group:
            screen.blit(b2.image, camera.apply(b2))
        for h in huey_group:
            screen.blit(h.image, camera.apply(h))

        pygame.display.update()
        loop_counter += 1

    while run.storyp4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                pygame.sprite.Group.empty(platform_group)
                pygame.sprite.Group.empty(entities)
                pygame.sprite.Group.empty(huey_group)
                pygame.sprite.Group.empty(bullet_group)
                run.storyp4 = False
                run.play3 = True
                x = 0
                y = 0

                for p in platform_group:
                    p.kill()
                del platforms[:]
                for e in entities:
                    e.kill()

                for row in level3:
                    for col in row:
                        if col == "P":
                            p = Platform(x, y, "P")
                            platforms.append(p)
                            entities.add(p)
                            x += 32
                        if col == "S":
                            s = Platform(x, y, "S")
                            platforms.append(s)
                            entities.add(s)
                            x += 32
                        if col == "F":
                            f = BackgroundPlatform(x, y, "F")
                            platform_group.add(f)
                            x += 32
                        if col == "C":
                            c = BackgroundPlatform(x, y, "C")
                            platform_group.add(c)
                            x += 32
                        if col == "N":
                            n = BackgroundPlatform(x, y, "N")
                            platform_group.add(n)
                            x += 32
                        if col == "B":
                            b = BackgroundPlatform(x, y, "B")
                            platform_group.add(b)
                            x += 32
                        if col == "E":
                            e = ExitBlock3(x, y, "E")
                            platforms.append(e)
                            entities.add(e)
                            x += 32
                        if col == "I":
                            i = Platform(x, y, "I")
                            platforms.append(i)
                            entities.add(i)
                            x += 32
                        if col == "W":
                            w = BackgroundPlatform(x, y, "W")
                            platform_group.add(w)
                            x += 32
                        if col == "L":
                            l = BackgroundPlatform(x, y, "L")
                            platform_group.add(l)
                            x += 32
                        if col == "K":
                            k = BackgroundPlatform(x, y, "K")
                            platform_group.add(k)
                            x += 32
                        if col == "T":
                            t = BackgroundPlatform(x, y, "T")
                            platform_group.add(t)
                            x += 32
                        if col == "Z":
                            z = BackgroundPlatform(x, y, "Z")
                            platform_group.add(z)
                            x += 32
                        if col == "Q":
                            q = BackgroundPlatform(x, y, "Q")
                            platform_group.add(q)
                            x += 32
                        if col == "M":
                            m = BackgroundPlatform(x, y, "M")
                            platform_group.add(m)
                            x += 32
                    y += 32
                    x = 0
                container3 = pygame.Rect(0, 0, len(level3[0]) * 32, len(level3 * 32))
                total_level_width3 = len(level3[0]) * 32
                total_level_height3 = len(level3) * 32
                camera = Camera(complex_camera, total_level_width3, total_level_height3)
                player = Dante(64, 1768, container3)
                entities.add(player)
                up = False
                down = False
                left = False
                running = False
                right = False
                shooting = False
                gargoyle = Gargoyle(container, loop_counter, 1024, 150)
                huey_group.add(gargoyle)
                gargoylel = Gargoyleright(container, loop_counter, 0, 336)
                huey_group.add(gargoylel)
                gargoyle2 = Gargoyle(container, loop_counter, 1024, 100)
                huey_group.add(gargoyle2)
                gargoylel2 = Gargoyleright(container, loop_counter, 0, 300)
                huey_group.add(gargoylel)

        screen.blit(story4, dest)
        pygame.display.flip()


            # THIRD LEVEL

        while run.play3:
            timer.tick(60)

            for e in pygame.event.get():
                if e.type == QUIT:
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    running = True
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    running = True
                    right = True
                if e.type == KEYDOWN and e.key == K_SPACE:
                    shooting = True
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_SPACE:
                    shooting = False

            for y in range(32):
                for x in range(32):
                    screen.blit(bg, (x * 32, y * 32))

            if loop_counter % 150 == 0:
                garbullet = GarBullet(gargoyle)
                bullet2_group.add(garbullet)
                garbullet2 = GarBullet(gargoyle2)
                bullet2_group.add(garbullet2)
            if loop_counter % 150 == 0:
                garbulletr = GarBulletright(gargoylel)
                bullet2_group.add(garbulletr)
                garbulletr2 = GarBullet(gargoylel2)
                bullet2_group.add(garbulletr2)
            camera.update(player)
            player.update(up, down, left, right, running, shooting, platforms, player, bullet_group, loop_counter,
                          huey_group, run, bullet2_group, platform_group, num, graygroup)
            player.setimage(up, down, left, right, shooting)
            bullet_group.update()
            huey_group.update(bullet_group)
            bullet2_group.update()

            for p in platform_group:
                screen.blit(p.image, camera.apply(p))
            for e in entities:
                screen.blit(e.image, camera.apply(e))
            for b in bullet_group:
                screen.blit(b.image, camera.apply(b))
            for b2 in bullet2_group:
                screen.blit(b2.image, camera.apply(b2))
            for h in huey_group:
                screen.blit(h.image, camera.apply(h))

            pygame.display.update()
            loop_counter += 1

    while run.story5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                pygame.sprite.Group.empty(platform_group)
                pygame.sprite.Group.empty(entities)
                pygame.sprite.Group.empty(huey_group)
                pygame.sprite.Group.empty(bullet_group)

                run.story5 = False
                run.play4 = True
                x = 0
                y = 0

                for p in platform_group:
                    p.kill()
                del platforms[:]
                for e in entities:
                    e.kill()
                for b2 in bullet2_group:
                    b2.kill()
                for row in level4:
                    for col in row:
                        if col == "P":
                            p = Platform(x, y, "P")
                            platforms.append(p)
                            entities.add(p)
                            x += 32
                        if col == "S":
                            s = Platform(x, y, "S")
                            platforms.append(s)
                            entities.add(s)
                            x += 32
                        if col == "F":
                            f = BackgroundPlatform(x, y, "F")
                            platform_group.add(f)
                            x += 32
                        if col == "C":
                            c = BackgroundPlatform(x, y, "C")
                            platform_group.add(c)
                            x += 32
                        if col == "N":
                            n = BackgroundPlatform(x, y, "N")
                            platform_group.add(n)
                            x += 32
                        if col == "B":
                            b = BackgroundPlatform(x, y, "B")
                            platform_group.add(b)
                            x += 32
                        if col == "E":
                            e = ExitBlock3(x, y, "E")
                            platforms.append(e)
                            entities.add(e)
                            x += 32
                        if col == "I":
                            i = Platform(x, y, "I")
                            platforms.append(i)
                            entities.add(i)
                            x += 32
                        if col == "W":
                            w = BackgroundPlatform(x, y, "W")
                            platform_group.add(w)
                            x += 32
                        if col == "L":
                            l = BackgroundPlatform(x, y, "L")
                            platform_group.add(l)
                            x += 32
                        if col == "K":
                            k = BackgroundPlatform(x, y, "K")
                            platform_group.add(k)
                            x += 32
                        if col == "T":
                            t = BackgroundPlatform(x, y, "T")
                            platform_group.add(t)
                            x += 32
                        if col == "Z":
                            z = BackgroundPlatform(x, y, "Z")
                            platform_group.add(z)
                            x += 32
                        if col == "Q":
                            q = BackgroundPlatform(x, y, "Q")
                            platform_group.add(q)
                            x += 32
                        if col == "M":
                            m = BackgroundPlatform(x, y, "M")
                            platform_group.add(m)
                            x += 32
                    y += 32
                    x = 0
                container4 = pygame.Rect(0, 0, len(level4[0]) * 32, len(level3 * 32))
                total_level_width4 = len(level4[0]) * 32
                total_level_height4 = len(level4) * 32
                camera = Camera(complex_camera, total_level_width4, total_level_height4)
                player = Dante(64, 416, container4)
                entities.add(player)
                up = False
                down = False
                left = False
                running = False
                right = False
                shooting = False
                gray = Gray(500, 300, container, loop_counter)
                gray.add(graygroup)

        screen.blit(grayintro, dest)
        pygame.display.flip()

    while run.play4:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                running = True
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                running = True
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                shooting = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                shooting = False

        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))
        if loop_counter % 40:
            slash = Bullet2(gray)
            bullet2_group.add(slash)

        camera.update(player)
        player.update(up, down, left, right, running, shooting, platforms, player, bullet_group, loop_counter,
                      huey_group, run, bullet2_group, platform_group, num, graygroup)
        player.setimage(up, down, left, right, shooting)
        bullet_group.update()
        huey_group.update(bullet_group)
        bullet2_group.update()
        graygroup.update(bullet_group, run)


        for p in platform_group:
            screen.blit(p.image, camera.apply(p))
        for h in huey_group:
            screen.blit(h.image, camera.apply(h))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for b in bullet_group:
            screen.blit(b.image, camera.apply(b))
        for b2 in bullet2_group:
            screen.blit(b2.image, camera.apply(b2))
        for g in graygroup:
            screen.blit(g.image, camera.apply(g))

        pygame.display.update()
        loop_counter += 1

    while run.outro:
        music_2.stop()
        music_3.stop()
        music_4.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                main()
                music_intro = pygame.mixer.Sound("sound/Vampire Killer.ogg")
                music_intro.play(-1)
        screen.blit(GameOver, dest)
        timer.tick(fps)
        pygame.display.flip()

    while run.end:
        music_2.stop()
        music_3.stop()
        music_4.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        screen.blit(End, dest)
        timer.tick(fps)
        pygame.display.flip()


if __name__ == "__main__":
    main()
