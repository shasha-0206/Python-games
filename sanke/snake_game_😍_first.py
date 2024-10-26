import pygame
import random
pygame.mixer.init()
pygame.init()

# setting graphics
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
font = pygame.font.SysFont('bold',30)
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
    global velocity_x, velocity_y,score
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
        elif event.key == pygame.K_q:
            score += 5

# Food
food_x = random.randint(20, screen_width - width)    # First food outside the while loop 
food_y = random.randint(20, screen_height - height)  # First food outside the while loop 

def food():
    global apple_image
    food_size = 25
    apple_image = pygame.transform.scale(apple_image, (food_size, food_size))
    game_window.blit(apple_image, (food_x, food_y))

snake_body = []
snake_length = 1

# Checking for collision
score = 0
def collision():
    global snake_length,score
    global food_x, food_y
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
with open (r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\highscore.txt","r") as f:
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
        elif event.type == pygame.KEYDOWN:  # if entre is pressed game start
            if event.key == pygame.K_RETURN:
                def game_loop():
                    global highscore
                    game_over = False
                    game_end = False
                    global snake_x,snake_y

                    while not game_end:        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
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
                            with open (r"C:\Users\malkh\Desktop\programs\Python\imp_files\snake\highscore.txt","w") as f:
                                f.write(str(highscore))

                        # Calling all the functions
                        plot_snake(game_window,snake_body) # add(width,height,color)if not using graphics
                        snake_head()
                        food()
                        screen_font("    :" + str(score) + "    Highscore: " + str(highscore), 'red', 10,10)
                        collision()

                        # setting boundaries
                        if snake_y < 0 or snake_y > screen_height or snake_x < 0 or snake_x  > screen_width:
                            pygame.mixer.music.load(r"C:\Users\malkh\Desktop\Python-Games\sanke\assests\gta-v-death-sound-effect-102.mp3") 
                            pygame.mixer.music.play()
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
                        clock.tick(30)
                game_loop()
                # pygame.quit()

