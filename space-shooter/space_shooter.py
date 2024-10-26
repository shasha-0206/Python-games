import pygame
import random
import time

def gameloop():
    pygame.init()

    # game variable
    game_over = False
    game_end = False
    clock = pygame.time.Clock()
    screen_width = 1000
    screen_height = 750
    pygame.display.set_caption('Space Shooter')
    game_window = pygame.display.set_mode((screen_width,screen_height))

    # ship details
    ship_width = 80
    ship_height = 80
    ship_x = 500
    ship_y = screen_height - (ship_height + 10)

    # laser details
    laser_width = 20
    laser_height = 80

    # meteor details
    meteor_width = 40
    meteor_height = 40

    meteors_list = []
    def create_meteros(num):
        nonlocal game_end
        if game_end == False:
            for i in range(num):
                meteor_x = random.randint(0,screen_width - 50)
                meteor_y = random.randint(-80,0)
                meteors_list.append([meteor_x,meteor_y])

    def create_stars(num):
        stars = []
        for i in range(num):
            x = random.randint(0,screen_width - 10)
            y = random.randint(0,screen_height - 10)
            stars.append([x,y])
        return stars
            
    creation = create_stars(30)

    # game graphics
    bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\shooterbg.png")
    stars_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\star.png")
    ship_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\player.png")

    meteor_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\meteor.png")
    laser_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\laser.png")
    special_laser_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\special_laser.png")
    heart_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\heart.png")
    game_over_bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\2134714.jpg")
    explotion_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\explosion.png")

    explotion_pic = pygame.transform.scale(explotion_pic,(40,40))
    game_over_bg = pygame.transform.scale(game_over_bg,(screen_width,screen_width))
    heart_pic = pygame.transform.scale(heart_pic,(30,30))
    special_laser_pic = pygame.transform.scale(special_laser_pic,(50,laser_height))
    laser_pic = pygame.transform.scale(laser_pic,(laser_width,laser_height))
    meteor_pic = pygame.transform.scale(meteor_pic,(meteor_width,meteor_height))
    bg = pygame.transform.scale(bg,(screen_width,screen_height))
    ship_pic = pygame.transform.scale(ship_pic,(ship_width,ship_height))
    
    hearts = []
    def creat_heart():
        heart_x = 850
        for i in range(3):
            heart_x += 35
            heart_y = 10
            hearts.append([heart_x,heart_y])

    special_lasers=[]
    def create_sl(num):
        for i in range(num):
            special_x = ship_x
            special_y = ship_y -50
            special_lasers.append([special_x,special_y])

    lasers = []
    def create_laser(num):
        for i in range (num):
            laser_x = ship_x
            laser_y = ship_y - 50
            lasers.append([laser_x,laser_y])
            
    def movement():
        nonlocal ship_x,ship_y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and ship_x >= 0:
            ship_x -= 5 
        if keys[pygame.K_d] and ship_x <= (screen_width - ship_width):
            ship_x += 5
        if keys[pygame.K_w] and ship_y >= 0:
            ship_y -= 5
        if keys[pygame.K_s] and ship_y <= (screen_height - ship_height):
            ship_y += 5

    explosions = []
    def collision(ship_rect): 
        nonlocal game_end
        for met in meteors_list[:]:
            meteor_rect = pygame.Rect(met[0],met[1],meteor_width,meteor_height)
            for j in lasers[:]:
                laser_rect = pygame.Rect(j[0],j[1],laser_width,laser_height)
                if meteor_rect.colliderect(laser_rect):
                    meteors_list.remove(met)
                    lasers.remove(j)
                    explosions.append((met[0], met[1], time.time()))
                
            # removing hearts on collsion
            if meteor_rect.colliderect(ship_rect):
                if hearts:
                    hearts.pop(0)
                    meteors_list.remove(met)
                    game_end = False
                else:
                    game_end= True

                return game_end

            # removing rocks on collision with sl
            for sl in special_lasers[:]:
                sl_rect = pygame.Rect(sl[0],sl[1],50,laser_height)
                if sl_rect.colliderect(meteor_rect):
                    meteors_list.remove(met)
                    explosions.append((met[0], met[1], time.time()))

    # highscore
    highest_time = 0
    with open(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\highscore.txt",'r') as f:
       highest_time = int(f.read())

    # meteor timer
    meteor_timer = pygame.event.custom_type()
    pygame.time.set_timer(meteor_timer,700)

    # laser and sl timer
    laser_shot = 0
    time_gap = 0.5
    sl_shot = 0
    sl_gap = 2

    # game timer
    start_time = pygame.time.get_ticks()
    creat_heart()

    while not game_over:
        ship_rect = pygame.Rect(ship_x,ship_y,ship_width,ship_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == meteor_timer:
                    create_meteros(4)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    current_time = time.time()
                    if current_time - sl_shot >= sl_gap:
                        create_sl(1)
                        sl_shot = current_time
                if event.key == pygame.K_SPACE:
                    current_time = time.time()  # getting real time
                    if current_time - laser_shot >= time_gap: #checking if 0.5 seconds have past
                        create_laser(1)
                        laser_shot = current_time #setting laser shot back
                if event.key == pygame.K_q: 
                    game_over = True

        game_window.blit(bg,(0,0))
        game_window.blit(ship_pic,(ship_x,ship_y))
        
        for i in creation:
            game_window.blit(stars_pic,(i[0],i[1]))

        for j in meteors_list[:]:
            game_window.blit(meteor_pic,(j[0],j[1]))
            j[1] += 5
            if j[1] > screen_height:
                meteors_list.remove(j)

        for k in lasers[:]:
            game_window.blit(laser_pic,(k[0],k[1]))
            k[1] -= 3
            if k[1] >= screen_height:
                lasers.remove(k)

        for l in special_lasers[:]:
            game_window.blit(special_laser_pic,(l[0],l[1]))
            l[1] -= 3
            if l[1] >= screen_height:
                special_lasers.remove(l)

        for m in hearts[:]:
            game_window.blit(heart_pic,(m[0],m[1]))

        for n in explosions[:]:
            if time.time() - n[2] < 1: # display for 1 second
                game_window.blit(explotion_pic,(n[0],n[1]))
            else:
                explosions.remove(n)   

        # score / time 
        if not game_end:
            timer = (pygame.time.get_ticks() - start_time) // 1000
            score_text = pygame.font.SysFont('bold',30)
            time_score = score_text.render("TIME: " + str(timer),True,'white')
            game_window.blit(time_score,(10,10))

        # updating highscore 
        if timer > highest_time:
            highest_time = timer
            with open(r"C:\Users\malkh\Desktop\Python-Games\space-shooter\assets\highscore.txt",'w') as f:
                f.write(str(highest_time))
    
        if game_end == True:
            game_window.blit(game_over_bg,(0,0))

            # displaying highscore
            highest_time_text = pygame.font.SysFont('bold',50)
            highest_time_display = highest_time_text.render("Highest time: " + str(highest_time),True,'white')
            game_window.blit(highest_time_display,(325,650))

            # your score
            score_text = pygame.font.SysFont('bold',50)
            time_score = score_text.render("Your time: " + str(timer),True,'white')
            game_window.blit(time_score,(325,700))

        collision(ship_rect)
        movement()
        pygame.display.update()
        clock.tick(60)

pygame.quit()
gameloop()
