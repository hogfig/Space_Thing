# Razvoj Space_Thing

import pygame
import random
import time
import shelve 

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
screen_rect = screen.get_rect()
d  = shelve.open('SaveFiles/highscore.txt')



asteroid_images  = []    #slike razlicitih asteroida, random se bira jedna kad se kreira asteroid
Meteors = [] # meteori u menu
Pew_Pew = [] # metci
Stars = [] #background stars u igri
asteroidi = [] #meteori u igrici
Score = [] # lista za pracenje rezultata
Socore_player2 = [] #lista za pracenje rezultata drugog igraca
LetjeliceAnimacija = [pygame.image.load('Letjelice/letjelica_0.png'),pygame.image.load('Letjelice/letjelica_1.png'),pygame.image.load('Letjelice/letjelica_2.png')]
index = [0]

all_sprites = pygame.sprite.Group()
hearts = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.image.load('Bullets/bullet.png')
        self.rect = self.image.get_rect()
        # bullet position is according the player position
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -15
        self.player = player
 
    def update(self):
        self.rect.y += self.speedy
 
        # if bullet goes off top of window, destroy it
        if self.rect.bottom < 0:
            self.kill()

class Heart(pygame.sprite.Sprite):
    def __init__(self,image, x,y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):             #srce pada i ako izade iz ekrana se obrise
        self.rect.y += 1.7
        if self.rect.top > height:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, health, size):
        super().__init__()
        self.health = health
        self.image = pygame.image.load(image)
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)          #pri kreiranju asteroida bira se random x koordinata
        self.rect.y = random.randrange(-100, -50)
        self.speed = random.randrange(2,4)      
        self.hit_by_player = 'player1'

    def update(self):
        if self.health > 0:
            self.rect.y += self.speed
            if self.rect.top > height:
                self.kill()
        else:
            self.kill() 
            if self.size == "small":
                if self.hit_by_player == 'player1':
                    UpdateScore(10)
                else:
                    UpdateScore2(10)
            else:
                if self.hit_by_player == 'player1':
                    UpdateScore(25)
                else:
                    UpdateScore2(25) 
            if random.random() > 0.98:
                heart = Heart('Animacije/HeartPowerUp.png', self.rect[0], self.rect[1])
                all_sprites.add(heart)
                hearts.add(heart)

counter = 0
class Phases():
    def __init__(self,count):
        self.povecaj_mali = 1
        self.povecaj_srednji = 1
        self.init_time = clock.get_time()
    #Algoritam za kreaciju asteroida
    def LoadAsteroidi(self,count): 
        if count % (fps/2 - self.povecaj_mali) == 0 and count % (fps*2 - self.povecaj_srednji ) == 0:
            small_asteroid = Asteroid('Asteroidi/Asteroid1.png', 1, "small")
            all_sprites.add(small_asteroid)
            asteroids.add(small_asteroid)

            medium_asteroid = Asteroid('Asteroidi/medasteroid.png', 3, "medium")
            all_sprites.add(medium_asteroid)
            asteroids.add(medium_asteroid)

        if count % (fps/2 - self.povecaj_mali) == 0:
            small_asteroid = Asteroid('Asteroidi/Asteroid1.png', 1, "small")
            all_sprites.add(small_asteroid)
            asteroids.add(small_asteroid)
        elif count % (fps*2 - self.povecaj_srednji ) == 0:
            medium_asteroid = Asteroid('Asteroidi/medasteroid.png', 3, "medium")
            all_sprites.add(medium_asteroid)
            asteroids.add(medium_asteroid)

    def phase_0(self,count):
        global counter
        if(counter <= 205):
            S = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',40), (255,255,255), [width / 2, height / 2], 'PHASE 0')
            S.Display() 
            counter+=1  
        else:     
            self.povecaj_mali = 1
            self.povecaj_srednji = 1
            self.LoadAsteroidi(count)
        
    def phase_1(self,count):  
        global counter
        if(counter <= 420):
            S = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',40), (255,255,255), [width / 2, height / 2], 'PHASE 1')
            S.Display()   
            counter+=1
        else:     
            self.povecaj_mali = 10
            self.povecaj_srednji = 50    
            self.LoadAsteroidi(count)
        
    def phase_2(self,count):
        global counter
        if(counter <= 635):
            S = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',40), (255,255,255), [width / 2, height / 2], 'PHASE 2')
            S.Display()     
            counter+=1
        else:     
            self.povecaj_mali = 20
            self.povecaj_srednji = 60   
            self.LoadAsteroidi(count)
        
