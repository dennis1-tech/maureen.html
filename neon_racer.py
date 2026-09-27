import pygame,random,math,os,json
from array import array
pygame.init()
try:
    pygame.mixer.init()
except:
    pass
WIDTH,HEIGHT=900,700
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("NEON PYTHON RACER")
clock=pygame.time.Clock()
FPS=60
BLACK=(5,5,15)
WHITE=(240,240,255)
CYAN=(0,255,255)
PINK=(255,40,180)
PURPLE=(170,50,255)
GREEN=(50,255,120)
YELLOW=(255,230,50)
RED=(255,50,70)
BLUE=(50,120,255)
ORANGE=(255,130,30)
GRAY=(70,70,90)
FONT_BIG=pygame.font.SysFont("arial",64,True)
FONT_TITLE=pygame.font.SysFont("arial",46,True)
FONT_MEDIUM=pygame.font.SysFont("arial",30,True)
FONT_SMALL=pygame.font.SysFont("arial",22)
FONT_TINY=pygame.font.SysFont("arial",17)
HIGH_SCORE_FILE="neon_highscore.json"
def load_high_score():
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE,"r") as f:
                data=json.load(f)
                return int(data.get("high_score",0))
    except:
        pass
    return 0
def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE,"w") as f:
            json.dump({"high_score":score},f)
    except:
        pass
high_score=load_high_score()
def create_tone(frequency,duration=0.12,volume=0.25):
    try:
        rate=44100
        samples=int(rate*duration)
        buffer=array("h")
        amplitude=int(32767*volume)
        for i in range(samples):
            value=int(amplitude*math.sin(2*math.pi*frequency*i/rate))
            buffer.append(value)
        return pygame.mixer.Sound(buffer=buffer)
    except:
        return None
SOUND_COIN=create_tone(900,0.08,0.25)
SOUND_CRASH=create_tone(100,0.25,0.35)
SOUND_LEVEL=create_tone(600,0.15,0.25)
SOUND_SELECT=create_tone(500,0.08,0.20)
SOUND_START=create_tone(700,0.15,0.25)
def play_sound(sound):
    if sound:
        try:
            sound.play()
        except:
            pass
def draw_text(text,font,color,x,y,center=True):
    surface=font.render(str(text),True,color)
    if center:
        rect=surface.get_rect(center=(x,y))
    else:
        rect=surface.get_rect(topleft=(x,y))
    screen.blit(surface,rect)
stars=[]
for i in range(100):
    stars.append([
        random.randint(0,WIDTH),
        random.randint(0,HEIGHT),
        random.randint(1,3)
    ])
def draw_background():
    screen.fill(BLACK)
    for star in stars:
        x,y,size=star
        pygame.draw.circle(
            screen,
            (40,40+size*20,70+size*30),
            (x,y),
            size
        )
    for i in range(8):
        y=120+i*8
        pygame.draw.line(
            screen,
            (15,20+i*3,40+i*5),
            (0,y),
            (WIDTH,y),
            1
        )
ROAD_LEFT=210
ROAD_RIGHT=690
ROAD_WIDTH=ROAD_RIGHT-ROAD_LEFT
LANE_WIDTH=ROAD_WIDTH//3
road_lines=[]
for i in range(15):
    road_lines.append(i*60)

def update_road(speed):
    for i in range(len(road_lines)):
        road_lines[i]+=speed
        if road_lines[i]>HEIGHT:
            road_lines[i]-=900
def draw_road():
    pygame.draw.rect(
        screen,
        (18,18,30),
        (ROAD_LEFT,0,ROAD_WIDTH,HEIGHT)
    )
    pygame.draw.line(
        screen,
        CYAN,
        (ROAD_LEFT,0),
        (ROAD_LEFT,HEIGHT),
        4
    )
    pygame.draw.line(
        screen,
        PINK,
        (ROAD_RIGHT,0),
        (ROAD_RIGHT,HEIGHT),
        4
    )
    for y in road_lines:
        for lane in range(1,3):
            x=ROAD_LEFT+lane*LANE_WIDTH
            pygame.draw.rect(
                screen,
                (50,50,70),
                (x-2,y,4,35)
            )

