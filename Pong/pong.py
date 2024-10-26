import pygame
import random

def gameloop():
    pygame.init() 
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # game variable
    screen_width = 800
    screen_height = 600
    
    pygame.display.set_caption("Pong")
    game_window = pygame.display.set_mode((screen_width,screen_height))

    # ball variables
    radius = 15
    r_x = 250
    r_y = 250
    velocity_x = 8
    velocity_y = 8

    # paddel variables
    p_width = 30
    p_height = 80
    p_x = (screen_width - p_width - 40)
    p_y = (screen_height ) // 2
    p2_x = (p_width + 20)
    p2_y = (screen_height) // 2

    def movement():
        nonlocal p_y,p2_y,r_y #since the whole code is in a function we cant change the value of varibale so we have to amke it a nonlocal
        keys = pygame.key.get_pressed()

        if multiplayer == True:

            if keys[pygame.K_w] and p2_y >= 0:
                p2_y -= 15 
            if keys[pygame.K_s] and p2_y <= (screen_height - p_height - 10):
                p2_y += 15 
            if keys[pygame.K_UP] and p_y >= 0:
                p_y -= 15 
            if keys[pygame.K_DOWN] and p_y <= (screen_height - p_height - 10):
                p_y += 15 

        if single_player == True:
            # automatic paddle movement
            if p2_y < r_y:
                p2_y += 7
            elif p2_y > r_y:
                p2_y -= 7
            
            # for kepping the paddle inside the screen boundaries
            if p2_y < 0:
                p2_y = 0
            elif p2_y > screen_height - p_height:
                p2_y = screen_height - p_height

            if keys[pygame.K_UP] and p_y >= 0:
                p_y -= 15 
            if keys[pygame.K_DOWN] and p_y <= (screen_height - p_height - 10):
                p_y += 15 

    def drawing():
        # drawing paddel player 2
        pygame.draw.rect(game_window,'#ee322c',(p_x,p_y,p_width,p_height))

        # seconds paddel player 2
        pygame.draw.rect(game_window,'#ee322c',(p2_x,p2_y,p_width,p_height))

        # drawing ball
        pygame.draw.circle(game_window,'#ee622c',(r_x,r_y),radius)

        # drawing line
        pygame.draw.line(game_window, 'white', (screen_width // 2, 0), (screen_width // 2, screen_height), 5)

        movement()

    def collision(ball_rect,paddle_rect,paddle2_rect):
        nonlocal velocity_x
        if ball_rect.colliderect(paddle_rect) or ball_rect.colliderect(paddle2_rect):
            velocity_x = -velocity_x
            pygame.mixer.music.load(r"C:\Users\malkh\Desktop\Python-Games\Pong\assets\mixkit-game-ball-tap-2073.wav")
            pygame.mixer.music.play()

    pause = False
    score = 0
    score2 = 0
    game_over = False
    single_player = False
    multiplayer = False
    selection = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # for quitting the game
                    game_over = True
                if event.key == pygame.K_p: # for pausing the game
                    pause = not pause # toggling so now p can be used to pause and pause 
                if event.key == pygame.K_r: # for restarting the game
                    gameloop()
                if event.key == pygame.K_1:
                    single_player = True
                    selection = True
                if event.key == pygame.K_2:
                    multiplayer = True
                    selection = True

        # a small selection menu
        if not selection:
            game_window.fill('#002633')
            select_font = pygame.font.SysFont('bold',50)
            select_display = select_font.render("Click 1 for single player",True,'white')
            select_display2 = select_font.render("Click 2 for multiplayer",True,'white')
            game_window.blit(select_display,(250,screen_height//2))
            game_window.blit(select_display2,(250,350))
            pygame.display.update()
        else:
            game_window.fill('#002633')

            # movement
            if not pause:
                r_x += velocity_x
                r_y += velocity_y
                if r_y >= (screen_height - radius - 10) or r_y <= radius:
                    velocity_y = -velocity_y
                    pygame.mixer.music.load(r"C:\Users\malkh\Desktop\Python-Games\Pong\assets\mixkit-game-ball-tap-2073.wav")
                    pygame.mixer.music.play()

                # should place these here then only the collisioin will work
                # cause x and y values will be updated and collision wont work as expected will see a shaking effect
                ball_rect = pygame.Rect(r_x,r_y,radius,radius)
                paddle_rect = pygame.Rect(p_x,p_y,p_width,p_height)
                paddle2_rect = pygame.Rect(p2_x,p2_y,p_width,p_height)

                # drawing()
                collision(ball_rect,paddle_rect,paddle2_rect)

                # for different direction after each miss 
                direction = [-velocity_x,velocity_y,velocity_x,-velocity_y]

                # recentering the ball after it crosses the right edge
                if r_x >= (screen_width - radius):
                    r_x = screen_width // 2
                    r_y = screen_height // 2
                    pygame.mixer.music.load(r"C:\Users\malkh\Desktop\Python-Games\Pong\assets\error-5-199276.mp3")
                    pygame.mixer.music.play()
                    velocity_x = random.choice(direction) #random direction everytime 
                    score += 1 # updating score 

                # recentering the ball after it crosses the left edge
                if r_x <= radius:
                    r_x = screen_width // 2
                    r_y = screen_height // 2
                    pygame.mixer.music.load(r"C:\Users\malkh\Desktop\Python-Games\Pong\assets\error-5-199276.mp3")
                    pygame.mixer.music.play()
                    velocity_x = random.choice(direction) #random direction everytime 
                    score2 += 1 # updating score 

            drawing()

            # displaying player one score
            score_font = pygame.font.SysFont('bold',80)
            score_display = score_font.render(str(score),True,'white')
            game_window.blit(score_display,(screen_width//2 - 100,screen_height//2))

            # displaying player two score
            score2_font = pygame.font.SysFont('bold',80)
            score2_display = score2_font.render(str(score2),True,'white')
            game_window.blit(score2_display,(screen_width//2 + 80,screen_height//2))


            if pause:
                pause_text = pygame.font.SysFont('bold',80)
                pause_display = pause_text.render('PAUSED',True,'#ee622c')
                game_window.blit(pause_display,(300,200))

            pygame.display.update()
            clock.tick(30)

    pygame.quit()

gameloop()
