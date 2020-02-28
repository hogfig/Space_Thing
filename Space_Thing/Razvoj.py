# Razvoj Space_Thing

import pygame
import random
import time

white=(255,255,255)
orange = (255,162,0)
black=(0,0,0)
size=width,height= 920,640
screen=pygame.display.set_mode(size)
clock= pygame.time.Clock()
fps= 60
meteor_speed = 5
meteor_size = 1
asteroid_speed = 3
meteor_num = 200

Meteors = [] # meteori u menu
Pew_Pew = [] # metci
Stars = [] #background stars u igri
asteroidi = [] #meteori u igrici
Score = [] # lista za pracenje rezultata
index = [0]
class Asteroidi():
    def __init__(self, position, health, img, size):
        self.position = position
        self.health = health
        self.img = img
        self.size = size
        
        rect = self.img.get_rect()
        self.rect = pygame.Rect(position[0], position[1], rect[2], rect[3])       

    def To_screen(self,count, i):
        if self.health != 0:
            self.rect[1] += asteroid_speed
            screen.blit(self.img,(self.rect[0],self.rect[1]))
        else:
            if self.size == 'small':
                asteroidi.remove(i)
                UpdateScore(10)
            else:
                asteroidi.remove(i)
                UpdateScore(25)

    #puni listu meteori s objektima Meteori 
    def LoadAsteroidi(count):
        if count % fps == 0:
            small = Asteroidi([random.randrange(0, width),-10], 1, pygame.image.load('Asteroidi/Asteroid1.png'), 'small')
            asteroidi.append(small)
        elif count % 201 == 0:
            medium = Asteroidi([random.randrange(0, width),-20], 3, pygame.image.load('Asteroidi/medasteroid.png'), 'medium')
            asteroidi.append(medium)

    def CheckAsteroid(count,):
        if len(asteroidi) > 0:
            for i in asteroidi:
                i.To_screen(count, i) 

        
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

       
#Klasa za mehaniku letjelice i metaka
class Letjelica():
    def __init__(self, position, img_path, promjena_poz_x, promjena_poz_y,health):
        self.position = position
        self.img_path = pygame.image.load(img_path)
        self.promjena_poz_x = promjena_poz_x
        self.promjena_poz_y = promjena_poz_y
        self.width = 49
        self.height = 55
        self.health = health
        rect = self.img_path.get_rect()
        self.rect = pygame.Rect(position[0], position[1], rect[2], rect[3])

    def pew_pew(self):
        x = self.position[0] + 28
        y = self.position[1] - 5
        size = 3
        pew = pygame.Rect(x,y,size,size)
        Pew_Pew.append(pew)

    def LoadPewPew(): # za pucanje metaka, kada je u dodiru sa asteroidom obrisi metak i skini HP asteroidu
        if len(Pew_Pew) > 0:
            for pew in Pew_Pew :
                if len(asteroidi) > 0:
                    for i in asteroidi:
                        if pew.colliderect(i.rect):
                            Pew_Pew.remove(pew)
                            i.health -= 1
                            
                if pew[1] > 0:
                    pew[1] -= 10
                    pygame.draw.rect(screen,orange,pew)
                elif pew[1] < 0:
                    Pew_Pew.remove(pew)
                
def init_Stars():
    for i in range(0, 49): 
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        Stars.append([x,y])

def init_Meteori():
    for m in range(meteor_num): # dodjeljujes random koordinate za meteore i spremas ih u array  
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        Meteors.append([x,y])

def UpdateScore(num):
    Score[0] += num

def DisplayLife(count, HP, Srce_gore, Srce_dolje):
    offset = 20
    x_kord = width - 20
    Srca=[Srce_dolje,Srce_gore]
    for x in range(HP):        
        x_kord -= offset
        if count%fps*2 >= 0 and count%fps*2 <=60 :
            index[0] = 1
        elif count%fps*2 > 60 and count%fps*2 <= 119:
            index[0] = 0
        screen.blit(Srca[index[0]], (x_kord, 10))


