from tkinter import * 
from tkinter import messagebox
import pygame
import random

t = Tk()
t.title("PROJECT - 4")
t.geometry('720x500')

# creating frames
welcome_frame = Frame(t)
welcome_frame.pack()
select_frame = Frame(t, width=754, height=528, bg='#c44ec7')  

# setting bg of welcome frame
bg_image = PhotoImage(file=r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\Screenshot 2024-05-11 112231.png")
bg_label = Label(welcome_frame, image=bg_image)
bg_label.grid(row=0, column=0)

# player name 
welcome_entry = Entry(welcome_frame)
welcome_entry.place(x = 260, y = 280,width=200)

pygame.init()

# breakout game
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
        ball_vel_x *= -1
    
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
    t.withdraw()
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
    with open (r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\breakout_score","r") as f:
        highscore = int(f.read())

    while not game_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    game_end = True
                    t.deiconify()
                                   
        bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\Screenshot 2024-05-10 143404.png")
        game_over_bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\Screenshot 2024-05-29 140143.png")
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
            with open (r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\breakout_score","w") as f:
                f.write(str(highscore))

        # gameover bg 
        if ball_y >= screen_height:
            game_window.blit(game_over_bg, (0, 0))
            pygame.display.update()
            pygame.time.wait(3000)

            #  quit initialisation
            option = messagebox.askyesno("info", "Do you want to try other games?")
            if option:
                pygame.quit()
                t.deiconify()
            else:
                pygame.quit()
                t.withdraw()

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

    pygame.quit()

# bullet dodge game
def second_game():
    pygame.init()
    t.withdraw()
    clock = pygame.time.Clock()

    # setting game window
    screen_width = 900
    screen_height = 500
    game_window = pygame.display.set_mode((screen_width, screen_height))

    # graphics
    bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\bg.jpeg")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

    game_over_bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\gettyimages-1325433246-640x640.jpg")
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
    with open(r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\space_shooter1_score",'r') as f:
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
                        game_end = True
                        t.deiconify()
            x
            # displaying background
            game_window.blit(bg, (0, 0))

            # time / score
            if not game_end:
                time = (pygame.time.get_ticks() - start_time) // 1000
                score_text = pygame.font.SysFont('bold',30)
                time_score = score_text.render("TIME: " + str(time),True,'white')
                game_window.blit(time_score,(10,10))

            # updating highscore 
            if time > highest_time:
                highest_time = time
                with open(r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\space_shooter1_score",'w') as f:
                    f.write(str(highest_time))
            
            # displaying highscore
            highest_time_text = pygame.font.SysFont('bold',30)
            highest_time_display = highest_time_text.render("Highest time: " + str(highest_time),True,'white')
            game_window.blit(highest_time_display,(730,10))

            # drawing rectangle
            pygame.draw.rect(game_window, 'red', (x, y, player_width, player_height))

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
                pygame.time.wait(3000)
                optoin_2 = messagebox.askyesno("info",'Do you want to try other games?')
                if optoin_2 == True:
                    t.deiconify()
                    pygame.quit()
                else:
                    pygame.quit()
                    t.withdraw()

            create_bullets(bullet,game_over)

            pygame.display.update()
            clock.tick(30)

    game_loop_2()
    pygame.quit()

# snake game 
def third_game():
    t.withdraw()
    pygame.init()
    pygame.font.init()
    apple_image = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\apple.png")
    home_screen = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\Screenshot 2024-04-30 222153.png")
    bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\891ee9a180d14aa4cb2f71100d7b3a987215d384.jpg")
    game_over_bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\maxresdefault.jpg")

    head_up = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\head_up.png")
    head_right = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\head_right.png")
    head_left = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\head_left.png")
    head_down = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\head_down.png")

    body_horizontal = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\body_horizontal.png")
    body_vertical = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\body_vertical.png")

    game_over_bg = pygame.transform.scale(game_over_bg,(750,350))
    clock = pygame.time.Clock()

    # Game window 
    screen_width = 700
    screen_height = 350
    game_window = pygame.display.set_mode((screen_width, screen_height))

    # Game title
    pygame.display.set_caption("Snake Game")

    # Drawing snakehead
    snake_x = 50
    snake_y = 50
    width = 20
    height = 20
    velocity_y = 0
    velocity_x = 0

    # displaying score on screen
    font = pygame.font.SysFont('bold', 30) 
    def screen_font(text,color,x,y):
        screen_text = font.render(text,True,color)
        game_window.blit(screen_text,(x,y))
        game_window.blit(apple_image,(10,6))

    # setting snake head
    def snake_head():
        if velocity_y < 0:  # Moving upwards since y is neg
            game_window.blit(head_up, (snake_x, snake_y))
        elif velocity_y > 0:  # Moving downwards since i y is positive
            game_window.blit(head_down, (snake_x, snake_y))
        elif velocity_x > 0:  # Moving rightwards since x is positive
            game_window.blit(head_right, (snake_x, snake_y))
        else:  # Moving leftwards since x is neg
            game_window.blit(head_left, (snake_x, snake_y))

    # Binding keys
    def binding(event):
        nonlocal velocity_x, velocity_y,score
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                velocity_y -= 5  # speed of snake
                velocity_x = 0
            elif event.key == pygame.K_s:
                velocity_y += 5  # speed of snake
                velocity_x = 0
            elif event.key == pygame.K_a:
                velocity_x -= 5  # speed of snake
                velocity_y = 0
            elif event.key == pygame.K_d:
                velocity_x += 5  # speed of snake 
                velocity_y = 0
            elif event.key == pygame.K_x:
                score += 5

    # Food
    food_x = random.randint(20, screen_width - width)    # First food outside the while loop 
    food_y = random.randint(20, screen_height - height)  # First food outside the while loop 

    def food():
        nonlocal apple_image
        food_size = 25
        apple_image = pygame.transform.scale(apple_image, (food_size, food_size))
        game_window.blit(apple_image, (food_x, food_y))

    snake_body = []
    snake_length = 1

    # Checking for collision
    score = 0
    def collision():
        nonlocal snake_length,score
        nonlocal food_x, food_y
        if abs(snake_x - food_x) < 25 and abs(snake_y - food_y) < 25: # abs functions used to absolute value
            score += 1
            food_x = random.randint(20, screen_width - 20)  # adding new food at random spots
            food_y = random.randint(20, screen_height - 20) # adding new food at random spots
            snake_length += 2

    def plot_snake(game_window, snake_body):  # for x,y in snake_body,draw a reactangel

        # Draw the body segments
        for i in range(1, len(snake_body) - 1):
            segment = snake_body[i]
            next_segment = snake_body[i + 1]
            previous_segment = snake_body[i - 1]
            dx = next_segment[0] - previous_segment[0]
            dy = next_segment[1] - previous_segment[1]

            if dx == 0:
                if dy < 0:
                    game_window.blit(body_vertical, (segment[0], segment[1]))
                else:
                    game_window.blit(body_vertical, (segment[0], segment[1]))
            elif dy == 0:
                if dx < 0:
                    game_window.blit(body_horizontal, (segment[0], segment[1]))
                else:
                    game_window.blit(body_horizontal, (segment[0], segment[1]))

    # Load and scale background image to fit the game window
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    home_screen = pygame.transform.scale(home_screen, (screen_width, screen_height))

    # highscore display
    highscore = 0
    with open (r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\snake_score","r") as f:
        highscore = int(f.read())

    # homescreen image displyed
    game_window.blit(home_screen,(0,0))
    pygame.display.update()

    # Loop for not ending the window
    while True:
        for event in pygame.event.get(): #keeping the window open
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_RETURN:    # if entre is pressed game start
                    def game_loop():
                        nonlocal highscore
                        game_over = False
                        game_end = False
                        nonlocal snake_x,snake_y

                        while not game_end:        
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    game_end = True
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_q:
                                        game_end = True
                                
                                binding(event)
                            
                            game_window.blit(bg, (0, 0))

                            snake_x += velocity_x  #continuouse movement of snake
                            snake_y += velocity_y

                            head = []
                            head.append(snake_x)
                            head.append(snake_y)
                            snake_body.append(head)

                            if len(snake_body) > snake_length:
                                del snake_body[0]

                            # snake collides wiht its own body the game ends
                            if head in snake_body[:-1]:
                                game_over = True   

                            # setting highscore
                            if score > highscore:
                                highscore = score
                                with open (r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\snake_score","w") as f:
                                    f.write(str(highscore))

                            # Calling all the functions
                            plot_snake(game_window,snake_body) # add(width,height,color)if not using graphics
                            snake_head()
                            food()
                            screen_font("    :" + str(score) + "    Highscore: " + str(highscore), 'red', 10,10)
                            collision()

                            # setting boundaries
                            if snake_y < 0 or snake_y > screen_height or snake_x < 0 or snake_x  > screen_width:
                                game_over = True

                            # displaying score
                            if game_over:
                                game_window.blit(game_over_bg,(0,0))
                                font_game_over = pygame.font.SysFont('bold',30)
                                game_over_text = font_game_over.render("YOUR SCORE: " + str(score),True,'white')
                                game_window.blit(game_over_text,(280,214))
                                highscore_font = font_game_over.render( "HIGHSCORE: " + str(highscore),True,'white')
                                game_window.blit(highscore_font,(290,250))
                                pygame.display.update()
                                pygame.time.wait(3000)
                                optoin_3 = messagebox.askyesno("info",'Do you want to try other games?')
                                if optoin_3:
                                    pygame.quit()
                                    t.deiconify()
                                else:
                                    pygame.quit()
                                    t.withdraw()

                            pygame.display.update()
                            clock.tick(30)

                    game_loop()        
                
# creating second frame by binding entre key
def second_frame(click):
    welcome_message = welcome_entry.get()
    if welcome_message:
        if len(welcome_message) >= 5:
            welcome_frame.pack_forget()
            select_frame.pack()
        else:
            messagebox.showerror("error",'please entre a name with charecters more than 5')
    else:
        messagebox.showerror("error",'please entre your name to proceed')

t.bind("<Return>", second_frame)

# snake game icon 
s_game_image = PhotoImage(file=r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\Screenshot 2024-05-10 170049.png")
s_game_image = s_game_image.subsample(2)
s_image_label = Label(select_frame,image=s_game_image)
s_image_label.place(x = 50,y = 50,width=100,height=100)

start_snake = Button(select_frame, text='Snake Game',
                     font=('bold', 10),
                     bg='#c44ec7',
                     fg='white',
                     command=third_game)

start_snake.place(x=202, y=91)

# breakout icon
b_game_image = PhotoImage(file=r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\Screenshot 2024-05-10 223216.png")
b_image_label = Label(select_frame,image=b_game_image)
b_image_label.place(x = 51, y = 216,width=100,height=100)

start_break = Button(select_frame, text='Breakout Game',
                     font=('bold', 10),
                     bg='#c44ec7',
                     fg='white',
                     command=gameloop)

start_break.place(x=202, y=257)

# bullet dodge icon
bullet_game_image = PhotoImage(file=r"C:\Users\malkh\Desktop\Python-Games\game-trio-hub\assets\Screenshot 2024-05-10 224500.png")
bullet_game_label = Label(select_frame,image=bullet_game_image)
bullet_game_label.place(x = 50, y = 365,width=100,height=120)

start_bullet = Button(select_frame, text='Bulletdodge Game',
                     font=('bold', 10),
                     bg='#c44ec7',
                     fg='white',
                     command = second_game)

start_bullet.place(x=202, y=417)

t.mainloop()
