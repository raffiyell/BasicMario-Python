##You can use your own images inside the view class.
import pygame
import random
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, m, x, y, w, h, type):
		#print("created Sprite"+" Type=", type)
		#print(" type= ", type)
		self.x=x
		self.h=h
		self.w=w
		self.y=y
		self.beforeX=0
		self.beforeY=0
		self.model=m
		self.type=type
		self.accelerate=0
		self.timeInAir=0
		self.jumpOnce=None
		self.addCoin=None
		self.coinsLeft=5
		self.rand1=random.randint(0, 20)
	def marioUpdate(self):
		#print(self.y, self.x)
		if self.y>=550:
			self.y=550
			self.accelerate=0
			self.timeInAir=0
			self.jumpOnce=True
		else:
			self.accelerate+=2
			self.y+=self.accelerate
		self.timeInAir+=1
		self.collision()
	def collision(self):	
		for i in range(len(self.model.sprites)):
			self.b=self.model.sprites[i]
			
			if self.b.type==2 or self.b.type==3 or self.b.type==4:
			
				if self.model.mario.x< self.b.x + self.b.w and self.model.mario.x +self.model.mario.w > self.b.x and self.model.mario.y < self.b.y + self.b.h and self.model.mario.y + self.model.mario.h > self.b.y:
					print("collision")
		
					if self.model.mario.x < self.b.x + self.b.w and self.model.mario.beforeX >= self.b.x + self.b.w:
						self.model.mario.x=self.b.x+self.b.w
						print("hitting right side")
					elif self.model.mario.x+self.model.mario.w > self.b.x  and  self.model.mario.beforeX +self.model.mario.w <= self.b.x:
						self.model.mario.x=self.b.x-self.model.mario.w;
						print("Hitting left Side")
					elif self.model.mario.y < self.b.y + self.b.h  and  self.model.mario.beforeY > self.b.y + self.b.h:
						print("bottom")
						self.jumpOnce=False
						self.model.mario.y= self.b.y+self.b.h+2
						self.model.mario.accelerate=10
						if self.b.coinsLeft==0:					#<--------if there's no coin left, disable a
							self.b.addCoin=False
						elif self.model.mario.timeInAir>1:
							self.b.addCoin=True					#<---------if there are still coins left, coinblock update will
							self.b.coinsLeft-=1				#		  call addcoin from model. Also coinsLeft will decrement
					elif self.model.mario.y+ self.model.mario.h > self.b.y and self.model.mario.beforeY  + self.model.mario.h <= self.b.y:
						print("hitting top s ide", self.b.x,self.b.y, self.b.w, self.b.h)
						self.jumpOnce=True
						self.model.mario.accelerate=0
						self.model.mario.y= self.b.y-self.model.mario.h 
						self.model.mario.accelerate=0
						self.timeInAir=0
				
	def beforePos(self):
		self.beforeX=self.model.mario.x
		self.beforeY=self.model.mario.y
	def brickUpdate(self):
		#print("brickUpdate")
		pass
	def coinblockUpdate(self):
		#print("coinblockUpdate")
		if self.addCoin==True:
			self.model.coin=Sprite(self.model, self.x,self.y,self.w,self.h,4)
			self.model.sprites.append(self.model.coin)
			self.addCoin=False
	def coinUpdate(self):
		self.y=self.y-25;					
		self.accelerate+=2;			
		self.y+=self.accelerate
		if self.y>5000:
			self.y=5000
		if self.rand1%2==0:
			self.x+=self.rand1
		else:
			self.x-=self.rand1
	def update(self):
		if self.type == 1:
			self.marioUpdate()
		elif self.type == 2:
			self.brickUpdate()
		elif self.type == 3:
			self.coinblockUpdate()
		elif self.type == 4:
			self.coinUpdate()
	#	print(self.addCoin)	
	#	self.rect.top 	= self.y
	#	self.rect.left 	= self.x
	def moveMario(self, dx, dy):
		self.x+=dx
		self.y+=dy