def init_Phases(count):
    
    if(Score[0] < 1000):
        p=Phases(count)
        p.phase_0(count)
    elif(Score[0]>=1000 and Score[0]<2000):
        p1=Phases(count)
        p1.phase_1(count)
    else:
        p2=Phases(count)
        p2.phase_2(count)


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
class Letjelica(pygame.sprite.Sprite):
    def __init__(self, image, x, y, health):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.health = health

        self.width = 49
        self.height = 55
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 100
        self.last_shot = pygame.time.get_ticks()

    

    def update(self):
        if self.health > 0:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        self.speedx = 0
        self.speedy = 0

    
    
    def shoot(self, player = 'player1'):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            bullet = Bullet(self.rect.centerx, self.rect.top, player)
            all_sprites.add(bullet)
            bullets.add(bullet)

                
def init_Stars():
    for i in range(0, 49): 
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        Stars.append([x,y])

def init_Meteori():
    for m in range(meteor_num):          # dodjeljujes random koordinate za meteore i spremas ih u array  
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        Meteors.append([x,y])

def UpdateScore(num):
    Score[0] += num

def UpdateScore2(num):
    Score[1] += num

def DisplayLife(count, HP, Srce_gore, Srce_dolje, x_kord,y):
    offset = 20
    Srca=[Srce_dolje,Srce_gore]
    for x in range(HP):        
        x_kord -= offset
        if count%fps*2 >= 0 and count%fps*2 <=60 :
            index[0] = 1
        elif count%fps*2 > 60 and count%fps*2 <= 119:
            index[0] = 0
        screen.blit(Srca[index[0]], (x_kord, y))


#Funkcija glavnog menija koja se otvara pri pokretanju igrice
def main_menu():
    menu_running = True
    pygame.mixer.music.load('Pjesme/SpaceThingMain_menu_theme.mp3') #Path do pjesme u folderu
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
        x_icon = pygame.image.load('Menu_icons/x_icon.png') #Slika iksica
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

def GameOver(score):
    game_over_running = True
    pygame.mixer.music.load('Pjesme/SpaceThingMain_menu_theme.mp3') #Path do pjesme u folderu
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    
    while game_over_running == True:
        screen.fill(black)
        GameOverMessage = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',50), (255,255,255), [width/2, height*0.3], 'GAME OVER')
        GameOverMessage.Display()
        GameOverScore = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [(width/2), height*0.4], 'YOUR      SCORE    ' + str(score))
        GameOverScore.Display()
        HighscoreMessage = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',35), (255,255,255), [width/2, height*0.6], 'ALL TIME     HIGHSCORE')
        HighscoreMessage.Display()
        HighscoreNumba = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [(width/2), height*0.7], str(d['highscore']))
        HighscoreNumba.Display()
        PlayAgainMessage = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',50), (255,255,255), [width/2, height*0.85], 'PLAY    AGAIN')
        PlayAgainMessage.Display()
        
        if PlayAgainMessage.rect.collidepoint(pygame.mouse.get_pos()): #ako je mis iznad teksta helping hand napravi 3D kurac
            PlayAgainMessage.font = pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',60)
            PlayAgainMessage.color = (239, 90, 150)
            PlayAgainMessage_3D = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',55), (58,255,249), [width/2, height*0.85], 'PLAY    AGAIN')
            PlayAgainMessage_3D.Display()
            PlayAgainMessage.Display()

        pygame.display.update()                     
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ako kliknes na x prozora ugasi igricu
                game_over_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    game_over_running = False
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and PlayAgainMessage.rect.collidepoint(pygame.mouse.get_pos()):
                game_over_running = False
                pygame.mixer.music.stop()
                PlayerOneGameLoop()
    pygame.quit()
    quit()


