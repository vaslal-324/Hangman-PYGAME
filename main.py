import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 500

# loading images
images = []

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40, bold=True, italic=True)
WORD_FONT = pygame.font.SysFont('comicsans', 60)

# game variables
hangman_status = 0
words_list = ["PYTHON", "PYGAME", "CODING", "JAVA", "IDE", "COMPILER", "BINARY", "FUNCTION", "LOOPING"]
word = random.choice(words_list)
guessed = []

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (GAP + 2 * RADIUS) * 13) / 2)
starty = 400

for i in range(26):
    x = startx + GAP * 2 + ((GAP + 2 * RADIUS) * (i % 13))
    y = starty + (i // 13) * (2 * RADIUS + GAP)
    letters.append([x, y, chr(65 + i), True])  # storing the centres of the circles

for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN !!!")

FPS = 60  # Frames per second
clock = pygame.time.Clock()

run = True


def draw():
    screen.fill((255, 255, 255))
    display_word = ""
    for letter in word:  # iterate with word in trder to maintain the order
        if letter in guessed:
            display_word += letter + " "  # if a letter is guessed correctly then it is added to guessed and displayed
        else:
            display_word += "_ "
    text_w = WORD_FONT.render(display_word, 1, (0, 0, 0))  # first render and then blit
    screen.blit(text_w, (400, 200))
    # draw buttons
    for letter in letters:
        X, Y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, (0, 0, 0), (X, Y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, (0, 0, 0))
            screen.blit(text, (X - text.get_width() / 2, Y - text.get_height() / 2))
    screen.blit(images[hangman_status], (150, 100))
    pygame.display.update()  # can be put at the end of while loop also..good practice acc to me


def display_message(mess):
    pygame.time.delay(1000)
    screen.fill((255, 255, 255))
    text = WORD_FONT.render(mess, 1, (0, 0, 0))
    screen.blit(text, ((WIDTH - text.get_width()) / 2, (HEIGHT - text.get_height()) / 2))
    # above formula for centring the text depending on text
    pygame.display.update()  # vvv important
    pygame.time.delay(3000)  # == 3sec


while run:
    clock.tick(FPS)
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()  # returns a tuple of coordiantes
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                    if dist < RADIUS:
                        letter[3] = False  # do not write as visible = False since visible is just a copy
                        guessed.append(ltr)
                        if ltr not in word:  # pressed letter is not in word
                            hangman_status += 1

    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    if won:
        draw()

        display_message("YAAYYY, YOU WON !!!")
        break

    if hangman_status == 6:
        screen.blit(images[hangman_status], (150, 100))  # for showing the last image
        pygame.display.update()  # very important to update the changes after you do any change
        # else blit won't work

        display_message("OOPS ,YOU LOST !")
        break

pygame.quit()
