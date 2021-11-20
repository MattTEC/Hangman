import pygame, sys, random, time

#setting up pygame stuff
pygame.font.init()
pygame.display.set_caption("Hangman")
default_font = pygame.font.SysFont("Consolas", 50)
special_font = pygame.font.SysFont("Consolas", 100)
screen = pygame.display.set_mode((1280, 720))
play = False
fail = False
win = False
clock = pygame.time.Clock()
file = open("words.txt","r")
content = file.readlines()
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
strikes = 0
#setting up hangman png's into list
hangmen = {}
name = ""

for image in range(7):
    stringimage = str(image)
    hangmen[image] = pygame.image.load("Hangman-" + stringimage + ".png").convert_alpha()
    hangmen[image] = pygame.transform.scale(hangmen[image], (600, 600))

start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        #mouse pos
        pos = pygame.mouse.get_pos()

        #check mouseover and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0]== 0:
            self.clicked = False
                


        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


start_button = Button(90, 230, start_img, 2)
exit_button = Button(690, 230, exit_img, 2)
start_buttton = Button(860, 230, start_img, 1)
exit_buttton = Button(880, 400, exit_img, 1)


def setup():
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    strikes = 0
    pygame.event.pump()
    word = content[random.randint(0, 854)]
    word = word.lower()
    wordguess = []
    da = len(word) - 1

    for i in range(0, da):
        wordguess.append("_ ")
    wrong = 0

    return word, wordguess, wrong, letters, strikes 
    

def gameloop(word, wordguess, wrong):
    screen.fill((255, 255, 255))
    time.sleep(0.5)
    text = ''.join(wordguess)
    text = text[:-1]
    letters_avaliable = ""
    screen.blit(hangmen[strikes],(230,-50))
    y = -50
    
    for i in range(len(letters)):
        if i % 7 == 0:
            textsurface = special_font.render(letters_avaliable, False, (0, 0, 0))
            screen.blit(textsurface, (70, y))
            y = y + 100
            letters_avaliable = ""
        letters_avaliable = letters_avaliable + str(letters[i])
    
    if len(letters_avaliable) > 0:
        textsurface = special_font.render(letters_avaliable, False, (0, 0, 0))
        screen.blit(textsurface, (100, y))
        
    
    
    
    
    target_width = 10
    width, height = default_font.size(text)
    if width <= target_width:
        # use the default font
        textsurface = default_font.render(text, False, (0, 0, 0))
    else:
        # use a smaller temp font
        size_factor = target_width / width
        #size_factor = round(size_factor)
        the_size = 50 * size_factor
        the_size = round(the_size)
        smaller_font = pygame.font.SysFont("Consolas", 50 * the_size)
        textsurface = smaller_font.render(text, False, (0, 0, 0))

    text_rect = textsurface.get_rect(center=(1280/2, 1200/2))
    screen.blit(textsurface, text_rect)

    
    
    
    
    go = False
    pygame.display.update()

    return go
    
def add_letter(name, strikes):
    fail = False
    win = False
    name = name.upper()
    if name in letters:
        letters.remove(name)
        name = name.lower()
        if name in word:
            for i in range(0, len(word)):
                if word[i] == name:
                    wordguess[i] = name + " "
        else:
            strikes = strikes + 1
            
            if strikes == 6:
                fail = True
        
        if "_ " not in wordguess:
            win = True
            
                
            
            
    
    return strikes, letters, fail, win








go = True

run = True
#mainloop
while run:

    #quit loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                name = event.unicode

                if win == False and fail == False:
                    strikes, letters, fail, win = add_letter(name, strikes)
                    go = gameloop(word, wordguess, wrong)

    if win == False and fail == False:
        if play == True and go == True: 
            word, wordguess, wrong, letters, strikes = setup()
            go = gameloop(word, wordguess, wrong) 

        elif play == False:
            screen.fill((255, 255, 255))
            if start_button.draw():
                play = True
            if exit_button.draw():
                run = False

    if win == True:
        textsurface = special_font.render("You win!", False, (0, 0, 0))
        screen.blit(textsurface, (790, 100))
        if start_buttton.draw():
            play = True
            win = False
            lose = False
            fail = False
            word, wordguess, wrong, letters, strikes = setup()
            go = gameloop(word, wordguess, wrong)
        if exit_buttton.draw():
            run = False
        
    if fail == True:
        textsurface = special_font.render("You lose!", False, (0, 0, 0))
        screen.blit(textsurface, (790, 100))
        if start_buttton.draw():
            play = True
            win = False
            lose = False
            fail = False
            word, wordguess, wrong, letters, strikes = setup()
            go = gameloop(word, wordguess, wrong)
        if exit_buttton.draw():
            run = False    
    
    pygame.display.update()