def AnimateLetjelica(count, letjelica, letjelica_frame):

    if count % (fps/2) == 0:    
        letjelica_frame += 1   
        if letjelica_frame > 2:
            letjelica_frame  = 0 
        return LetjeliceAnimacija[letjelica_frame], letjelica_frame
        

    return letjelica.image, letjelica_frame  

def PlayerOneGameLoop():
    game_running = True
    count = 0 #brojac koji se koristi u while loopu
    Srce_gore = pygame.image.load('Animacije/HeartUp.png')
    Srce_dolje = pygame.image.load('Animacije/HeartDown.png')
    #Objekt letjelica: position, img_path, promjena_poz_x, promjena_poz_x, broj zivota
    letjelica = Letjelica(pygame.image.load('Letjelice/letjelica_0.png'), width*0.5, height*0.90, 3)
    all_sprites.add(letjelica)
    Score.append(0) 
    Score[0] = 0
    for asteroid in asteroids:
        asteroid.kill()
    crash_sound = pygame.mixer.Sound('Pjesme/Roblox_Death_Sound_Effect.ogg')
    pygame.mixer.music.load('Pjesme/Spacething_Level_1.mp3') #Path do pjesme u folderu
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    letjelica_frame = 0
    

    while game_running:
        screen.fill(black)
        S = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [65, 20], 'SCORE    ' + str(Score[0]))
        S.Display() 
        DisplayLife(count, letjelica.health, Srce_gore, Srce_dolje,width - 20, 10)
        
        

        if letjelica.health == 0:
            letjelica.kill()
            if Score[0] > d['highscore']:     #saves the new score if its bigger than the all time high score
                d['highscore'] = Score[0]
            pygame.mixer.music.stop()
            GameOver(Score[0])


        #Blok za crtanje background zvezda
        for i in Stars:
            if i[1]< height:
                i[1] += 2
                pygame.draw.rect(screen,white,[i[0], i[1], 1, 1])
            elif i[1] > height: 
                i[1] = 1
        
        #NOVI NACIN KRETANJA
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    game_running = False
                if event.key == pygame.K_ESCAPE:
                    letjelica.kill()
                    main_menu()
                if event.key == pygame.K_SPACE:
                    letjelica.shoot()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            letjelica.speedy -= 5
        if pressed[pygame.K_DOWN]:
            letjelica.speedy += 5
        if pressed[pygame.K_LEFT]:
            letjelica.speedx -= 5
        if pressed[pygame.K_RIGHT]:
            letjelica.speedx += 5   
        
        init_Phases(count)

        letjelica.image , letjelica_frame = AnimateLetjelica(count, letjelica, letjelica_frame)
        

        all_sprites.update()            #updejta lokaciju svih spritova
        all_sprites.draw(screen)        #crta sve spritove na ekranu
        

        if count % 50 == 0:             #povecava score otprilike scaku sekundu za 10
            Score[0] += 10



        heartHits = pygame.sprite.spritecollide(letjelica, hearts, True)
        if heartHits:
            letjelica.health += 1

        asteroidHits = pygame.sprite.spritecollide(letjelica, asteroids, True)
        if asteroidHits:
            pygame.mixer.Sound.play(crash_sound)
            letjelica.health -= 1

        pewpew_Hits = pygame.sprite.groupcollide(asteroids, bullets, False, pygame.sprite.collide_circle)
        for hit in pewpew_Hits:
            hit.health -= 1
            
        
        
        #FADE IN VOLUME
        if pygame.mixer.music.get_volume() < 0.4:
            value = pygame.mixer.music.get_volume() + 0.01  
            pygame.mixer.music.set_volume(value)

        letjelica.rect.clamp_ip(screen_rect)      #neda letjelici da izade iz ekrana                     
        
        
        pygame.display.update()
        
        clock.tick(fps)
        count += 1
        
    pygame.quit()
    quit()
    
