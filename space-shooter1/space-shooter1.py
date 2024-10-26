import pygame
import random

pygame.init()

def bullet_game():
    pygame.init()
    clock = pygame.time.Clock()

    # setting game window
    screen_width = 900
    screen_height = 500
    game_window = pygame.display.set_mode((screen_width, screen_height))

    # graphics
    bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter1\assets\bg.jpeg")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

    game_over_bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter1\assets\gettyimages-1325433246-640x640.jpg")
    game_over_bg = pygame.transform.scale(game_over_bg,(screen_width,screen_height))

    # game title
    pygame.display.set_caption('Second game')

    # bullet
    bullet = []
    bullet_width = 10
    bullet_height = 20

    def create_bullets(bullet,bool):
        game_over = bool
        for bullets in bullet:
            if game_over == False:
                pygame.draw.rect(game_window,'white',bullets)

    # highest time initialisation
    highest_time = 0
    with open(r"C:\Users\malkh\Desktop\Python-Games\space-shooter1\assets\highscore_bullet.txt",'r') as f:
       highest_time = int(f.read())

    # gameloop
    def game_loop_2():
        # game variable
        nonlocal highest_time
        game_over = False
        player_width = 30
        player_height = 50
        x = 450
        y = screen_height - player_height
        game_end = False
        start_time = pygame.time.get_ticks()

        while not game_end:        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: 
                        pygame.quit()
                        
            # displaying background
            game_window.blit(bg, (0, 0))

            # time / score
            time = (pygame.time.get_ticks() - start_time) // 1000
            score_text = pygame.font.SysFont('bold',30)
            time_score = score_text.render("TIME: " + str(time),True,'white')
            game_window.blit(time_score,(10,10))

            # updating highscore 
            if time > highest_time:
                highest_time = time
                with open(r"C:\Users\malkh\Desktop\Python-Games\space-shooter1\assets\highscore_bullet.txt",'w') as f:
                    f.write(str(highest_time))
            
            # displaying highscore
            highest_time_text = pygame.font.SysFont('bold',30)
            highest_time_display = highest_time_text.render("Highest time: " + str(highest_time),True,'white')
            game_window.blit(highest_time_display,(730,10))

            # spaceship
            spaceship = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter1\assets\spaceship.png")
            spaceship = pygame.transform.scale(spaceship,(player_width,player_height))
            game_window.blit(spaceship,(x,y))

            # binding
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if x <= 10:
                    x -= 0
                else:
                    x -= 10
            elif keys[pygame.K_d]:
                if x + (player_width + 10) >= screen_width:
                    x += 0
                else:
                    x += 10

            # if the number genrated is less than five then it runs
            if random.randint(0,100) < 5:  # to control frequency of the bullets
                for i in range (3):  # to control frequency of the bullets
                    bullet_x = random.randint(20, screen_width - bullet_width) # randomly plcaing the bullets
                    bullets = pygame.Rect(bullet_x,-bullet_height,bullet_width,bullet_height)
                    bullet.append(bullets)


            for bullets in bullet[:]:
                bullets.y += 5  # to make the bullets come down
                if  bullets.y > screen_height: #removin the bullets which exit the screen
                    bullet.remove(bullets)
                elif bullets.colliderect(pygame.Rect(x, y, player_width, player_height)):
                        game_over = True

            if game_over:
                game_window.blit(game_over_bg,(0,0))
                pygame.display.update()

            create_bullets(bullet,game_over)

            pygame.display.update()
            clock.tick(30)

    game_loop_2()
    pygame.quit()
bullet_game()
