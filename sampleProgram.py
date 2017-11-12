import pygame as pg
from CD_classes_and_functions import *
from random import random
from numpy import sqrt

# Green is a very creative color: "0fc007"

# Pygame initiation
pg.init()
pg.font.init()
screen = pg.display.set_mode((1200, 700), pg.RESIZABLE)

# Logo and Title
logo=pg.image.load("C-D_logo.png")
pg.display.set_icon(logo)
pg.display.set_caption("CYB3R-D3F3NS3")

# Initialization Stuff
done = False
inProgress = True
clock = pg.time.Clock()

title_font=pg.font.SysFont('couriernew', 36, bold=True)
title_font.set_underline(True)
title= title_font.render("CYB3R-D3F3NS3", True, (15, 192, 7))
price = 0

my_font=pg.font.SysFont('couriernew', 24)

map=pg.image.load("better-map.png")
scaled_map, x, y, w, h =scale_and_new_coords(map)
enemy_size=int(0.06*h)
screen.fill((0, 0, 0))

enemies=[]
spawnrate=150

player=Stats()
health, gold = player.display(my_font)

all_slots=[]
slot_data=[(0.26, 0.02), ( 0.47, 0.02), (0.21, 0.31), (0.47,0.31), 
(0.3, 0.59), (0.61, 0.59), (0.25, 0.86), (0.56, 0.86)]
purchase_position=(0.77, 0.3)
purchase_size=(0.2, 0.08)
visible_purchase=-1
for data in slot_data:
	slot=Slots(data, purchase_position, (0.1, 0.1), purchase_size)
	all_slots.append(slot)

	
# Heart of the game
while not done:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			done = True
		if event.type == pg.MOUSEBUTTONDOWN and (pg.mouse.get_pressed())[0] and inProgress:
			cursor_position=pg.mouse.get_pos()
			what_was_pressed=0
			if (in_range(x, y, w, h, purchase_position, purchase_size, cursor_position) 
			and (visible_purchase !=-1)):
				what_was_pressed=1
			else:
				count=0
				for slot in all_slots:
					success=slot.tower_is_pressed(x, y, w, h, cursor_position)
					if success:
						what_was_pressed=2
						break
					count+=1
			for slot in all_slots:
				slot.buy.visible=0
				slot.upgrade.visible=0
				price=0
			if what_was_pressed==1:
				(all_slots[visible_purchase]).purchase(player)
				player.display(my_font)
			elif what_was_pressed==2:
				if all_slots[count].enter_shop():
					visible_purchase=count
					price=my_font.render("Costs "+("30" if all_slots[count].tower1.visible else "15")+" gold.", True, (15, 192, 7))
			
		if event.type == pg.VIDEORESIZE:
			new_size= event.size
			screen=pg.display.set_mode((new_size), pg.RESIZABLE)
			scaled_map, x, y, w, h =scale_and_new_coords(map)
			enemy_size=int(0.06*h)
	
	if not inProgress:
		continue
	
	screen.blit(scaled_map, (x,y))
	screen.blit(health, ((0.77*w)+x,(0.15*h)+y))
	screen.blit(gold, ((0.77*w)+x,(0.225*h)+y))
	screen.blit(title, ((0.705*w)+x,(0.05*h)+y))
	if price:
		screen.blit(price, ((0.77*w)+x,(0.42*h)+y))
	
	
	for slot in all_slots:
		if not slot.empty.visible:
			if not slot.cooldown:
				#Math to find closest mob
				if enemies:
					distance=[]
					for manny in enemies:
						distance.append((((slot.empty.x-manny.x)*(9/16))**2+(slot.empty.y-manny.y)**2)**(1/2))
					if min(distance) < (0.4 if slot.tower2.visible else 0.25):
						slot.enemy=enemies[distance.index(min(distance))]
					slot.firing_time = 30
					width=5
				if slot.tower1.visible:
					slot.cooldown=150
				else:
					slot.cooldown=90
			elif slot.firing_time>1:
				if slot.enemy:
					pg.draw.line(screen, (  255,   255, 255)
					, ((slot.empty.x+0.03)*w+x, (slot.empty.y+0.05)*h+y)
					, ((slot.enemy.x+0.03)*w+x, (slot.enemy.y+0.03)*h+y), width) 
				slot.firing_time-=1
				if width<(15 if slot.tower2.visible else 5):
					width+=1
				else:
					width=(6 if slot.tower2.visible else 1)
			elif slot.firing_time==1:
				slot.firing_time =0
				if slot.enemy in enemies:
					enemies.remove(slot.enemy)
				slot.enemy=0
				player.g+=1
				health, gold = player.display(my_font)
				if spawnrate>2:
					if random()>(0.75-(2/spawnrate)+(player.hp/400)):
						spawnrate-=1
			else:
				slot.cooldown -= 1
	
	num=int(random()*spawnrate)
	if num<2:
		if num: position=(0.36, -0.08)
		else: position=(-0.08, 0.12)
		new_enemy=Enemy(position, (200, 0, 0))
		enemies.append(new_enemy)
		cooldown=30
	
	for manny in enemies:
		dead = manny.move()
		if dead:
			enemies.remove(manny)
			player.hp-=1
			health, gold = player.display(my_font)
			if not player.hp:
				inProgress=False
		manny.display(screen, x, y, w, h, enemy_size)
		
	for slot in all_slots:
		slot.display(screen, x, y, w, h)
		
	if x:
		pg.draw.rect(screen, (0,0,0),(0, 0, x, h))
		pg.draw.rect(screen, (0,0,0),(w+x, 0, w+2*x, h))
	elif y:
		pg.draw.rect(screen, (0,0,0),(0, 0, w, y))
		pg.draw.rect(screen, (0,0,0),(0, h+y, w, h+2*y))
	
	pg.display.flip()
	clock.tick(60)