def GameOver2(score1, score2):
    game_over_running = True
    pygame.mixer.music.load('Pjesme/SpaceThingMain_menu_theme.mp3') #Path do pjesme u folderu
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while game_over_running == True:
        screen.fill(black)
        GameOverMessage = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',50), (255,255,255), [width/2, height*0.3], 'GAME OVER')
        GameOverMessage.Display()
        GameOverScore1 = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [(width*0.2), height*0.4], 'PLAYER1      SCORE    ' + str(score1))
        GameOverScore1.Display()
        GameOverScore2 = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [(width*0.8), height*0.4], 'PLAYER2      SCORE    ' + str(score2))
        GameOverScore2.Display()
        HighscoreMessage = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',35), (255,255,255), [width/2, height*0.6], 'ALL TIME     HIGHSCORE')
        HighscoreMessage.Display()
        HighscoreNumba = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,255,255), [(width/2), height*0.7], str(d['highscore']))
        HighscoreNumba.Display()
        PlayAgainMessage = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',50), (255,255,255), [width/2, height*0.85], 'PLAY    AGAIN')
        PlayAgainMessage.Display()
        
        if PlayAgainMessage.rect.collidepoint(pygame.mouse.get_pos()): #ako je mis iznad teksta helping hand napravi 3D kurac
            PlayAgainMessage.font = pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',60)
            PlayAgainMessage.color = (239, 90, 150)
            PlayAgainMessage_3D = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',55), (58,255,249), [width/2, height*0.85], 'PLAY    AGAIN')
            PlayAgainMessage_3D.Display()
            PlayAgainMessage.Display()

        pygame.display.update()                     
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ako kliknes na x prozora ugasi igricu
                game_over_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    game_over_running = False
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and PlayAgainMessage.rect.collidepoint(pygame.mouse.get_pos()):
                game_over_running = False
                pygame.mixer.music.stop()
                PlayerTwoGameLoop()
    pygame.quit()
    quit()