#Funkcija glavnog menija koja se otvara pri pokretanju igrice
def main_menu():
    menu_running = True
    pygame.mixer.music.load('Pjesme\SpaceThingMain_menu_theme.mp3') #Path do pjesme u folderu
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
        
        space_img = pygame.image.load('Menu_icons/space_w.png') #Slika rakete
        x_icon = pygame.image.load('Menu_icons/x_icon.png') #Slika iksića
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
            
            if not(Title.rect.collidepoint(i) or Player1_text.rect.collidepoint(i)
                   or Player2_text.rect.collidepoint(i)
                   or pygame.Rect(404, 256, 116, 120).collidepoint(i)
                   or pygame.Rect(18, 10, 70, 70).collidepoint(i)):  # koristis tako da ti meteori padaju iznad teksta i svih ostalih objekta na ekranu
                
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
            if event.type == pygame.MOUSEBUTTONDOWN and Player1_text.rect.collidepoint(pygame.mouse.get_pos()):
                menu_running = False
                pygame.mixer.music.stop()
                PlayerOneGameLoop()
            if event.type == pygame.MOUSEBUTTONDOWN and Player2_text.rect.collidepoint(pygame.mouse.get_pos()):
                menu_running = False
                pygame.mixer.music.stop()
                PlayerTwoGameLoop()
            if event.type == pygame.MOUSEBUTTONDOWN and x_icon.get_rect().collidepoint(pygame.mouse.get_pos()):
                menu_running = False

        pygame.display.update()                     
        clock.tick(fps)

    pygame.quit()
    quit()

def PlayerOneGameLoop():
    game_running = True
    count = 0 #brojac koji se koristi u while loopu
    Srce_gore = pygame.image.load('Animacije/HeartUp.png')
    Srce_dolje = pygame.image.load('Animacije/HeartDown.png')
    #Objekt letjelica: position, img_path, promjena_poz_x, promjena_poz_x, broj zivota
    letjelica = Letjelica([width*0.5,height*0.90], 'Letjelice/smth-pixilart.png', 0, 0, 3)
    Score.append(0) 

    while game_running:
        screen.fill(black)
        S = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [65, 20], 'SCORE    ' + str(Score[0]))
        S.Display() 
        DisplayLife(count, letjelica.health, Srce_gore, Srce_dolje)
        for i in asteroidi:
            if letjelica.rect.colliderect(i.rect):
                letjelica.health -= 1 
        #Blok za crtanje background zvezda
        for i in Stars:
            if i[1]< height:
                i[1] += 2
                pygame.draw.rect(screen,white,[i[0], i[1], 1, 1])
            elif i[1] > height: 
                i[1] = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ako kliknes na x prozora ugasi igricu
                game_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    game_running = False
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_LEFT:
                   # letjelica.promjena_poz_x = -5
                    letjelica.rect.move_ip(-5,0)
                if event.key == pygame.K_RIGHT:
                    #letjelica.promjena_poz_x = 5  
                    letjelica.rect.move_ip(5,0)
                if event.key == pygame.K_UP:
                    #letjelica.promjena_poz_y = -5
                    letjelica.rect.move_ip(0,-5)
                if event.key == pygame.K_DOWN:
                    #letjelica.promjena_poz_y = 5
                    letjelica.rect.move_ip(0,5)
                if event.key == pygame.K_SPACE:
                    letjelica.pew_pew()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    #letjelica.promjena_poz_x = 0
                    letjelica.rect.move_ip(0,0)
                if event.key == pygame.K_RIGHT:
                    #letjelica.promjena_poz_x = 0
                    letjelica.rect.move_ip(0,0)
                if event.key == pygame.K_UP:
                    #letjelica.promjena_poz_y = 0
                    letjelica.rect.move_ip(0,0)
                if event.key == pygame.K_DOWN:
                    #letjelica.promjena_poz_y = 0
                    letjelica.rect.move_ip(0,0)
                    
        if (letjelica.position[0] + letjelica.promjena_poz_x) < (width-letjelica.width) and (letjelica.position[0] + letjelica.promjena_poz_x) > -11:
            letjelica.position[0] += letjelica.promjena_poz_x
        if (letjelica.position[1] + letjelica.promjena_poz_y) < (height-letjelica.height+5) and (letjelica.position[1] + letjelica.promjena_poz_y) > 0:
            letjelica.position[1] += letjelica.promjena_poz_y                 
        
        #Mehanizam za pucanje, crta metak dok je god u okvirima ekrana, kad izade
        #presane crtat i mice metak iz arraya. Ako se sudari sa meteorom isto tako.
        Letjelica.LoadPewPew()
        #Mehanizam za meteore
        Asteroidi.LoadAsteroidi(count)
        #Provjeri ako ima asteroida i onda zovi funkciju da ih crtas
        Asteroidi.CheckAsteroid(count)                            

        screen.blit(letjelica.img_path,(letjelica.rect[0],letjelica.rect[1]))

        #screen.blit(letjelica.img_path, (letjelica.position[0], letjelica.position[1]))      
        pygame.display.update()
        
        clock.tick(fps)
        count += 1
        
    pygame.quit()
    quit()
    
    
