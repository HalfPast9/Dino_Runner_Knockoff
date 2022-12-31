import pygame as pg
from sys import exit
import random as r

def display_score():
    score = (pg.time.get_ticks() - start_time) // 50
    score_surf = font.render(f"Score: {score}", True, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)

    return score

def obs_movement(obs_lst):
    if obs_lst:
        for obs_rect in obs_lst:
            obs_rect.left -=5

            if obs_rect.top == 270:
                screen.blit(goomba_surf, obs_rect)
            
            else:
                screen.blit(ghost_surf, obs_rect)
        
        obs_lst = [obs for obs in obs_lst if obs.x > -100]
        
        return obs_lst
    else:
        return []

def collision(player, obs):
    if obs:
        for obs_rect in obs:
            if player.colliderect(obs_rect):
                return False
    
    return True

pg.init()
screen = pg.display.set_mode((800,400))
pg.display.set_caption("Mario Knockoff")
clock = pg.time.Clock()
font = pg.font.Font("amazing.ttf", 50)
end_font = pg.font.Font("amazing.ttf", 30)
game_active = False
start_time = 0
score = 0

sky_surf = pg.image.load("sky.png").convert()
ground_surf = pg.image.load("ground.png").convert()

goomba_surf = pg.transform.scale(pg.image.load("goomba.png").convert_alpha(), (70,70))
ghost_surf = pg.transform.scale(pg.image.load("ghost.png").convert_alpha(), (70,70))

obs_rect_lst = []

player_surf = pg.transform.scale(pg.image.load("slime.png").convert_alpha(), (70,60))
player_rect = player_surf.get_rect(topleft = (80,260))
player_grav = 0

player_stand = pg.transform.scale(pg.image.load("slime.png").convert_alpha(), (140,120))
player_stand_rect = player_stand.get_rect(center = (400,200))

title = font.render("Dino Runner Knockoff", True, (8, 150, 8))
title_rect = title.get_rect(center = (400, 300))

start_condition = end_font.render("Press Space to start", True, (9, 88, 9))
start_rect = title.get_rect(center = (550, 380))

obs_time = pg.USEREVENT + 1
pg.time.set_timer(obs_time, 1400)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if game_active:    
            if event.type == pg.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.top == 260:
                        player_grav = -20

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                        if player_rect.top == 260:
                            player_grav = -20
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game_active = True
                    start_time = pg.time.get_ticks()

        if event.type == obs_time and game_active:
            if r.randint(0,2):
                obs_rect_lst.append(goomba_surf.get_rect(topleft = (r.randint(900, 1100), 270)))
            else:
                obs_rect_lst.append(ghost_surf.get_rect(topleft = (r.randint(900, 1100), 175)))

    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,320))

        score = display_score()
        
        player_rect.top += player_grav
        screen.blit(player_surf, player_rect)

        if player_rect.top >= 260:
            player_grav = 0
        else:
            player_grav += 1

        obs_rect_lst = obs_movement(obs_rect_lst)

        game_active = collision(player_rect, obs_rect_lst)



    else:
        screen.fill((132,210,132))
        screen.blit(player_stand, player_stand_rect)

        
        screen.blit(title, title_rect)
        screen.blit(start_condition, start_rect)

        obs_rect_lst.clear()
        
        if score != 0:
            score_msg = end_font.render(f"Your score: {score}", True, (9, 88, 9))
            score_msg_rect = score_msg.get_rect(center = (400, 50))
            screen.blit(score_msg, score_msg_rect)


    pg.display.update()
    clock.tick(60)
