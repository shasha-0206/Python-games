import pygame
import random

clock = pygame.time.Clock()

def game():
    pygame.init()

    # game variables
    height = 20
    width = 20
    screen_width = 500
    screen_height = 500
    # game graphics
    bg = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\rps\assets\bg.png")
    rock_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\rps\assets\stone.png")
    paper_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\rps\assets\paper.png")
    scissor_pic = pygame.image.load(r"C:\Users\malkh\Desktop\Python-Games\rps\assets\scissor.png")

    # resized images
    rock_pic = pygame.transform.scale(rock_pic,(width,height))
    paper_pic = pygame.transform.scale(paper_pic,(width,height))
    scissor_pic = pygame.transform.scale(scissor_pic,(width,height))

    game_window = pygame.display.set_mode((screen_width,screen_height))

    # displaying scissor
    def creating_scissor(numb):
        scissor_location = []
        s__x = [1,1.5,2,2.5,3,4]
        s__y = [1,1.5,2,2.5,3,4]
        for _ in range (numb):
            s_vel_x = random.choice(s__x)
            s_vel_y = random.choice(s__y)
            scissor_x = random.randint(350,450)
            scissor_y = random.randint(350,450)
            scissor_location.append([scissor_x,scissor_y,s_vel_x,s_vel_y])
        return scissor_location

    scissor_pos = creating_scissor(7)

    # displaying paper
    def creating_paper(num):
        paper_location = []
        p__x = [1,1.5,2,2.5,3,4]
        p__y = [1,1.5,2,2.5,3,4]
        for _ in range(num):
            p_velx = random.choice(p__x)
            p_vely = random.choice(p__y)
            paper_x = random.randint(220,270)
            paper_y = random.randint(10,100)
            paper_location.append([paper_x,paper_y,p_velx,p_vely])
        return paper_location

    paper_pos = creating_paper(7)

    # displaying rocks
    def creating_rocks(number):
        rock_location = []
        x = [1,1.5,2,2.5,3,4]
        y = [1,1.5,2,2.5,3,4]
        for _ in range (number):
            vel_x = random.choice(x)
            vel_y = random.choice(y)
            rock_x = random.randint(30 ,100)
            rock_y = random.randint(350,450)
            rock_location.append([rock_x,rock_y,vel_x,vel_y])
        return rock_location

    rocks_pos = creating_rocks(7)

    def collision():

        scissor_count = len(scissor_pos)
        paper_count = len(paper_pos)
        rock_count = len(rocks_pos)

        # checking collision btw rock and paper
        for rock in rocks_pos[:]: #creating a copy of the original rock pos 
            # this is to ensure tht original list remains smae and iteration is done without any issues
            rock_rect = pygame.Rect(rock[0],rock[1],width,height)
            for paper in paper_pos[:]:
                paper_rect = pygame.Rect(paper[0],paper[1],width,height)
                if rock_rect.colliderect(paper_rect):
                    # removing rock on collsion
                    rocks_pos.remove(rock)
                    rock_count -= 1
                    paper_pos.append([rock[0],rock[1],rock[2],rock[3]])
                    paper_count += 1
                    break
                    # appending the speed and coords of rock to the paper pos
                    # since we are bliting paper pics in paper pos in gameloop the rock is changed to paper

        # checking collision btw rock and scissor
        for rock in rocks_pos[:]:
            rock_rect = pygame.Rect(rock[0],rock[1],width,height)
            for scissor in scissor_pos[:]:
                scissor_rect = pygame.Rect(scissor[0],scissor[1],width,height)
                if rock_rect.colliderect(scissor_rect):
                    scissor_pos.remove(scissor)
                    scissor_count -= 1
                    rocks_pos.append([scissor[0],scissor[1],scissor[2],scissor[3]])
                    rock_count += 1
                    break

        # checking collision btw scissor and paper
        for scissor in scissor_pos[:]:
            scissor_rect = pygame.Rect(scissor[0],scissor[1],width,height)
            for paper in paper_pos[:]:
                paper_rect = pygame.Rect(paper[0],paper[1],width,height)
                if scissor_rect.colliderect(paper_rect):
                    paper_pos.remove(paper)
                    paper_count -= 1
                    scissor_pos.append([paper[0],paper[1],paper[2],paper[3]])
                    scissor_count += 1
                    break

        return rock_count, paper_count, scissor_count

    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_exit = True

        game_window.blit(bg,(0,0))

        for i in rocks_pos:
            i[0] += i[2]
            i[1] += i[3]

            if i[0] <= 0 or i[0] >= screen_width - width:
                i[2] = -i[2]
            if i[1] <= 0 or i [1] >= screen_height -  height:
                i[3] = -i[3]
                
            game_window.blit(rock_pic,(i[0],i[1]))

        for j in paper_pos:
            j[0] += j[2]
            j[1] += j[3]

            if j[0] <= 0 or j[0] >= screen_width - width:
                j[2] = -j[2]
            if j[1] <= 0 or j [1] >= screen_height -  height:
                j[3] = -j[3]

            game_window.blit(paper_pic,(j[0],j[1]))

        for k in scissor_pos:
            k[0] += k[2]
            k[1] += k[3]

            if k[0] <= 0 or k[0] >= screen_width - width:
                k[2] = -k[2]
            if k[1] <= 0 or k [1] >= screen_height -  height:
                k[3] = -k[3]
                
            game_window.blit(scissor_pic,(k[0],k[1]))

        rock_count, paper_count, scissor_count = collision()
        
        # displaying score
        font = pygame.font.Font(None, 36)
        game_window.blit(rock_pic,(0,10))
        game_window.blit(paper_pic,(69,12))
        game_window.blit(scissor_pic,(140,12))
        text = font.render(f"  : {rock_count}      : {paper_count }      : {scissor_count}", True, ('black'))
        game_window.blit(text, (10, 10))

        # winner declaration
        if rock_count == 0 and paper_count == 0:
            font = pygame.sysfont.SysFont('bold',100)
            winner1 = font.render("Scissors won",True,'white')
            game_window.blit(winner1,(100,200))

        elif rock_count == 0 and scissor_count == 0:
            font = pygame.sysfont.SysFont('bold',100)
            winner2 = font.render("Paper won",True,'white')
            game_window.blit(winner2,(100,200))

        elif scissor_count == 0 and paper_count == 0:
            font = pygame.sysfont.SysFont('bold',100)
            winner3 = font.render("Rock won",True,'white')
            game_window.blit(winner3,(100,200))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

game()

           
