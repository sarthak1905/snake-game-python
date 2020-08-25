#Made by /sarthak1905(GitHub)
#If you find any bugs with the following, feel free to report an issue or contact me!
import pygame
import random
import math
import sys

#Dimensions
WIDTH = 800
HEIGHT = 600

#Colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

#Snake square Dimensions
snake_d = 40

#Food square Dimensions
food_d = 40

#Maximum distance to successfully eat food
edible_dist = 40

#Collison with self distance
collision_dist = edible_dist

def round40(x):
    return 40* round(x/40)

def print_food(win,food,foodx,foody):
    win.blit(food,(foodx,foody))

def check_if_eaten(win,x,y,foodx,foody):
    dist = calc_dist(x,y,foodx,foody)
    if dist <= 20:
        return True
    else:
        return False

def check_if_collided(snake_list):
    for i in range(2,len(snake_list)):
        dist = calc_dist(snake_list[0][0],snake_list[0][1],snake_list[i][0],snake_list[i][1])
        if dist == 0:
            return True
    return False

def calc_dist(x1,y1,x2,y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def produce_food(snake_list,rectx,recty):
    f = True
    while True:
        foodx = round40(random.randrange(0,WIDTH - food_d))
        foody = round40(random.randrange(0,HEIGHT - food_d))
        for x in snake_list:
            if calc_dist(x[0],x[1],foodx,foody) < collision_dist or (x[0] in range(2*rectx+1) and x[1] in range(2*recty+1)):
                f = False
                break
        if f:
            break
    return foodx, foody 

def add_body(snake_list,moving):
    if moving is 'left':
        snake_list.append((snake_list[-1][0]+snake_d,snake_list[-1][1]))
    if moving is 'right':
        snake_list.append((snake_list[-1][0]-snake_d,snake_list[-1][1]))
    if moving is 'down':
        snake_list.append((snake_list[-1][0],snake_list[-1][1]-snake_d))
    if moving is 'up':
        snake_list.append((snake_list[-1][0],snake_list[-1][1]+snake_d))


def move_body(snake_list):
    for i in range(len(snake_list)-1,0,-1):
        x = snake_list[i-1][0]
        y = snake_list[i-1][1]
        snake_list[i] = (x,y)

def print_body(win,body,snake_head,snake_list):
    for i in range(len(snake_list)-1,0,-1):
        win.blit(body,(snake_list[i][0],snake_list[i][1]))
    win.blit(snake_head,(snake_list[0][0],snake_list[0][1]))

def game():

    #Initialization
    pygame.init()
    win = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Snake game by @sarthak1905')
    game_running = True

    #Loading Background Image
    bg_img = pygame.image.load('images/background.png')

    #Loading Food
    food = pygame.image.load('images/apple.png')

    #Loading Snake Head, initially looking up 
    head_img = pygame.image.load('images/snake_head_up.png')

    #Loading Snake Body
    body = pygame.image.load('images/body.png')

    #Initial snake length 
    s_length = 1

    #start point 
    x = WIDTH/2
    y = HEIGHT/2

    #Chage in dimension
    change_d = snake_d

    #change in x and y, initially moving upwards 
    x_change = 0
    y_change = -change_d
    moving = 'up'

    #Initialization of speed 
    clock = pygame.time.Clock()

    #Initialization of list for handling snake body 
    snake_list = []
    snake_list.append((x,y))

    #Game over display 
    font_c = pygame.font.Font('freesansbold.ttf', 40)
    message_c = ' Game Over! Your score was: '
    text_c = font_c.render(message_c, True, white, black)
    textRect_c = text_c.get_rect()
    messagex = WIDTH/2
    messagey = HEIGHT/4
    textRect_c.center = (messagex, messagey)
    replay_quit_img = pygame.image.load('images/game_close.png')

    #Live score display 
    font = pygame.font.Font('freesansbold.ttf', 25)
    score_template = ' Score: '
    text = font.render(score_template, True, black, white)
    textRect = text.get_rect()
    score_rectx = 40
    score_recty = 15
    textRect.center = (score_rectx,score_recty)   

    #Initialization
    score = 0

    #Speed
    speed = 5

    #Initial food coordinates
    foodx,foody = produce_food(snake_list,score_rectx,score_recty)

    game_over = False
    eaten = False
    play_again = False
    break_out = False

    #Mouse coordinates initialized 
    mouse = (0,0)

    #Game loop
    while game_running:

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break
            
            if not game_over:

                #Keypress Conditions
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        head_img = pygame.image.load('images/snake_head_left.png')
                        x_change = -change_d
                        y_change = 0
                        moving = 'left'
                    if event.key == pygame.K_RIGHT:
                        head_img = pygame.image.load('images/snake_head_right.png')
                        x_change = change_d
                        y_change = 0
                        moving = 'right'
                    if event.key == pygame.K_DOWN:
                        head_img = pygame.image.load('images/snake_head_down.png')
                        y_change = change_d
                        x_change = 0
                        moving = 'down'
                    if event.key == pygame.K_UP:
                        head_img = pygame.image.load('images/snake_head_up.png')
                        y_change = -change_d
                        x_change = 0
                        moving = 'up'
            
            else:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse[0] in range(208,350) and mouse[1] in range(475,540):
                        break_out = True
                        play_again = True 
                        break
                    elif mouse[0] in range(454,605) and mouse[1] in range(475,540):
                        break_out = True
                        play_again = False
                        break
        if break_out:
            break

        if not game_over:
            
            #Updating Change in coordinates
            x += x_change
            y += y_change

            #Checking bounds
            if x>= WIDTH - snake_d:
                x = WIDTH - snake_d
            if x<= 0:
                x = 0
            if y>= HEIGHT - snake_d:
                y = HEIGHT - snake_d
            if y<= 0 :
                y = 0

            snake_xy = (x,y)
            if len(snake_list) > 0:
                snake_list[0] = snake_xy
            else: 
                snake_list.append(snake_xy)

            #Check if snake has eaten food
            eaten = check_if_eaten(win,x,y,foodx,foody)

            #Background Image
            win.blit(bg_img,(0,0))

            #Print new food if snake eats it 
            if eaten:
                foodx,foody = produce_food(snake_list,score_rectx, score_recty) 
                print_food(win,food,foodx,foody)
                s_length += 1
                
                #Update score
                score += 10

                #Adding Body
                add_body(snake_list,moving)

                #Increasing Speed
                #speed += 1

            else:
                print_food(win,food,foodx,foody)
            
            if check_if_collided(snake_list):
                game_over = True

            #Moving snake 
            move_body(snake_list)

            #Printing Snake
            print_body(win,body,head_img,snake_list)

            #Display Live Score
            text = font.render(score_template + str(score) + ' ', True, black, white)
            win.blit(text,textRect)
 
        #If game is over 
        else:
            win.fill(black)
            text_c = font_c.render(message_c + str(score) + ' ', True, white, black)

            #Display final score
            win.blit(text_c,textRect_c)

            #Display Play or Quit 
            win.blit(replay_quit_img, (WIDTH/5,2*HEIGHT/3))

            #Mouse coordinates
            mouse = pygame.mouse.get_pos()
            
        #Updating display with specified time
        pygame.display.update()
        clock.tick(speed)
    
    if play_again:
        game()
    pygame.quit()
    sys.exit(0)

def main():
    game()

if __name__ == '__main__' :
    main()