CAR_TYPES=[
    {"name":"CYBER","color":CYAN,"speed":7,"health":3},
    {"name":"PHANTOM","color":PURPLE,"speed":9,"health":2},
    {"name":"TITAN","color":ORANGE,"speed":6,"health":5}
]
class Player:
    def __init__(self,car_index):
        self.data=CAR_TYPES[car_index]
        self.width=55
        self.height=95
        self.x=WIDTH//2
        self.y=HEIGHT-150
        self.speed=self.data["speed"]
        self.health=self.data["health"]
        self.rect=pygame.Rect(
            int(self.x-self.width//2),
            int(self.y),
            self.width,
            self.height
        )
    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x-=self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x+=self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y-=self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y+=self.speed
        self.x=max(
            ROAD_LEFT+self.width//2,
            min(ROAD_RIGHT-self.width//2,self.x)
        )
        self.y=max(
            100,
            min(HEIGHT-120,self.y)
        )
        self.rect=pygame.Rect(
            int(self.x-self.width//2),
            int(self.y),
            self.width,
            self.height
        )
    def draw(self):
        color=self.data["color"]
        pygame.draw.rect(
            screen,
            (20,20,35),
            self.rect.inflate(14,14),
            border_radius=12
        )
        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            BLACK,
            (
                self.rect.x+9,
                self.rect.y+15,
                self.width-18,
                27
            ),
            border_radius=6
        )
        pygame.draw.rect(
            screen,
            WHITE,
            (
                self.rect.centerx-3,
                self.rect.y+5,
                6,
                self.height-10
            )
        )
        pygame.draw.circle(
            screen,
            YELLOW,
            (self.rect.left+10,self.rect.bottom-12),
            5
        )
        pygame.draw.circle(
            screen,
            YELLOW,
            (self.rect.right-10,self.rect.bottom-12),
            5
        )
class Enemy:
    def __init__(self,level):
        self.width=55
        self.height=90
        lane=random.randint(0,2)
        self.x=ROAD_LEFT+lane*LANE_WIDTH+LANE_WIDTH//2
        self.y=-120
        self.speed=random.randint(4+level,7+level)
        self.color=random.choice([
            RED,BLUE,PINK,GREEN,ORANGE
        ])
        self.rect=pygame.Rect(
            int(self.x-self.width//2),
            int(self.y),
            self.width,
            self.height
        )
    def update(self):
        self.y+=self.speed
        self.rect.y=int(self.y)
    def draw(self):
        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            BLACK,
            (
                self.rect.x+9,
                self.rect.y+15,
                self.width-18,
                27
            ),
            border_radius=6
        )
        pygame.draw.circle(
            screen,
            RED,
            (self.rect.left+10,self.rect.top+8),
            5
        )
        pygame.draw.circle(
            screen,
            RED,
            (self.rect.right-10,self.rect.top+8),
            5
        )
class Coin:
    def __init__(self,level):
        lane=random.randint(0,2)
        self.x=ROAD_LEFT+lane*LANE_WIDTH+LANE_WIDTH//2
        self.y=-40
        self.speed=5+level
        self.radius=13
    def update(self):
        self.y+=self.speed

    def draw(self):
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(self.x),int(self.y)),
            self.radius
        )
        pygame.draw.circle(
            screen,
            BLACK,
            (int(self.x),int(self.y)),
            6
        )
    def get_rect(self):
        return pygame.Rect(
            int(self.x-self.radius),
            int(self.y-self.radius),
            self.radius*2,
            self.radius*2
        )
particles=[]
def create_explosion(x,y):
    for i in range(30):
        particles.append({
            "x":x,
            "y":y,
            "dx":random.uniform(-4,4),
            "dy":random.uniform(-4,4),
            "life":random.randint(20,50)
        })
def update_particles():
    for particle in particles[:]:
        particle["x"]+=particle["dx"]
        particle["y"]+=particle["dy"]
        particle["life"]-=1
        if particle["life"]<=0:
            particles.remove(particle)
def draw_particles():
    for particle in particles:
        pygame.draw.circle(
            screen,
            ORANGE,
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            3
        )
def button(text,rect,color):
    hovered=rect.collidepoint(pygame.mouse.get_pos())
    current_color=WHITE if hovered else color
    pygame.draw.rect(
        screen,
        current_color,
        rect,
        border_radius=10
    )
    pygame.draw.rect(
        screen,
        BLACK,
        rect,
        3,
        border_radius=10
    )
    draw_text(
        text,
        FONT_SMALL,
        BLACK,
        rect.centerx,
        rect.centery
    )