class Model():
	def __init__(self):
		print("created model")
		self.sprites= []
		self.mario= Sprite( self, 0, 0, 61, 95, 1)					#last parameter is Sprite Type: 1=mario,2=bricks,3=coinblocks,4=coin
		self.sprites.append(self.mario)
		self.scrollPos=0
		self.brick1=Sprite(self, 350, 500, 145, 146, 2)
		self.brick2=Sprite(self, 900, 330, 145, 146, 2)
		self.brick3=Sprite(self, 600, 270, 145, 146, 2)
		self.coinblock1=Sprite(self, 100, 400, 89, 83, 3)
		self.coinblock2=Sprite(self, 400, 100, 89, 83, 3)
		self.coinblock3=Sprite(self, 770, 300, 89, 83, 3)
		self.coinblock4=Sprite(self, 1070, 300, 89, 83, 3)
		self.sprites.append(self.brick1)
		self.sprites.append(self.brick2)
		self.sprites.append(self.brick3)
		self.sprites.append(self.coinblock1)
		self.sprites.append(self.coinblock2)
		self.sprites.append(self.coinblock3)
		self.sprites.append(self.coinblock4)
	
	def update(self):
		for i in range(len(self.sprites)):
			self.sprites[i].update()
			#print(self.sprites[i].x,self.sprites[i].y, self.sprites[i].w, self.sprites[i].h)
		self.scrollPos=self.mario.x
	def move(self, dx, dy):
		self.mario.moveMario(dx, dy)

class View():
	def __init__(self, model):
		print("created View")
		screen_size = (1000,800)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.marioImage = pygame.image.load("mario1.png")
		self.marioImage2 = pygame.image.load("mario2.png")
		self.marioImage3 = pygame.image.load("mario3.png")
		self.marioImage4 = pygame.image.load("mario4.png")
		self.marioImage5 = pygame.image.load("mario5.png")
		self.brickImage= pygame.image.load("brick.png")
		self.wallpaper=pygame.image.load("wallpaper.png")
		self.coinblockImage=  pygame.image.load("block2.png")
		self.coinblockImage2=  pygame.image.load("block1.png")
		self.coinImage= pygame.image.load("coin.png")
		self.brickRoad=pygame.image.load("brickroad.png")
		self.model = model
		
	def update(self):    
		self.screen.fill([0,200,100])
		for i in range(len(self.model.sprites)):

		#	self.screen.blit(self.brickRoad, (0,550))
			self.sprite=self.model.sprites[i]
			if self.sprite.type==1:					#<--- 1 means mario 
				count= abs(self.model.mario.x%4)
				if count==0:
					self.screen.blit(self.marioImage, (self.model.mario.x-self.model.scrollPos+200,self.model.mario.y))
				elif count==1:
					self.screen.blit(self.marioImage2, (self.model.mario.x-self.model.scrollPos+200,self.model.mario.y))
				elif count==2:
					self.screen.blit(self.marioImage3, (self.model.mario.x-self.model.scrollPos+200,self.model.mario.y))
				elif count==3:
					self.screen.blit(self.marioImage4, (self.model.mario.x-self.model.scrollPos+200,self.model.mario.y))
				elif count==4:
					self.screen.blit(self.marioImage5, (self.model.mario.x-self.model.scrollPos+200,self.model.mario.y))
			elif self.sprite.type==2:	
				self.screen.blit(self.brickImage, (self.sprite.x-self.model.scrollPos+200,self.sprite.y))
			elif self.sprite.type==3:
				if self.sprite.coinsLeft<=0:
					self.screen.blit(self.coinblockImage, (self.sprite.x-self.model.scrollPos+200,self.sprite.y))
				else:
					self.screen.blit(self.coinblockImage2, (self.sprite.x-self.model.scrollPos+200,self.sprite.y))
			elif self.sprite.type==4:
				self.screen.blit(self.coinImage, (self.sprite.x-self.model.scrollPos+200,self.sprite.y))
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		print("created Controller")
		self.model = model
		self.keep_going = True
		
	def update(self):
		self.dx=0
		self.dy=0
		self.model.mario.beforePos()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.dx -= 10
		if keys[K_RIGHT]:
			self.dx += 10
		if keys[K_SPACE]==True and self.model.mario.jumpOnce==True and self.model.mario.timeInAir<10:
			self.dy -= 50
		self.model.move(self.dx, self.dy)

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")