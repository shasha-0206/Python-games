import pygame
import random

pygame.init()

score = 0

def bricks_create():
    colours = ['#35e9f2', 'red', 'green']
    bricks = []  
    brick_w = 47
    brick_h = 20
    brick_x = 5
    brick_y = 0
    for colour in colours:
        for _ in range(2):
            for _ in range(10):
                bricks.append((brick_x, brick_y, colour))  
                brick_x += (brick_w + 2)
            brick_x = 5
            brick_y += (brick_h + 2)
    return bricks

def collision(ball_x, ball_y, p_x, p_y, p_w, ball_vel_x, ball_vel_y, screen_width, ball_radius, bricks):
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_vel_x = -ball_vel_x
    
    if ball_y - ball_radius <= 0:
        ball_vel_y *= -1
    
    if p_y <= ball_y + ball_radius <= p_y + 5 and p_x <= ball_x <= p_x + p_w:
        ball_vel_y *= -1
    
    # on collision removes brick
    global score
    for i in bricks[:]:
        brick_x, brick_y, _ = i
        if (brick_x <= ball_x <= brick_x + 47) and (brick_y <= ball_y <= brick_y + 20):
            ball_vel_y *= -1
            bricks.remove(i)
            score += 1
            
    return ball_vel_x, ball_vel_y

def gameloop():
    # game variables
    clock = pygame.time.Clock()
    game_end = False
    screen_width = 500
    screen_height = 500

    p_w = 80 
    p_h = 10 
    p_x = 200 
    p_y = 470 
    vel_x = 10

    ball_x = 225
    ball_y = 460
    ball_vel_x = 5
    ball_vel_y = 5
    ball_radius = 8

    game_window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('BREAKOUT')

    bricks = bricks_create()  # Create bricks list

    # highscore initialisation
    highscore = 0
    with open (r"C:\Users\malkh\Desktop\Python-Games\breakout\assets\highscore_breakout.txt","r") as f:
        highscore = int(f.read())

    while not game_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    game_end = True
                                   
        bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\breakout\assets\Screenshot 2024-05-10 143404.png")
        game_over_bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\breakout\assets\Screenshot 2024-05-29 140143.png")
        game_over_bg = pygame.transform.scale(game_over_bg,(screen_width,screen_height))

        game_window.blit(bg,(0,0))
        pygame.draw.rect(game_window, 'white', (p_x, p_y, p_w, p_h))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and p_x >= 20:
            p_x -= vel_x
        elif keys[pygame.K_d] and p_x <= (screen_width - p_w - 20):
            p_x += vel_x

        # drawing bricks
        for brick in bricks:
            brick_x, brick_y, brick_color = brick
            pygame.draw.rect(game_window, brick_color, (brick_x, brick_y, 47, 20))

        # updating velx and vely values when collision occurs
        ball_vel_x, ball_vel_y = collision(ball_x, ball_y, p_x, p_y, p_w, ball_vel_x, ball_vel_y, screen_width, ball_radius, bricks)
        ball_x += ball_vel_x
        ball_y += ball_vel_y
        
        # drawing ball
        pygame.draw.circle(game_window, 'white', (ball_x, ball_y), ball_radius)

        # updating highscore
        if score > highscore:
            highscore = score
            with open (r"C:\Users\malkh\Desktop\Python-Games\breakout\assets\highscore_breakout.txt","w") as f:
                f.write(str(highscore))

        # gameover bg 
        if ball_y >= screen_height:
            game_window.blit(game_over_bg, (0, 0))
            pygame.display.update()
            pygame.time.wait(3000)

        # displaying score
        score_text = pygame.font.SysFont('bold',50)
        score_display = score_text.render("Score: " + str(score),True,'white')
        game_window.blit(score_display,(200,250))
    
        # displaying highscore
        highscore_text = pygame.font.SysFont('bold',50)
        highscore_display = highscore_text.render('Highscore: ' + str(highscore),True,'white')
        game_window.blit(highscore_display,(175,300))

        pygame.display.update()
        clock.tick(30)
gameloop()
pygame.quit()
