# Produkcija 

import pygame
import random
import time

white=(255,255,255)
black=(0,0,0)
size=width,height= 920,640
screen=pygame.display.set_mode(size)
clock= pygame.time.Clock()
fps= 60

meteor_num = 200
Meteors = []
meteor_speed = 5
meteor_size = 1


for m in range(meteor_num): # dodjeljujes random koordinate za meteore i spremas ih u array  
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    Meteors.append([x,y])

#Klasa koja sluzi za obradu i prikaz teksta na ekran   
class Message_to_screen(): 

    def __init__(self, font, color, position, msg):
        self.font = font
        self.color = color
        self.position = position
        self.msg = msg
        self.rect = 0
        
    def Display(self):
       text = self.font.render(self.msg, True, self.color)
       self.rect = text.get_rect()
       position = self.rect
       position.center = (self.position[0], self.position[1])
       screen.blit(text,position)
        
#Funkcija glavnog menija koja se otvara pri pokretanju igrice
def main_menu():
    menu_running = True

    pygame.mixer.music.load('SpaceThingMain_menu_theme.mp3') #Path do pjesme u folderu
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while menu_running == True:
        screen.fill(black)
        
        Title = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',40), (255,255,255), [width/2, height*0.3], 'SPACETHING')
        Player1_text = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [width*0.2, height*0.85], 'HAND   SOLO')
        Player2_text = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [width*0.8, height*0.85], 'HELPING   HAND')
        
        Title.Display()
        Player1_text.Display()
        Player2_text.Display()
        
        space_img = pygame.image.load('space_w.png') #Slika rakete
        x_icon = pygame.image.load('x_icon.png') #Slika iksića
        screen.blit(x_icon, (width*0.02, height*0.02))
        screen.blit(space_img, (width*0.429, height*0.4))
        

        if Player1_text.rect.collidepoint(pygame.mouse.get_pos()): #ako je mis iznad teksta hand solo napravi 3D kurac
            Player1_text.font = pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',35)
            Player1_text.color = (239, 90, 150)
            Player1_3D = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',30), (58,255,249), [width*0.2, height*0.85], 'HAND   SOLO')
            Player1_text.Display()
            Player1_3D.Display()
            
        if Player2_text.rect.collidepoint(pygame.mouse.get_pos()): #ako je mis iznad teksta helping hand napravi 3D kurac
            Player2_text.font = pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',35)
            Player2_text.color = (239, 90, 150)
            Player2_3D = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',30), (58,255,249), [width*0.8, height*0.85], 'HELPING   HAND')
            Player2_text.Display()
            Player2_3D.Display()

        for i in Meteors: #zoves array meteora i svaki ispisujes
            i[1] += meteor_speed

            if i[1] > height:
                i[1] = random.randrange(-50,-5)
                i[0] = random.randrange(width)
            # koristis tako da ti meteori padaju iznad teksta i svih ostalih objekta na ekranu
            if not(Title.rect.collidepoint(i) or Player1_text.rect.collidepoint(i)
                   or Player2_text.rect.collidepoint(i)
                   or pygame.Rect(404, 256, 116, 120).collidepoint(i) #rect za logo
                   or pygame.Rect(18, 10, 70, 70).collidepoint(i)):  # rect za x_icon
                
                if i[1] <= height*0.2: # mjenjas boje ovisno o y koordinati
                    pygame.draw.circle(screen,(255,77,0),i, meteor_size)
                elif i[1] > height*0.2 and i[1] <= height * 0.4:
                    pygame.draw.circle(screen,(255,162,0),i, meteor_size)
                elif i[1] > height*0.4 and i[1] <= height * 0.6:
                    pygame.draw.circle(screen,(255,213,0),i, meteor_size)
                elif i[1] > height*0.6 and i[1] <= height * 0.8:
                    pygame.draw.circle(screen,(250,255,0),i, meteor_size)
                else:
                    pygame.draw.circle(screen,(255,253,168),i, meteor_size)
  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ako kliknes na x prozora ugasi igricu
                menu_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Player1_text.rect.collidepoint(pygame.mouse.get_pos()): # ako se klike na hand solo, pokrece se singleplayer igra
                    menu_running = False
                    PlayerOneGameLoop()
                if pygame.Rect(18, 10, 70, 70).collidepoint(pygame.mouse.get_pos()):# klik na x_icon se izlazi iz igre
                    menu_running = False

        pygame.display.update()                     
        clock.tick(fps)
        
    pygame.quit()
    quit()

def PlayerOneGameLoop():
    game_running = True
    while game_running:
        screen.fill(black)
        letjelica = pygame.image.load('smth-pixilart.png')
        meteor_najmanji = pygame.image.load('Asteroid1.png')
        meteor_srednji = pygame.image.load('medasteroid.png')
        screen.blit(letjelica, (width*0.5, height*0.90))
        screen.blit(meteor_najmanji, (width*0.5, height*0.5))
        screen.blit(meteor_srednji, (width*0.7, height*0.5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ako kliknes na x prozora ugasi igricu
                game_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    game_running = False
                    
        pygame.display.update()                     
        clock.tick(fps)
        
    pygame.quit()
    quit()
    

def main (): #glavna funkcija koja se prva pokrece
    pygame.init()
    main_menu()

    pygame.quit()
    quit()
    
main()