import sys, pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.vx = 0.0
        self.vy = 0.0
        self.platform = False
        self.jumping = False
        self.jump_speed = 0.1
        self.speed = 0.2
        self.box = pygame.Surface((self.w,self.h))
        self.box = self.box.convert()
        self.box.fill((255,0,0))
    def update(self,dt,gravity):
        if not self.platform: self.vy+= gravity
        else:
            if not self.jumping: self.vy = 0.0
        if self.vy > 1.0: self.vy = 1.0
        self.x += self.vx * dt 
        self.y += self.vy * dt 

    def move_left(self):
        self.vx -= self.speed 
    def move_right(self):
        self.vx += self.speed 
    def clear_moving_x(self):
        if self.vx > 0: self.vx -= 0.5
        if self.vx < 0: self.vx += 0.5
    def clear_moving_y(self):
        self.vy = 0.0
    def jump(self):
        if self.platform and self.jumping == False:
            self.y -= 0.1
            self.vy = -self.jump_speed
            self.platform = False
            self.jumping = True

class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w 
        self.h = h
        self.box = pygame.Surface((self.w, self.h))
        self.box = self.box.convert()
        self.box.fill((0,0,255))
    def top_collision(self,player):
        if self.x + self.w < player.x or self.y + self.h < player.y or player.x + player.w < self.x or player.y + player.h < self.y: return False
        else: 
            if self.y > player.y - player.h/4: return True
            else: return False  

class Coin:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.w = 8
        self.h = 8
    def collision(self,player):
        if self.x + self.w < player.x or self.y + self.h < player.y or player.x + player.w < self.x or player.y + player.h < self.y: return False
        else: return True 

class Level_changer:
    def __init__(self, x,y, id):
        self.id = id
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
    def collision(self,player):
        if self.x + self.w < player.x or self.y + self.h < player.y or player.x + player.w < self.x or player.y + player.h < self.y: return False
        else: return True  

def level_change(player, platforms, coins, x, y, new_platforms, newcoins):
    player = Player(x,y)
    platforms = new_platforms
    coins = newcoins
    return player, platforms, coins


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont('Lucida Console',12)
    coins = 0

    size = width, height = 320,240
    speed = [2,2]

    screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
    pygame.display.set_caption('Game window')


    clock = pygame.time.Clock()

    player = Player(30,200)
    platforms = { Platform(0,220,50,20), 
    Platform(80,200,50,20), 
    Platform(150,180,50,20),
    Platform(70,120,40,20),
    Platform(150,80,50,20),
    Platform(200,50,50,20),
    Platform(10,100,50,20), 
    }
    Coins = [ Coin(90,192), Coin(30, 92) ]
    newCoins = []

    LChanger = Level_changer(150,64,1)


    cointex = pygame.Surface((8,8))
    cointex = cointex.convert()
    cointex.fill((255,0,255)) 

    lchangertex = pygame.Surface((16,16))
    lchangertex = lchangertex.convert()
    lchangertex.fill((255,255,0))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    gravity = 0.05

    while 1:
        dt = clock.tick(30)
        if player.y > 400: sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: sys.exit()
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                   player.clear_moving_x()
                #if event.key == pygame.K_UP: #or event.key == pygame.K_DOWN:
                    #player.clear_moving_y()
        player.platform = False
        for platform in platforms:
            if platform.top_collision(player):
                player.platform = True
                player.y = platform.y - player.h
                player.jumping = False
        newCoins = Coins
        for coin in Coins:
            if coin.collision(player): 
                coins+=1
                newCoins.remove(coin)
        

        player.update(dt,gravity)

        if LChanger.collision(player):
            player, platforms, Coins = level_change(player, platforms, Coins, 20, 200, { Platform(0,220,100,20)}, [Coin(50,210)])

        screen.blit(background, (0,0))
        screen.blit(player.box, (player.x,player.y))
        for platform in platforms:
            screen.blit(platform.box,(platform.x, platform.y))
        for coin in Coins:
            screen.blit(cointex,(coin.x,coin.y))
        conistexture = font.render('Coins:'+str(coins), False, (255,255,0))
        screen.blit(lchangertex,(LChanger.x,LChanger.y))



        screen.blit(conistexture,(0,0));

        pygame.display.flip()