def PlayerTwoGameLoop():   #ugl isto kao player1 ali za dva plejera
    game_running = True

    #Objekt letjelica: position, img_path, promjena_poz_x, promjena_poz_x
    letjelica1 = Letjelica([width*0.4,height*0.90], 'Letjelice/smth-pixilart.png', 0, 0, 3)
    letjelica2 = Letjelica([width*0.6,height*0.90], 'Letjelice/smth-pixilart.png', 0, 0, 3)
    
    while game_running:
        screen.fill(black)

        #Blok za crtanje background zvezda
        for i in Stars:
            if i[1]< height:
                i[1] += 2
                pygame.draw.rect(screen,white,[i[0], i[1], 1, 1])
            elif i[1] > height: 
                i[1] = 1
                
 #       meteor_najmanji = pygame.image.load('Asteroidi/Asteroid1.png')
 #       meteor_srednji = pygame.image.load('Asteroidi/medasteroid.png') 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ako kliknes na x prozora ugasi igricu
                game_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    game_running = False
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_LEFT:
                    letjelica1.promjena_poz_x = -5
                if event.key == pygame.K_RIGHT:
                    letjelica1.promjena_poz_x = 5
                if event.key == pygame.K_UP:
                    letjelica1.promjena_poz_y = -5
                if event.key == pygame.K_DOWN:
                    letjelica1.promjena_poz_y = 5
                if event.key == pygame.K_SPACE:
                    letjelica1.pew_pew()
                if event.key == pygame.K_a:
                    letjelica2.promjena_poz_x = -5
                if event.key == pygame.K_d:
                    letjelica2.promjena_poz_x = 5
                if event.key == pygame.K_w:
                    letjelica2.promjena_poz_y = -5
                if event.key == pygame.K_s:
                    letjelica2.promjena_poz_y = 5
                if event.key == pygame.K_RETURN:
                    letjelica2.pew_pew()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    letjelica1.promjena_poz_x = 0
                if event.key == pygame.K_RIGHT:
                    letjelica1.promjena_poz_x = 0
                if event.key == pygame.K_UP:
                    letjelica1.promjena_poz_y = 0
                if event.key == pygame.K_DOWN:
                    letjelica1.promjena_poz_y = 0
                if event.key == pygame.K_a:
                    letjelica2.promjena_poz_x = 0
                if event.key == pygame.K_d:
                    letjelica2.promjena_poz_x = 0
                if event.key == pygame.K_w:
                    letjelica2.promjena_poz_y = 0
                if event.key == pygame.K_s:
                    letjelica2.promjena_poz_y = 0

        if (letjelica1.position[0] + letjelica1.promjena_poz_x) < (width-letjelica1.width) and (letjelica1.position[0] + letjelica1.promjena_poz_x) > -11:
            letjelica1.position[0] += letjelica1.promjena_poz_x

        if (letjelica1.position[1] + letjelica1.promjena_poz_y) < (height-letjelica1.height+5) and (letjelica1.position[1] + letjelica1.promjena_poz_y) > 0:
            letjelica1.position[1] += letjelica1.promjena_poz_y


        if (letjelica2.position[0] + letjelica2.promjena_poz_x) < (width-letjelica2.width) and (letjelica2.position[0] + letjelica2.promjena_poz_x) > -11:
            letjelica2.position[0] += letjelica2.promjena_poz_x

        if (letjelica2.position[1] + letjelica2.promjena_poz_y) < (height-letjelica2.height+5) and (letjelica2.position[1] + letjelica2.promjena_poz_y) > 0:
            letjelica2.position[1] += letjelica2.promjena_poz_y
        

        #Mehanizam za pucanje, crta metak dok je god u okvirima ekrana, kad izade
        #presane crtat i mice metak iz arraya
        if len(Pew_Pew) > 0:
            for x in Pew_Pew :
                if x[1] > 0:
                    x[1] -= 10
                    pygame.draw.rect(screen,orange,x)
                elif x[1] < 0:
                    Pew_Pew.remove(x)
                                 
        screen.blit(letjelica1.img_path, (letjelica1.position[0], letjelica1.position[1]))
        screen.blit(letjelica2.img_path, (letjelica2.position[0], letjelica2.position[1]))
 #       screen.blit(meteor_najmanji, (width*0.5, height*0.5))
 #       screen.blit(meteor_srednji, (width*0.7, height*0.5))
        pygame.display.update()
        
        clock.tick(fps)
        
    pygame.quit()
    quit()

    
def main (): #glavna funkcija koja se prva pokrece
    
    init_Stars()
    init_Meteori()


    pygame.init()
    main_menu()

    pygame.quit()
    quit()
    
main()
