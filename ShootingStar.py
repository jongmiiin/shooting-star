#ShootingStar

import random
import pygame # 파이게임 실행을 위한 라이브러리
import sys

from time import sleep # sleep함수 사용
from pygame.locals import *
from datetime import datetime # 현재시간 출력용

WINDOW_WIDTH = 480 # x축 (오른쪽이 값 증가)
WINDOW_HEIGHT = 640 # y축 (아래가 값 증가)

# 컬러
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (250,250,50)
RED = (250,50,50)

FPS = 60 # 1초에 몇 프레임이냐

# 플레이어 구현
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        self.image = pygame.image.load('data/fighter.png') #플레이어 이미지 가져오기
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH / 2) # 처음 플레이어 위치 설정
        self.rect.y = WINDOW_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        #화면 밖으로 나가는 거 방지 (y축 버그 수정)
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx
        
        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

#잡몹 구현
class Mob(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Mob, self).__init__()
        self.image = pygame.image.load('data/mob.png') # 잡몹이미지 가져오기
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos
        self.speed = speed
 
    def update(self):
        if self.rect.y - self.rect.height > WINDOW_HEIGHT:
            self.kill()
         
        self.rect.y += self.speed
        if(self.rect.y % 10 == 0):
            self.rect.x += random.randrange(-10,10)
            
        if  self.rect.x + self.rect.width < 0:
            self.kill()

# 보스 구현
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.image = pygame.image.load('data/boss.png') #보스 이미지 가져오기 
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH - 380) # 처음 위치 설정
        self.rect.y = WINDOW_HEIGHT - 720
        self.dx = 1
        self.dy = 0
    
    # 화면 밖으로 나가는 거 방지
    def update(self): # 보스등장
        self.rect.y += 1
        if self.rect.y > 30:
            self.rect.y = 30
            
 
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