def PlayerTwoGameLoop():   #ugl isto kao player1 ali za dva plejera
    game_running = True
    count = 0 #brojac koji se koristi u while loopu
    Srce_gore = pygame.image.load('Animacije/HeartUp.png')
    Srce_dolje = pygame.image.load('Animacije/HeartDown.png')
    for asteroid in asteroids:
        asteroid.kill()
    Score.append(0) 
    Score.append(0)
    Score[0] = 0
    Score[1] = 0
    crash_sound = pygame.mixer.Sound('Pjesme/Roblox_Death_Sound_Effect.ogg')
    pygame.mixer.music.load('Pjesme/Spacething_Level_1.mp3') #Path do pjesme u folderu
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    #Objekt letjelica: position, img_path, promjena_poz_x, promjena_poz_x
    letjelica1 = Letjelica(pygame.image.load('Letjelice/letjelica_0.png'), width*0.5 - 40, height*0.90, 3)
    all_sprites.add(letjelica1)
    letjelica2 = Letjelica(pygame.image.load('Letjelice/smth-pixilart.png'), width*0.5 + 40, height*0.90, 3)
    all_sprites.add(letjelica2)
    while game_running:
        screen.fill(black)
        S_1 = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (255,0,0), [65, 20], 'PLAYER 1    ' + str(Score[0]))
        S_2 = Message_to_screen(pygame.font.Font('arcadeclassic/ARCADECLASSIC.TTF',25), (0,255,0), [820, 20], 'PLAYER 2   ' + str(Score[1]))
        
        S_1.Display() 
        S_2.Display()
        DisplayLife(count, letjelica1.health, Srce_gore, Srce_dolje, 65, 30)
        DisplayLife(count, letjelica2.health, Srce_gore, Srce_dolje, width-100, 30)



        if letjelica1.health == 0:
            letjelica1.kill()
            letjelica1.rect.x = width + 50     #makne letjelicu off screen, inace nestane slika letjelice ali njezin rect je josuvijek na ekranu i zabija se u asteroide

        if letjelica2.health == 0:
            letjelica2.kill()
            letjelica2.rect.x = width + 50    #makne letjelicu off screen, inace nestane slika letjelice ali njezin rect je josuvijek na ekranu i zabija se u asteroide
        
        if letjelica1.health <= 0 and letjelica2.health <= 0:    #ako su obje letjelice mrtve onda je game over
            if Score[0] > d['highscore']:     #saves the new score if its bigger than the all time high score
                d['highscore'] = Score[0]
            if Score[1] > d['highscore']:     #saves the new score if its bigger than the all time high score
                d['highscore'] = Score[1]
            pygame.mixer.music.stop()
            GameOver2(Score[0], Score[1])
            

        #Blok za crtanje background zvezda
        for i in Stars:
            if i[1]< height:
                i[1] += 2
                pygame.draw.rect(screen,white,[i[0], i[1], 1, 1])
            elif i[1] > height: 
                i[1] = 1
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN: #ako kliknes q dok se vrti igrica izadi iz igrice
                if event.key == pygame.K_q:
                    game_running = False
                if event.key == pygame.K_ESCAPE:
                    letjelica1.kill()
                    letjelica2.kill()
                    main_menu()
                if event.key == pygame.K_SPACE:
                    if letjelica2.health > 0:
                        letjelica2.shoot('player2')
                if event.key == pygame.K_RETURN:
                    if letjelica1.health > 0:
                        letjelica1.shoot('player1')
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            letjelica1.speedy -= 5
        if pressed[pygame.K_DOWN]:
            letjelica1.speedy += 5
        if pressed[pygame.K_LEFT]:
            letjelica1.speedx -= 5
        if pressed[pygame.K_RIGHT]:
            letjelica1.speedx += 5
        if pressed[pygame.K_w]:
            letjelica2.speedy -= 5
        if pressed[pygame.K_s]:
            letjelica2.speedy += 5
        if pressed[pygame.K_a]:
            letjelica2.speedx -= 5
        if pressed[pygame.K_d]:
            letjelica2.speedx += 5 

        init_Phases(count)

        all_sprites.update()            #updejta lokaciju svih spritova
        all_sprites.draw(screen)        #crta sve spritove na ekranu

        heartHits = pygame.sprite.spritecollide(letjelica1, hearts, True)
        if heartHits:
            letjelica1.health += 1

        asteroidHits = pygame.sprite.spritecollide(letjelica1, asteroids, True)
        if asteroidHits:
            pygame.mixer.Sound.play(crash_sound)
            letjelica1.health -= 1
        
        heartHits = pygame.sprite.spritecollide(letjelica2, hearts, True)
        if heartHits:
            letjelica2.health += 1

        asteroidHits = pygame.sprite.spritecollide(letjelica2, asteroids, True)
        if asteroidHits:
            pygame.mixer.Sound.play(crash_sound)
            letjelica2.health -= 1

        pewpew_Hits = pygame.sprite.groupcollide(asteroids, bullets, False, True)
        for asteroid, bullet in pewpew_Hits.items():
            asteroid.health -= 1
            asteroid.hit_by_player = bullet[0].player
        

        

        letjelica1.rect.clamp_ip(screen_rect)
        letjelica2.rect.clamp_ip(screen_rect)  

        count +=1
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
