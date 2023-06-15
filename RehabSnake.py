import pygame
import time
import random
import serial
import csv
import os

pygame.init()

ser = serial.Serial('/dev/tty.usbmodem101', 9600)

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
orange=(255,69,0)

dis_width = 1200
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Eat Up Snakey')

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

snake_block = 50
snake_speed = 50

font_style = pygame.font.SysFont("comicsansms", 35)
score_font = pygame.font.SysFont("comicsansms", 37)

bg = pygame.image.load("background.png")  # Load image once
bg2 = pygame.image.load("instruction.jpg")
image = pygame.transform.scale(bg2, (384, 300)) 
# ... Code omitted for brevity ...
def Your_score2(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def Your_score(score, start_time):
    run_time = pygame.time.get_ticks() - start_time
    value = score_font.render("Score: " + str(score) + ", time: " + str(int(run_time/1000)), True, yellow)
    dis.blit(value, [0, 0])
    
    
def Your_final_score(score, elapsed_seconds):
    value = score_font.render("Score: " + str(score) + ", time: " + str(elapsed_seconds), True, yellow)
    dis.blit(value, [0, 0])
    



def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    lines = msg.split('\n')
    for i, line in enumerate(lines):
        mesg = font_style.render(line, True, color)
        dis.blit(mesg, [int(dis_width / 3), int(dis_height / 3) + i*40])

def message2(msg):
    global image
    global bg
    dis.blit(bg,bg.get_rect())
    image_x = dis_width - image.get_width() - 20 
    image_y = dis_height - image.get_height() - 20  
    dis.blit(image, (image_x, image_y)) 

    lines = msg.split('\n')
    longest_line_width = max(font_style.size(line)[0] for line in lines)

    title_font_style = pygame.font.SysFont("comicsansms", 50)
    title = title_font_style.render(lines[0], True, white)
    title_rect = title.get_rect(center=(dis_width / 2, title_font_style.get_height() / 2 + 10)) 
    dis.blit(title, title_rect)

    for i, line in enumerate(lines[1:]):
        mesg = font_style.render(line, True, white)
        text_height = mesg.get_height()
        position_x = 20 
        position_y = 10 + i * (text_height + 10)  
        dis.blit(mesg, [position_x, position_y])
def start():
    game_start= False
    if game_start==True:
        return
    instructions = ('Welcome to RehabSnake\n\n'
                        'Instructions:\n'
                        '1. The snake moves according to your gestures.\n'
                        '  1.1. Lift your forearm to move the snake up or down.\n'
                        '  1.2. Twist your forearm to move the snake left or right.\n'
                        '2. Eat the food to grow and score.\n'
                        '3. Press G to finish the game.\n'
                        '4. Press SPACE to start the game.')
    message2(instructions)
    pygame.display.update()
    while not game_start:
        pygame.event.pump()  # only pump the events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_start = True
            break
def gameLoop():
    global bg  # Reference to global image

    # ... Code omitted for brevity ...
    leftmax = 0
    rightmax = 0
    upmax = 0
    downmax = 0
    game_start= False
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 50.0) * 50.0
    foody = round(random.randrange(0, dis_height - snake_block) / 50.0) * 50.0

    while not game_over:
        data = ser.readline().decode().rstrip()
        values = data.split(",")
        if len(values) == 3:
            try:
                sensorValue1 = float(values[0])
                sensorValue2 = float(values[1])
                sensorValue3 = float(values[2])
            except ValueError:
                print("Invalid float values received")
        else:
            print("Invalid data format received")

        # Combine event handling into a single loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game_close = True
                elif event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                elif event.key == pygame.K_p:
                    gameLoop()

        # ... Code omitted for brevity ...
        if game_close == True:
            end_time = pygame.time.get_ticks()
        while game_close == True:
        
            elapsed_time = end_time - start_time
            elapsed_seconds = int(elapsed_time / 1000)
#            print("game time:", elapsed_seconds)

            dis.blit(bg,bg.get_rect())
            mes = (f'Press Q-Quit.\n\n'
                    f'Time: {elapsed_seconds} seconds \n'
                    f'The range of motion:\n'
                    f'Left: {abs(round(leftmax*80, 2))} degree \n'
                    f'Right: {abs(round(rightmax*80, 2))} degree \n'
                    f'Up: {abs(round(upmax*90, 2))} degree \n'
                    f'Down: {abs(round(downmax*90, 2))} degree!\n')
            message(mes, white)
            #motionprompt="maxverticalmotionis"
            #message("You Lost! Press P-Play Again or Q-Quit\n"+motionprompt, red)
            Your_final_score(Length_of_snake - 1, elapsed_seconds)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if sensorValue2 < -0.3:
                x1_change = -snake_block/5
                y1_change = 0
        elif sensorValue2 > 0.3:
                x1_change = snake_block/5
                y1_change = 0
        elif sensorValue1 < -0.5:
                y1_change = -snake_block/5
                x1_change = 0
        elif sensorValue1 > 0.5:
                y1_change = snake_block/5
                x1_change = 0

        if x1 >= dis_width:
            x1 -= dis_width
        elif x1 < 0:
            x1 += dis_width
        elif y1 >= dis_height:
            y1 -= dis_height
        elif y1 < 0:
            y1 += dis_height

        if sensorValue2 > rightmax and sensorValue2<1:
            rightmax  = sensorValue2
        if sensorValue2 < leftmax and sensorValue2>-1:
            leftmax = sensorValue2
        if sensorValue1 > downmax and sensorValue1<1:
            downmax = sensorValue1
        if sensorValue1 < upmax and sensorValue1>-1:
            upmax = sensorValue1

        x1 += x1_change
        y1 += y1_change

        dis.blit(bg, bg.get_rect())
        pygame.draw.rect(dis, orange, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1,start_time)

        pygame.display.update()  # Update display once per frame
        if x1 >= foodx - 20 and x1 <= foodx + 20 and y1 >= foody - 20 and y1 <= foody + 20:

            foodx = round(random.randrange(0, dis_width - snake_block) / 50.0) * 50.0
            foody = round(random.randrange(0, dis_height - snake_block) / 50.0) * 50.0
            Length_of_snake += 1


        clock.tick(snake_speed)
        # ... Code omitted for brevity ...

    data = [Length_of_snake - 1, elapsed_seconds, abs(round(leftmax*90, 2)), round(rightmax*90, 2), round(upmax*90, 2), abs(round(downmax*90, 2))]
    return data

# ... Code omitted for brevity ...
def main():
    file_path = './data.csv'
    file_exists = os.path.isfile(file_path)
    #print('test')
    #start_screen()
    start()
    data = gameLoop()
    
    print('data', data)

    if file_exists:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    else:
        # Create a new CSV file and write the data
        data1 = []
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            name_list =  ['Score', 'Time', 'Left Angle', 'Right Angle', 'Up Angle', 'Down Angle']
            nested_list = [name_list, data]
            writer.writerows(nested_list)


if __name__ == '__main__':
    main()