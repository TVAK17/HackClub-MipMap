import pygame
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

class Body:
    # The Constructor
    def __init__(self, pos, mass, v):
        self.pos = pygame.Vector2(pos)
        self.mass = mass
        self.v = pygame.Vector2(v)
        self.restitution = .94

    # A Method
    def getPos(self):
        return self.pos

    def updatePos(self):
        self.pos.x += self.v.x
        self.pos.y += self.v.y
        self.v *= self.restitution

class Chaser(Body):

    def __init__(self, pos, mass, v, preyList):
        self.pos = pygame.Vector2(pos)
        self.mass = mass
        self.v = pygame.Vector2(v)
        self.preyList = preyList
        self.restitution = .99

xSpeed = 1
ySpeed = 1
# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
bodyList = []
bodyList.append(Body(pygame.Vector2(0, 400), 10, pygame.Vector2(0,0)))
chaserList = []
chaserList.append(Chaser(pygame.Vector2(200, 400), 10, pygame.Vector2(0,0), bodyList))
generationData = []
accumulated_df = pd.DataFrame(generationData)
for i in range(1,10):
    chaserList.append(Chaser(pygame.Vector2(random.randrange(0,400,1), random.randrange(0,400,1)), 10, pygame.Vector2(0,0), bodyList))
# Create a simple window (Width: 800, Height: 600)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame Window")
# Game Loop
frames = 0
running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    
    for body in bodyList:

        if keys[pygame.K_LEFT]:
            body.v.x -= xSpeed
        if keys[pygame.K_RIGHT]:
            body.v.x += xSpeed
        if keys[pygame.K_DOWN]:
            body.v.y += ySpeed
        if keys[pygame.K_UP]:
            body.v.y -= ySpeed

        if body.pos.x < 0:
            body.pos.x = 800
        elif body.pos.x > 800:
            body.pos.x = 0
        if body.pos.y < 0:
            body.pos.y = 600
        elif body.pos.y > 600:
            body.pos.y = 0
#        body.v.x += random.random()
#        body.v.y += random.random()
        body.updatePos()
        pygame.draw.circle(screen, (255, 0, 0), body.pos, 10, 0)


    for chaser in chaserList:
        if (chaser.pos.x < chaser.preyList[0].pos.x):
            chaser.v.x += xSpeed / random.randrange(3,15,1)
        elif (chaser.pos.x > chaser.preyList[0].pos.x):
            chaser.v.x -= xSpeed / random.randrange(3,15,1)
        if (chaser.pos.y < chaser.preyList[0].pos.y):
            chaser.v.y += ySpeed / random.randrange(3,15,1)
        elif (chaser.pos.y > chaser.preyList[0].pos.y):
            chaser.v.y -= ySpeed / random.randrange(3,15,1)

        if chaser.pos.x < 0:
            chaser.pos.x = 800
        elif chaser.pos.x > 800:
            chaser.pos.x = 0
        if chaser.pos.y < 0:
            chaser.pos.y = 600
        elif chaser.pos.y > 600:
            chaser.pos.y = 0

        chaser.updatePos()
        pygame.draw.circle(screen, (0, 0, 255), chaser.pos, 10, 0)


    frame_entry = {
        'bodyPos': bodyList[0].pos, 
        'bodyV': bodyList[0].v
    }

    for i, chaser in enumerate(chaserList):
        frame_entry[f'chaser_{i}_pos'] = chaser.pos
        frame_entry[f'chaser_{i}_v'] = chaser.v

    generationData.append(frame_entry)

    # ML start (not working)
    if (frames % 120 == 0):
        accumulated_df = pd.DataFrame(generationData)
        X = accumulated_df.drop(columns=['bodyV'])
        y = accumulated_df[['v']]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f'Frame Group {frames}: Cumulative Mean Squared Error: {mse:.4f}')

    
    pygame.display.flip()
    """
    for body in bodyList:
        print("Body:", body.pos)
    for chaser in chaserList:
        print("Chaser:", chaser.pos)
    """
    frames += 1
    clock.tick(60)
    

pygame.quit()