#미사일 구현
class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self). __init__()
        self.image = pygame.image.load('data/missile.png') # 미사일 이미지 구현
        self.rect = self.image.get_rect()
        self.rect.x = xpos -5
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('data/missile.wav') #소리 구현

    def launch(self):
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed  # 미사일 발사

        #화면 밖으로 나가는 거 제거
        if self.rect.y + self.rect.height < 0:
            self.kill()
        
    def collide(self,sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
# 레이저 구현
class Lazer(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Lazer, self). __init__()
        self.image = pygame.image.load('data/lazer.png') # 레이저 이미지 구현 (이미지 좋은 거 좀 써주세요)
        self.rect = self.image.get_rect()
        self.rect.x = xpos-30
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('data/missile.wav') #소리 구현

    def launch(self):
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed  # 레이저 발사

        #화면 밖으로 나가는 거 제거
        if self.rect.y + self.rect.height < 0:
            self.kill()
        
    def collide(self,sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

#보스 공격 구현 (Bossmissile)
class Bossmissile(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Bossmissile, self).__init__()
        self.image = pygame.image.load('data/bossmissile.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        #화면 밖으로 나가는 것 체크 (플레이러 공격 구현에서 응용)
        if self.rect.y - self.rect.height > WINDOW_HEIGHT:
            self.kill()
            
#보스 공격 스킬 (Ball)
class Ball(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Ball, self).__init__()
        self.image = pygame.image.load('data/ball.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos # 위치값
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        #화면 밖으로 나가는 것 체크 (플레이어 공격 구현에서 응용)
        if self.rect.y - self.rect.height > WINDOW_HEIGHT:
            self.kill()
            
#잡몹 공격 구현 (Mobmissile)
class Mobmissile(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Mobmissile, self).__init__()
        self.image = pygame.image.load('data/mobmissile.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos + 20 # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        #화면 밖으로 나가는 것 체크
        if self.rect.y - self.rect.height> WINDOW_HEIGHT:
            self.kill()

# 회복 아이템
class Heal(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Heal, self).__init__()
        
        self.image = pygame.image.load('data/heal.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        #화면 밖으로 나가는 것 체크
        if self.rect.y - self.rect.height > WINDOW_HEIGHT:
            self.kill()

# 보급(레이저) 아이템
class Supply(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Supply, self).__init__()
        
        self.image = pygame.image.load('data/supply.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        #화면 밖으로 나가는 것 체크
        if self.rect.y - self.rect.height > WINDOW_HEIGHT:
            self.kill()

# 배리어 아이템
class Barrier(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Barrier, self).__init__()    
        self.image = pygame.image.load('data/shield.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    #화면 밖으로 나가는 것 체크
    def out_of_screen(self):
       if self.rect.y - self.rect.height > WINDOW_HEIGHT:
            self.kill()
            
# 추가 탄창 아이템
class Ammo(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Ammo, self).__init__()
        
        self.image = pygame.image.load('data/ammo.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    #화면 밖으로 나가는 것 체크
    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True



#글자 출력
def draw_text(text, font, surface, x ,y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

#폭발
def occur_explosion(surface, x ,y):
    explosion_image = pygame.image.load('data/explosion.png')
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sounds = ('data/explosion01.wav','data/explosion02.wav','data/explosion03.wav')
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sound.play()

# 쉴드
def occur_shield(surface, x ,y):
    shield_image = pygame.image.load('data/barrier.png')
    shield_rect = shield_image.get_rect()
    shield_rect.x = x - 15
    shield_rect.y = y - 15
    surface.blit(shield_image, shield_rect)

#반복으로 화면처리, 이벤트처리
def game_loop():
    default_font = pygame.font.Font('data/imagine_font.ttf', 20) # 기본 폰트, 글자 크기
    background_image = pygame.image.load('data/background.png') # 배경이미지
    gameover_sound = pygame.mixer.Sound('data/gameover.wav') # 게임오버 효과음
    pygame.mixer.music.load('data/music.wav') # bgm 가져오기
    pygame.mixer.music.play(-1) # 몇 번 반복할건가 (-1은 무한반복)
    fps_clock = pygame.time.Clock() # 시간
    
    # SET UP LISTS
    mobmissiles = pygame.sprite.Group() # 잡몹 공격
    fighter = Fighter() # 플레이어 
    boss = Boss() # 보스
    missiles = pygame.sprite.Group() # 미사일
    bossmissiles = pygame.sprite.Group() # 보스 공격
    balls = pygame.sprite.Group() # 보스 스킬
    mobs = pygame.sprite.Group() # 잡몹
    heals = pygame.sprite.Group() # 회복 아이템
    lazers = pygame.sprite.Group() # 레이저(스킬) 
    supplys = pygame.sprite.Group() # 레이저 아이템
    barriers = pygame.sprite.Group() # 쉴드 아이템
    ammos = pygame.sprite.Group() # 탄창 아이템
    
    #밸런스 관련
    occur_prob = 45 # 확률적으로 얼만큼 나오게 할 것인가 (낮을수록 보스가 더 자주 공격함)
    shot_count = 0 # 점수
    count_life = 8 # 목숨 
    boss_hp = 500 # 보스 hp
    start_time = datetime.now() # 시작 시간
    missile_count = 40 # 미사일 개수 
    occur_prob_heal = 800 # 아이템 등장 확률 (높을수록 등장 확률 희박)
    occur_prob_supply = 800 # 레이저 아이템 등장 확률
    re_fill = 5 # 재장전 카운트
    lazer_count = 8 # 사용가능 레이저 개수 
    occur_prob_barrier = 750 # 배리어 아이템 등장 확률
    occur_prob_ammos = 700
    shield_time = 0 # 쉴드 횟수
    done = False
    UNTOUCH = False # True면 무적
    
    while not done:
        for event in pygame.event.get():
            # 조작키
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                    fighter.dx -= 5
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                    fighter.dx += 5
                elif event.key == pygame.K_UP or event.key == pygame.K_KP8:
                    fighter.dy -= 5
                elif event.key == pygame.K_DOWN or event.key == pygame.K_KP5:
                    fighter.dy += 5
                elif event.key == pygame.K_SPACE: # 미사일 발사
                    if missile_count > 0: # 미사일이 있으면 발사, 없으면 발사 X
                        missile_count -= 1
                        missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)
                        missile.launch()
                        missiles.add(missile)
                    elif missile_count == 0: # 미사일 재장전
                        if re_fill > 0:
                            missile_count += 40
                            re_fill -= 1
                elif event.key == pygame.K_a: # A를 눌러 레이저 발사 (스킬)
                    if lazer_count > 0:
                        lazer = Lazer(fighter.rect.centerx, fighter.rect.y, 18)
                        lazer_count -= 1
                        lazer.launch()
                        lazers.add(lazer)
                        
                # elif event.key == pygame.K_ESCAPE: # Esc를 누르면 게임 클리어 (마법의 키) 
                #     done = True
                #     pygame.mixer_music.stop()
                #     game_clear(shot_count)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_KP4 or event.key == pygame.K_KP6:
                    fighter.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_KP8 or event.key == pygame.K_KP5:
                    fighter.dy = 0
        
       
        screen.blit(background_image, background_image.get_rect())
        now_time = datetime.now() # 계속 증가하는 시간
        delta_time = 300 + round((start_time - now_time).total_seconds()) # 제한 시간
        # 보스의 체력에 따라 난이도 조절 (체력이 낮을수록 공격 속도 증가)
        occur_of_bossmissile = 2 + int((500-boss_hp) / 500)
        min_bossmissile_speed = 2 + int((500-boss_hp) / 250)
        max_bossmissile_speed = 2 + int((500-boss_hp) / 125)
        occur_of_heals = 1
        occur_of_supplys = 1
        occur_of_barriers = 1
        occur_of_ammos = 1
        
        # 잡몹 생성
        if random.randint(1, 70) == 1:
            for i in range(2):
                speed = 1
                mob = Mob(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                mobs.add(mob)
                speed = 2
                mobmissile = Mobmissile(mob.rect.x-10, mob.rect.y+30, speed)
                mobmissiles.add(mobmissile)
        
        # 보스의 공격
        if shot_count > 2500:
            if random.randint(1, occur_prob) == 1:
                for i in range(occur_of_bossmissile):
                    speed = random.randint(min_bossmissile_speed, max_bossmissile_speed)
                    bossmissile = Bossmissile(random.randint(0, WINDOW_WIDTH - 30), 95, speed)
                    bossmissiles.add(bossmissile)
                
        # 회복 아이템 등장
        if random.randint(1, occur_prob_heal) == 1:
            for i in range(occur_of_heals):
                speed = 2
                heal = Heal(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                heals.add(heal)
                
        # 레이저 아이템
        if random.randint(1, occur_prob_supply) == 1:
            for i in range(occur_of_supplys):
                speed = 2
                supply = Supply(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                supplys.add(supply)
                
        # 배리어 아이템 등장
        if random.randint(1, occur_prob_barrier) == 1:
            for i in range(occur_of_barriers):
                speed = 2
                barrier = Barrier(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                barriers.add(barrier)
                
        # 추가 탄창 아이템 등장
        if random.randint(1, occur_prob_ammos) == 1:
            for i in range(occur_of_ammos):
                speed = 2
                ammo = Ammo(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                ammos.add(ammo)
                
        font_mysize = pygame.font.Font('data/imagine_font.ttf', 20)
                
        # 아이템 갯수 이미지로 표현 
        missile_image = pygame.image.load('data/missile.png')
        missile_image = pygame.transform.scale(missile_image, (15, 30))
        missile_image_x = 10 # 처음 위치 설정
        missile_image_y = 610
        screen.blit(missile_image, (missile_image_x, missile_image_y))
        draw_text('        : {}'.format(missile_count),font_mysize, screen, 35, 630, YELLOW)

        ammo_image = pygame.image.load('data/ammo.png')
        ammo_image = pygame.transform.scale(ammo_image, (30, 30))
        ammo_image_x = 140 # 처음 위치 설정
        ammo_image_y = 610
        screen.blit(ammo_image, (ammo_image_x, ammo_image_y))
        draw_text(': {}'.format(re_fill),font_mysize, screen, 195, 630, YELLOW)

        heal_image = pygame.image.load('data/heal.png')
        heal_image = pygame.transform.scale(heal_image, (30, 30))
        heal_image_x = 295 # 처음 위치 설정
        heal_image_y = 610
        screen.blit(heal_image, (heal_image_x, heal_image_y))
        draw_text(': {}'.format(count_life),font_mysize, screen, 340, 630, RED)

        lazer_image = pygame.image.load('data/lazer.png')
        lazer_image = pygame.transform.scale(lazer_image, (30, 30))
        lazer_image_x = 380 # 처음 위치 설정
        lazer_image_y = 610
        screen.blit(lazer_image, (lazer_image_x, lazer_image_y))
        draw_text('(A): {}'.format(lazer_count),font_mysize, screen, 440, 630, YELLOW)
        
        # 텍스트 표시 (점수, 목숨, 남은 시간, 미사일 수, 보스 체력, 재장전, 레이저 수)
        draw_text('SCORE: {}'.format(shot_count),default_font, screen, 80, 20, YELLOW)
        draw_text('TIME: {}'.format(delta_time),default_font, screen, 400, 20, WHITE)

        
        # 미사일로 잡몹 공격
        for missile in missiles:
            mob = missile.collide(mobs)
            if mob:
                missile.kill()
                mob.kill()
                occur_explosion(screen, missile.rect.x, (missile.rect.y - 30))
                shot_count += 100
                

        #일반공격으로 보스 공격 파괴 - 난이도 조절할때 필요시 사용
        # for missile in missiles:
        #     bossmissile = missile.collide(bossmissiles)
        #     if bossmissile:
        #         missile.kill()
        #         bossmissile.kill()
        #         occur_explosion(screen, bossmissile.rect.x, bossmissile.rect.y)
        #         shot_count += 200

        # 레이저로 잡몹 공격
        for lazer in lazers:
            mob = lazer.collide(mobs)
            if mob:
                mob.kill()
                shot_count += 100
                occur_explosion(screen, mob.rect.x, mob.rect.y)
                
        for lazer in lazers: # 레이저로 보스의 공격을 격추
            bossmissile = lazer.collide(bossmissiles)
            mobmissile = lazer.collide(mobmissiles)
            if bossmissile:
                bossmissile.kill() # 레이저는 관통 공격
                shot_count += 80
                occur_explosion(screen, bossmissile.rect.x, bossmissile.rect.y)
        
            if mobmissile:
                mobmissile.kill()
                shot_count += 80
                occur_explosion(screen, mobmissile.rect.x, mobmissile.rect.y)
        
        UNTOUCH = False # True면 무적
        if shield_time > 0:
            UNTOUCH = True # 쉴드 횟수가 있으면 무적 상태, 배리어 생성
            occur_shield(screen, fighter.rect.x, fighter.rect.y)
            if round((now_time - shield_get_time).total_seconds()) == 3: #쉴드 3초 시간제한
                shield_time = 0
                UNTOUCH = False

        for mobmissile in mobmissiles:
            mobmissile = fighter.collide(mobmissiles) #  공격에 맞았을 때
            if mobmissile and (not UNTOUCH): # 배리어가 없는 상태에서 공격에 맞았을 때
                mobmissile.kill()
                count_life -= 1 # 목숨 - 1
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            elif mobmissile and (UNTOUCH): # 배리어가 있는 상태에서 공격에 맞았을 때
                mobmissile.kill()
                
        for mob in mobs:
            mob = fighter.collide(mobs) #  잡몹에 맞았을 때
            if mob and (not UNTOUCH): # 배리어가 없는 상태에서 공격에 맞았을 때
                mob.kill()
                count_life -= 1 # 목숨 - 1
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            #elif mob and (UNTOUCH): # 배리어가 있는 상태에서 공격에 맞았을 때
                #mob.kill()
                
        # 점수가 일정수준 이상이면 보스 등장    
        if shot_count >= 5000:
            #보스랑 충돌시 게임오버 (목숨이 몇개든 상관없이, 배리어도 상관x)
            if fighter.rect.colliderect(boss.rect):
                pygame.mixer_music.stop()
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                pygame.display.update()
                gameover_sound.play()
                sleep(1) 
                done = True
                game_over(shot_count) 
            draw_text('BOSS HP: {}'.format(boss_hp),default_font, screen, 250, 20, RED)
            bossmissiles.update() # 보스 공격
            bossmissiles.draw(screen)
            boss.update() # 보스
            boss.draw(screen)
            
            if random.randint(1, occur_prob) == 1:
                for i in range(occur_of_bossmissile):
                    speed = random.randint(min_bossmissile_speed, max_bossmissile_speed)
                    bossmissile = Bossmissile(random.randint(0, WINDOW_WIDTH - 30), 95, speed)
                    bossmissiles.add(bossmissile)
                    
            # 보스가 딸피이면 스킬을 사용
            if(boss_hp <= 100):
                # 보스의 스킬
                if random.randint(1, 100) == 1:
                    for i in range(2):
                        ball = Ball(boss.rect.x + 60, boss.rect.y + 40, 3)
                        balls.add(ball)
                balls.update() # 보스 스킬
                balls.draw(screen)
                
                boss.rect.x += boss.dx
                if boss.rect.x + boss.rect.width >= WINDOW_WIDTH:
                    boss.rect.x -= boss.dx
                    boss.dx = -boss.dx
                    boss.rect.x += boss.dx
                if boss.rect.x <= 0:
                    boss.rect.x -= boss.dx
                    boss.dx = -boss.dx
                    boss.rect.x += boss.dx
                
            for missile in missiles:
                missile = boss.collide(missiles) # 미사일로 보스 공격
                if missile:
                    missile.kill()
                    occur_explosion(screen, missile.rect.x, (missile.rect.y - 30))
                    boss_hp -= 1
                    shot_count += 200

            for lazer in lazers: # 레이저로 보스의 공격을 격추
                bossmissile = lazer.collide(bossmissiles)
                if bossmissile:
                    bossmissile.kill() # 레이저는 관통 공격
                    shot_count += 80
                    occur_explosion(screen, bossmissile.rect.x, bossmissile.rect.y)
                
                lazer = boss.collide(lazers) # 레이저로 보스 공격
                if lazer:
                    occur_explosion(screen, lazer.rect.x, lazer.rect.y)
                    boss_hp -= 1
                    shot_count += 200
        
            for bossmissile in bossmissiles:
                bossmissile = fighter.collide(bossmissiles) # 보스 공격에 맞았을 때
                if bossmissile and (not UNTOUCH): # 배리어가 없는 상태에서 공격에 맞았을 때
                    bossmissile.kill()
                    count_life -= 1 # 목숨 - 1
                    occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                elif bossmissile and (UNTOUCH): # 배리어가 있는 상태에서 공격에 맞았을 때
                    bossmissile.kill()
            
            for ball in balls: # 보스의 스킬에 맞았을 때
                ball = fighter.collide(balls)
                if ball and (not UNTOUCH):
                    count_life -= 3 # 보스 스킴이므로 -3
                    occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                elif ball and (UNTOUCH):
                    ball.kill()
                    shield_time -= 1 # 배리어가 있으면 막음
                    if shield_time == 0: # 쉴드 횟수가 0이 되면 배리어 폭발
                        occur_explosion(screen, fighter.rect.x, fighter.rect.y)

                
        for heal in heals: # 회복 아이템 획득
            heal = fighter.collide(heals)
            if heal:
                heal.kill()
                count_life += 1 # 먹으면 목숨 + 1
                                
        for supply in supplys: # 레이저 아이템 획득
            supply = fighter.collide(supplys)
            if supply:
                supply.kill()
                lazer_count += 1 # 먹으면 레이저 + 1

        for barrier in barriers: # 배리어 아이템 획득
            barrier = fighter.collide(barriers)
            if barrier:
                barrier.kill()
                shield_get_time = datetime.now()
                shield_time += 1 # 먹으면 배리어 + 1
                
        for ammo in ammos: #추가 탄창 아이템 획득
            ammo = fighter.collide(ammos)
            if ammo:
                ammo.kill()
                re_fill += 1 #획득시 탄창 + 1
        
        missiles.update() # 미사일
        missiles.draw(screen)
        
        fighter.update() # 플레이어
        fighter.draw(screen)
        
        mobs.update() # 잡몹
        mobs.draw(screen)
        
        mobmissiles.update() # 잡몹 공격
        mobmissiles.draw(screen)
        
        heals.update() # 회복 아이템
        heals.draw(screen)
        
        supplys.update() # 레이저 아이템
        supplys.draw(screen)
        
        lazers.update() # 레이저
        lazers.draw(screen)
        
        barriers.update() # 배리어 아이템
        barriers.draw(screen)
        
        ammos.update()
        ammos.draw(screen)
        
        pygame.display.flip()
        
        # 게임오버 (목숨이 0이 되거나 시간이 100초를 넘기면 종료)
        if count_life <= 0 or delta_time <= 0:
            pygame.mixer_music.stop()
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done = True # while 탈출
            game_over(shot_count)
            
        #보스 hp가 0이 되면 게임 클리어
        if boss_hp <= 0:
            pygame.mixer_music.stop()
            occur_explosion(screen, boss.rect.x, boss.rect.y)
            occur_explosion(screen, boss.rect.x + 20, boss.rect.y + 20)
            occur_explosion(screen, boss.rect.x + 40, boss.rect.y + 40)
            occur_explosion(screen, boss.rect.x + 60, boss.rect.y + 60)
            pygame.display.update()
            sleep(1)
            done = True # while 탈출
            game_clear(shot_count)
       
           
       
        fps_clock.tick(FPS)
        
    return 'game_menu'

# 게임 오버 창
def game_over(shot_count):
    start_image = pygame.image.load('data/background.png')
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_40 = pygame.font.Font('data/imagine_font.ttf', 40)
    draw_text('GAME OVER :(', font_40,screen, draw_x, draw_y + 150, WHITE)
    draw_text('Score: {}'. format(shot_count), font_40,screen, draw_x, draw_y + 200, WHITE)
    pygame.display.update()
    sleep(2)
    return 'game_menu'

# 게임 클리어 창
def game_clear(shot_count):
    start_image = pygame.image.load('data/background.png')
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_40 = pygame.font.Font('data/imagine_font.ttf', 40)
    draw_text('GAME CLEAR :)', font_40,screen, draw_x, draw_y + 150, WHITE)
    font_40 = pygame.font.Font('data/imagine_font.ttf', 30)
    draw_text('Score: {}'. format(shot_count), font_40,screen, draw_x, draw_y + 200, WHITE)
    pygame.display.update()
    sleep(2)
    return 'game_menu'

# 게임 메뉴 창
def game_menu():
    start_image = pygame.image.load('data/background.png')
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_60 = pygame.font.Font('data/imagine_font.ttf', 60)
    font_40 = pygame.font.Font('data/imagine_font.ttf', 40)
    font_20 = pygame.font.Font('data/imagine_font.ttf', 20)

    draw_text('SHOOTING', font_60,screen, draw_x, draw_y, YELLOW)
    draw_text('STAR', font_60,screen, draw_x, draw_y + 80, YELLOW)
    draw_text('Press Enter', font_40,screen, draw_x, draw_y + 200, WHITE)
    draw_text('Game Start', font_40,screen, draw_x, draw_y + 250, WHITE)
    draw_text('Spacebar: Attack    A: Skill ', font_20,screen, draw_x, draw_y + 300, WHITE)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # 엔터를 눌러 게임 시작
                return 'play'
            elif event.key == pygame.K_ESCAPE:   # 그 외의 키를 누르면 게임을 시작하지 않고 종료
                return 'quit'

        if event.type == QUIT:
            return 'quit'


    return 'game_menu'

# 메인 함수
def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('ShootingStar')

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop()
        
        
    pygame.quit()

if __name__ == "__main__":
    main()