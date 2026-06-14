import sys
import pygame
import random
import math

pygame.mixer.pre_init()
pygame.init()

#music
pygame.mixer.music.load("assets/sounds/bg_sound.mp3")
pygame.mixer.music.play(-1)
bullet_sound=pygame.mixer.Sound("assets/sounds/gun_shot.mp3")
collision_sound=pygame.mixer.Sound("assets/sounds/collision.mp3")

#screen dimension
WIDTH, HEIGHT= 800,600
screen= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space War Game")

#image load
bg_image=pygame.transform.scale(pygame.image.load("assets/imgs/HkaoI.png"),(WIDTH,HEIGHT))
player_image=pygame.transform.scale(pygame.image.load("assets/imgs/spaceship_2.png"),(64,64))
player_bullet_img=pygame.transform.scale(pygame.image.load("assets/imgs/bullet_1.png"),(32,32))
enemy_img1=pygame.transform.scale(pygame.image.load("assets/imgs/enemy_3.png"),(32,32))
enemy_img2=pygame.transform.scale(pygame.image.load("assets/imgs/enemy_2.png"),(32,32))
enemy_img3=pygame.transform.scale(pygame.image.load("assets/imgs/enemy_4.png"),(32,32))
collision_img1=pygame.transform.scale(pygame.image.load("assets/imgs/explosion_2.png"),(32,32))

#location
player_x=WIDTH//2-32
player_y=HEIGHT-80

#Multi_element
player_bullets=[] #(bullet_x,bullet_y)
enemies=[]
collisions=[]

#FPS
FPS=60
clock=pygame.time.Clock()

#game
game_over=False

#score
score=0

#font
font=pygame.font.SysFont("Arial", 36)
def player_controller(pressed_keys):
    global player_x,player_y

    pressed_keys=pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        player_x -= 3
    if pressed_keys[pygame.K_RIGHT]:
        player_x += 3

    if player_x<0:
        player_x=0
    elif player_x>WIDTH-64:
        player_x=WIDTH-64

    screen.blit(player_image, (player_x, player_y))
def player_bullet_controller():
    global player_bullets

    for bullet in player_bullets:
        bullet["y"] -= 5
        if bullet["y"] < -32:
            player_bullets.remove(bullet)

        screen.blit(player_bullet_img, (bullet["x"], bullet["y"]))
def enemy_controller():
    global enemies
    if random.randint(1, 30) == 1:
        x = random.randrange(0, WIDTH - 32)
        y = 0
        dx = random.randint(-3, 3)
        dy = random.randint(2, 6)
        img=enemy_img1 if random.randint(0,1)==1 else enemy_img2
        enemies.append(
            {
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "img": img
            }
        )
    for enemy in enemies:
        screen.blit(enemy.get('img'), (enemy.get('x'), enemy.get('y')))
        enemy['x'] += enemy['dx']
        enemy['y'] += enemy['dy']

        if enemy['y']>HEIGHT:
            enemies.remove(enemy)
def enemy_kill_controller():
    global player_bullets,enemies,score
    for bullet in player_bullets:
        for enemy in enemies:
            if is_kill(bullet["x"]+16, bullet["y"]+16, enemy["x"]+16, enemy["y"]+16,threshold=20):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                collisions.append(
                    {
                        "x": enemy["x"],
                        "y": enemy["y"],
                        "tick": pygame.time.get_ticks()
                    }
                )
                score += 1
                collision_sound.play()

    for c in collisions:
        if pygame.time.get_ticks() - c["tick"] < 500:
            screen.blit(collision_img1, (c["x"], c["y"]))
        else:
            collisions.remove(c)

def player_collision_controller():
    global game_over
    for e in enemies:
        if is_kill(player_x + 32, player_y + 32, e["x"] + 16, e["y"] + 16, threshold=25):
            game_over = True

def is_kill(x1,y1,x2,y2,threshold=30):
    d=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return d<=threshold

def draw_text(text,x,y,color=(255,255,255)):
    img=font.render(text, True, color)
    screen.blit(img, (x, y))

def game_loop():
    while True:
        screen.blit(bg_image,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player_bullets.append(
                        {
                        "x":player_x+16,
                        "y":player_y-16
                        }
                    )
                    bullet_sound.play()


        pressed_keys=pygame.key.get_pressed()
        player_controller(pressed_keys)
        player_bullet_controller()
        enemy_controller()
        enemy_kill_controller()
        player_collision_controller()
        draw_text(f"Score: {score}", 10,10)

        if game_over:
            draw_text(f"Game Over...! Score: {score}",WIDTH//2-150, HEIGHT//2-40)
            draw_text(f"Press ESC to Quit", WIDTH//2-150, HEIGHT//2)
            pygame.display.flip()
            if pressed_keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        clock.tick(FPS)

#Call_main_ Game Loop
game_loop()