def controls_screen():
    while True:
        draw_background()
        draw_text(
            "HOW TO PLAY",
            FONT_TITLE,
            CYAN,
            WIDTH//2,
            70
        )
        controls=[
            ("W / UP","Move Forward"),
            ("S / DOWN","Move Backward"),
            ("A / LEFT","Move Left"),
            ("D / RIGHT","Move Right"),
            ("P","Pause / Resume"),
            ("ESC","Main Menu"),
            ("MOUSE","Select Buttons / Cars")
        ]
        y=145
        for key,action in controls:
            pygame.draw.rect(
                screen,
                (20,20,40),
                (150,y-20,600,45),
                border_radius=8
            )
            draw_text(
                key,
                FONT_SMALL,
                YELLOW,
                310,
                y
            )
            draw_text(
                action,
                FONT_SMALL,
                WHITE,
                540,
                y
            )
            y+=55
        draw_text(
            "YELLOW COINS = +50 POINTS",
            FONT_SMALL,
            YELLOW,
            WIDTH//2,
            535
        )
        draw_text(
            "AVOID ENEMY CARS",
            FONT_SMALL,
            RED,
            WIDTH//2,
            570
        )
        back=pygame.Rect(
            WIDTH//2-120,
            615,
            240,
            50
        )
        button("BACK",back,PURPLE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return "quit"
            if event.type==pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    return "back"
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return "back"
        clock.tick(FPS)
def car_selection():
    selected=0
    while True:
        draw_background()
        draw_text(
            "SELECT YOUR CAR",
            FONT_TITLE,
            CYAN,
            WIDTH//2,
            80
        )
        for i,car in enumerate(CAR_TYPES):
            x=160+i*290
            box=pygame.Rect(
                x-100,
                180,
                200,
                300
            )
            pygame.draw.rect(
                screen,
                (15,15,30),
                box,
                border_radius=15
            )
            pygame.draw.rect(
                screen,
                car["color"],
                box,
                3,
                border_radius=15
            )
            preview=pygame.Rect(
                x-30,
                220,
                60,
                100
            )
            pygame.draw.rect(
                screen,
                car["color"],
                preview,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (x-20,235,40,25),
                border_radius=5
            )
            draw_text(
                car["name"],
                FONT_MEDIUM,
                car["color"],
                x,
                350
            )
            draw_text(
                "Speed: "+str(car["speed"]),
                FONT_SMALL,
                WHITE,
                x,
                390
            )
            draw_text(
                "Health: "+str(car["health"]),
                FONT_SMALL,
                WHITE,
                x,
                425
            )
            if i==selected:
                pygame.draw.rect(
                    screen,
                    YELLOW,
                    box.inflate(10,10),
                    3,
                    border_radius=18
                )
        back=pygame.Rect(
            WIDTH//2-120,
            540,
            240,
            55
        )
        button("BACK",back,RED)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return None
            if event.type==pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    x=160+i*290
                    box=pygame.Rect(
                        x-100,
                        180,
                        200,
                        300
                    )
                    if box.collidepoint(event.pos):
                        selected=i
                        play_sound(SOUND_SELECT)
                if back.collidepoint(event.pos):
                    return selected
        clock.tick(FPS)
def start_menu():
    global selected_car
    while True:
        draw_background()
        draw_text(
            "NEON",
            FONT_BIG,
            CYAN,
            WIDTH//2,
            80
        )
        draw_text(
            "PYTHON RACER",
            FONT_TITLE,
            PINK,
            WIDTH//2,
            140
        )
        draw_text(
            "High Score: "+str(high_score),
            FONT_SMALL,
            YELLOW,
            WIDTH//2,
            190
        )
        start=pygame.Rect(
            WIDTH//2-150,
            230,
            300,
            55
        )
        cars=pygame.Rect(
            WIDTH//2-150,
            300,
            300,
            55
        )
        controls=pygame.Rect(
            WIDTH//2-150,
            370,
            300,
            55
        )
        quit_button=pygame.Rect(
            WIDTH//2-150,
            440,
            300,
            55
        )
        button("START RACE",start,CYAN)
        button("SELECT CAR",cars,PURPLE)
        button("CONTROLS",controls,GREEN)
        button("QUIT",quit_button,RED)
        draw_text(
            "WASD / ARROWS = DRIVE",
            FONT_TINY,
            WHITE,
            WIDTH//2,
            545
        )
        draw_text(
            "Collect coins • Avoid enemies • Level up",
            FONT_TINY,
            GRAY,
            WIDTH//2,
            575
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return "quit"
            if event.type==pygame.MOUSEBUTTONDOWN:
                if start.collidepoint(event.pos):
                    play_sound(SOUND_START)
                    return "start"
                if cars.collidepoint(event.pos):
                    selected=car_selection()
                    if selected is not None:
                        selected_car=selected
                if controls.collidepoint(event.pos):
                    result=controls_screen()
                    if result=="quit":
                        return "quit"
                if quit_button.collidepoint(event.pos):
                    return "quit"
        clock.tick(FPS)
def draw_hud(player,score,coins,level):
    draw_text(
        "SCORE: "+str(score),
        FONT_SMALL,
        WHITE,
        20,
        20,
        False
    )
    draw_text(
        "COINS: "+str(coins),
        FONT_SMALL,
        YELLOW,
        20,
        50,
        False
    )
    draw_text(
        "LEVEL: "+str(level),
        FONT_SMALL,
        CYAN,
        WIDTH-150,
        20,
        False
    )
    draw_text(
        "HEALTH:",
        FONT_SMALL,
        WHITE,
        WIDTH-200,
        55,
        False
    )
    for i in range(player.health):
        pygame.draw.rect(
            screen,
            RED,
            (
                WIDTH-90+i*22,
                60,
                16,
                16
            ),
            border_radius=4
        )
def pause_screen():
    draw_text(
        "PAUSED",
        FONT_BIG,
        YELLOW,
        WIDTH//2,
        HEIGHT//2-40
    )
    draw_text(
        "Press P to continue",
        FONT_SMALL,
        WHITE,
        WIDTH//2,
        HEIGHT//2+30
    )
    pygame.display.flip()
def game_over(score,coins):
    global high_score
    new_record=False
    if score>high_score:
        high_score=score
        save_high_score(score)
        new_record=True
    while True:
        draw_background()
        draw_text(
            "GAME OVER",
            FONT_BIG,
            RED,
            WIDTH//2,
            150
        )
        draw_text(
            "Score: "+str(score),
            FONT_MEDIUM,
            WHITE,
            WIDTH//2,
            240
        )
        draw_text(
            "Coins: "+str(coins),
            FONT_MEDIUM,
            YELLOW,
            WIDTH//2,
            285
        )
        if new_record:
            draw_text(
                "NEW HIGH SCORE!",
                FONT_MEDIUM,
                GREEN,
                WIDTH//2,
                340
            )
        else:
            draw_text(
                "High Score: "+str(high_score),
                FONT_MEDIUM,
                CYAN,
                WIDTH//2,
                340
            )
        restart=pygame.Rect(
            WIDTH//2-150,
            410,
            300,
            60
        )
        menu=pygame.Rect(
            WIDTH//2-150,
            490,
            300,
            60
        )
        button("PLAY AGAIN",restart,GREEN)
        button("MAIN MENU",menu,CYAN)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return "quit"
            if event.type==pygame.MOUSEBUTTONDOWN:
                if restart.collidepoint(event.pos):
                    return "restart"
                if menu.collidepoint(event.pos):
                    return "menu"
        clock.tick(FPS)
def game():
    player=Player(selected_car)
    enemies=[]
    coins_list=[]
    score=0
    coins=0
    level=1
    spawn_timer=0
    coin_timer=0
    paused=False
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return "quit"
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    paused=not paused
                if event.key==pygame.K_ESCAPE:
                    return "menu"
        if paused:
            draw_background()
            draw_road()
            player.draw()
            for enemy in enemies:
                enemy.draw()
            for coin in coins_list:
                coin.draw()
            pause_screen()
            continue
        new_level=1+score//500
        if new_level>level:
            level=new_level
            play_sound(SOUND_LEVEL)
        update_road(5+level)
        player.update()
        spawn_timer+=1
        spawn_rate=max(
            20,
            70-level*5
        )
        if spawn_timer>=spawn_rate:
            enemies.append(Enemy(level))
            spawn_timer=0
        coin_timer+=1
        if coin_timer>=50:
            coins_list.append(Coin(level))
            coin_timer=0
        for enemy in enemies[:]:
            enemy.update()
            if enemy.rect.top>HEIGHT:
                enemies.remove(enemy)
                score+=10
        for coin in coins_list[:]:
            coin.update()
            if coin.y>HEIGHT:
                coins_list.remove(coin)
        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                player.health-=1
                create_explosion(
                    player.x,
                    player.y
                )
                play_sound(SOUND_CRASH)
                enemies.remove(enemy)
                if player.health<=0:
                    return game_over(
                        score,
                        coins
                    )
        for coin in coins_list[:]:
            if player.rect.colliderect(
                coin.get_rect()
            ):
                coins+=1
                score+=50
                play_sound(SOUND_COIN)
                coins_list.remove(coin)
        update_particles()
        draw_background()
        draw_road()
        for coin in coins_list:
            coin.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()
        draw_particles()
        draw_hud(
            player,
            score,
            coins,
            level
        )
        pygame.display.flip()
selected_car=0
def main():
    while True:
        result=start_menu()
        if result=="quit":
            break
        if result=="start":
            result=game()
            if result=="quit":
                break
            if result=="restart":
                continue
if __name__=="__main__":
    main()
pygame.quit()