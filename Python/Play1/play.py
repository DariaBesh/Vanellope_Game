import pygame

clock =pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((700 ,450))
pygame.display.set_caption("Vanellope")

icon = pygame.image.load('Play1/png player/icon.png').convert_alpha()
boss_x = 705
pygame.display.set_icon(icon)

bg = pygame.image.load('Play1/png player/bg7.png').convert()

walk_left = [
    pygame.image.load('Play1/left/player1_left.png').convert_alpha(),
    pygame.image.load('Play1/left/player2_left.png').convert_alpha(),
    pygame.image.load('Play1/left/player3_left.png').convert_alpha(),
    pygame.image.load('Play1/left/player4_left.png').convert_alpha(),
    pygame.image.load('Play1/left/player5_left.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('Play1/right/player1_right.png').convert_alpha(),
    pygame.image.load('Play1/right/player2_right.png').convert_alpha(),
    pygame.image.load('Play1/right/player3_right.png').convert_alpha(),
    pygame.image.load('Play1/right/player4_right.png').convert_alpha(),
    pygame.image.load('Play1/right/player5_right.png').convert_alpha(),
]

boss = pygame.image.load('Play1/Boss/Boss.png').convert_alpha()
boss_list_in_game =[]

player_anim_count = 0
bg_x = 0 

player_speed = 5
player_x = 150
player_y = 340

is_jump = False
jump_count = 9

bg_sound = pygame.mixer.Sound('Play1/Music/music.mp3')
bg_sound.play(-1)

boss_timer = pygame.USEREVENT + 1
pygame.time.set_timer(boss_timer, 2600)

label = pygame.font.Font('Play1/font.ttf', 50)
lose_label = label.render('Game over!',False , (255,182,193))
restart_label = label.render('Play again!',False , (255,105,180))
restart_label_rect = restart_label.get_rect(topleft=(200 , 250))

bullets_left = 7
bullet = pygame.image.load('Play1/bullet.png').convert_alpha()
bullets = []

gameplay = True

WHITE = (255, 255, 255)

def draw_text(text, label, color, surface, x, y):
    textobj =  label.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

running = True
while running:

    screen.blit(bg , (bg_x ,0))
    screen.blit(bg , (bg_x + 1080,0))
    
    draw_text(f'Bullet: {bullets_left}', label, WHITE, screen, 1, 1)

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x , player_y))
        boss_rect = boss.get_rect(topleft=(boss_x , 320))
        
        if boss_list_in_game:
            for (i ,el) in enumerate(boss_list_in_game):
                screen.blit(boss, el)
                el.x -= 10
                
                if el.x < -10 :
                    boss_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count] , (player_x,player_y ))
        else:
            screen.blit(walk_right[player_anim_count] , (player_x, player_y))

        if not is_jump:
            if keys[pygame.K_w]:
                is_jump = True
        else:
            if jump_count >= -9 :
                if jump_count > 0 :
                    player_y -= (jump_count **2) / 2
                else:
                    player_y += (jump_count **2) / 2
                jump_count -= 1
            else :
                is_jump = False
                jump_count = 9

        keys = pygame.key.get_pressed()  
        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed  
        elif keys[pygame.K_d]and player_x < 350:
            player_x += player_speed  

        if player_anim_count == 4 :
            player_anim_count = 0 
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -1080 :
            bg_x = 0
        
        if bullets :
            for (i , el) in enumerate (bullets):
                screen.blit(bullet, (el.x , el.y))
                el.x += 4
        
                if el.x > 700:
                    bullets.pop(i)
                
                if boss_list_in_game:
                    for (index, boss_el) in enumerate(boss_list_in_game):
                        if el.colliderect(boss_el):
                            boss_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((72,61,139))
        screen.blit(lose_label , (200 , 150))
        screen.blit(restart_label , (restart_label_rect))
        
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            boss_list_in_game.clear()
            bullets.clear()
            bullets_left = 7


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == boss_timer:
            boss_list_in_game.append(boss.get_rect(topleft =(700,320)))
        if gameplay and  event.type == pygame.KEYUP and event.key == pygame.K_e and bullets_left > 0 :
                bullets.append(bullet.get_rect(topleft=(player_x +30 , player_y +10)))
                bullets_left -=1

    clock.tick(15)

    boss_timer