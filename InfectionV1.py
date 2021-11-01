#Imports
import random
import pygame
import math
from math import atan2, degrees, pi
#Create the particles
class Particle(pygame.sprite.Sprite):
    #for when it initilizes
    def __init__(self, hue, pos, radius, dir, vel, ZTF):
        super().__init__()
        #Setting the x & y coords
        self.pos = pygame.math.Vector2(pos)
        #Setting the starting angle
        self.dir = pygame.math.Vector2(dir)
        #Setting the starting velocity
        self.vel = vel
        #Setting the particle size
        self.radius = radius
        #Making the hitbox (I think)
        self.rect = pygame.Rect(round(self.pos.x - radius), round(self.pos.y - radius), radius*2, radius*2)
        #Setting the image
        self.image = pygame.Surface((radius*2, radius*2))
        #Setting the Hue
        if (ZTF == True):
            #If Zombie, then set red
            hue = 350
            self.changeColor(hue)
        else:
            #if not zombie, set green
            hue = 90
        #Draw the sprite & stuff
        self.hue = hue
        color = pygame.Color(0)
        color.hsla = (self.hue, 100, 50, 100)
        self.image.set_colorkey((0, 0, 0))
        self.image.fill(0)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
    #used to change the color of sprite after "Infection" (collision with red particle)
    def changeColor(self, hue):
            #Change the hue to red
            hue = 350
            self.hue = hue
            color = pygame.Color(0)
            color.hsla = (self.hue, 100, 50, 100)
            self.image.set_colorkey((0, 0, 0))
            self.image.fill(0)
            #reset the sprite so it is now displayed as red
            pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
    #used to "chase" after the nearest green particle
    def chase(self):
        #gets current position
        #sets pos to current position
        pos = self.pos
        #used to determine if first iteration
        z =0
        #loop through all particles
        q=0
        for e in all_particles:
            #if not a zombie, then tempP = e
            if (e.hue == 90):
                q+=1
                #if the first loop, set enemy to e
                if (z==0):
                    enemy = e
                    z+=1
                #if not the first loop
                else:
                    #If the distance to the newest sprite selected is less than the stored value, set the newsest sprite as the stored value
                    if (pos.distance_to(pygame.math.Vector2(e.pos.x, e.pos.y)) < pos.distance_to(pygame.math.Vector2(enemy.pos.x, enemy.pos.y))):
                        enemy = e
        #sets up list of particles
        particle_list = all_particles.sprites()
        if q !=0:
            #determining the difference between the two points for x & y
            difx = enemy.pos.x - self.pos.x 
            dify = enemy.pos.y - self.pos.y 
            #determining radians from the difference of two points for x & y
            rads = atan2(dify,difx)
            #converting to integer version in degrees
            rads %=2*pi
            defg = degrees(rads)
            #setting dir to the determined degrees
            self.dir = pygame.math.Vector2(1, 0).rotate((defg))
            #for all the particles in the list
    #Used to move in current direction 
    def move(self):
        #move position based on velocity and angle
        self.pos += self.dir * self.vel
    #Used to set ZTF to true because for some reason I get an error if I just try and do particle_1.ZTF = True
    def ToZ():
        ZTF = True
    #used to change the angle of movement in the event of a collision with the border
    def update(self, border_rect):
        if self.pos.x - self.radius < border_rect.left:
            self.pos.x = border_rect.left + self.radius
            self.dir.x = abs(self.dir.x)
        elif self.pos.x + self.radius > border_rect.right:
            self.pos.x = border_rect.right - self.radius
            self.dir.x = -abs(self.dir.x)
        if self.pos.y - self.radius < border_rect.top:
            self.pos.y = border_rect.top + self.radius
            self.dir.y = abs(self.dir.y)
        elif self.pos.y + self.radius > border_rect.bottom:
            self.pos.y = border_rect.bottom - self.radius
            self.dir.y = -abs(self.dir.y) 
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))
#initilize pygame
pygame.init()
#draw the window 800pix by 800
window = pygame.display.set_mode((800, 800))
#begin the clock
clock = pygame.time.Clock()
#draw the rectangle bounds
rect_area = window.get_rect().inflate(-40, -40)
#setup the particle group
all_particles = pygame.sprite.Group()
#setting radius and velocity for sprites
radius, velocity = 5, 1
#setting up pos_rect
pos_rect = rect_area.inflate(-radius * 2, -radius * 2)
#create hue
hue = 90
#starting the loop
run = True

#spawn in the particles
p =0
#loop which runs while there are below x num of particles
while p <100:
    #random coords for spawning, and random angle for movement
    x = random.randrange(pos_rect.left, pos_rect.right)
    y = random.randrange(pos_rect.top, pos_rect.bottom)
    dir = pygame.math.Vector2(1, 0).rotate(random.randrange(360))
    
    if p == 99:
        #defines last particle as zombie
        ZTF = True
        particle = Particle(350, (x, y), radius, dir, velocity, ZTF)
    else:
        #defines all others as regular
        ZTF = False
        particle = Particle(90, (x, y), radius, dir, velocity, ZTF)
    #makes sure that the particle does not spawn on top of any other particles
    if not pygame.sprite.spritecollide(particle, all_particles, False, collided = pygame.sprite.collide_circle):
        p +=1
        all_particles.add(particle) # spawns the particle
#main loop, runs stuff
while run:
    #clock speed
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #Moves all the particles, and calls chase if it is a zombie
    for particle in all_particles:
        if particle.hue == 350:
            particle.chase()
        particle.move()
    #sets list of all sprites
    particle_list = all_particles.sprites()
    #Checks for collisions with nested loop
    for i, particle_1 in enumerate(particle_list):
        for particle_2 in particle_list[i:]:
            #math to see if anything collides
            distance_vec = particle_1.pos - particle_2.pos
            #if they do collide, then make them bounce off eachother
            if 0 < distance_vec.length_squared() < (particle_1.radius + particle_2.radius) ** 2:
                distanceBetween = particle_1.pos.distance_to(pygame.math.Vector2(particle_2.pos.x, particle_2.pos.y))
                #setup the combined hitbox size
                combinedHitbox = particle_1.radius + particle_2.radius
                #if they're overlapping, set them apart
                if combinedHitbox > distanceBetween:
                    # Calculate the delta position (difference between)
                    positionDiff = particle_2.pos - particle_1.pos
                    # Move them away from each other half of the distance between them.
                    particle_2.pos += positionDiff /2
                    particle_1.pos -= positionDiff /2
                particle_1.dir.reflect_ip(distance_vec)
                particle_2.dir.reflect_ip(distance_vec)
                # if one is a zombie and the other is not, make the
                if (particle_1.hue == 90 and particle_2.hue == 350):
                    particle_1.ToZ
                    particle.vel = 1
                    particle_1.changeColor(hue)
                elif (particle_1.hue == 350 and particle_2.hue == 90):
                    particle_2.ToZ
                    particle_2.changeColor(hue)
                break
    #Update all the particles, draw the window, and the bounds
    all_particles.update(rect_area)
    window.fill(0)
    pygame.draw.rect(window, (255, 0, 0), rect_area, 3)
    all_particles.draw(window)
    pygame.display.flip()

pygame.quit()
exit()
