import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Collision Detection by @TokyoEdtech")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

shapes = ["wizard.gif", "goblin.gif", "pacman.gif", "cherry.gif", "bar.gif", "ball.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)

class Sprite():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def is_overlapping_collision(self, other):
        return self.x == other.x and self.y == other.y

    def is_distance_collision(self, other):
        distance = (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** 0.5
        return distance < (self.width + other.width) / 2.0

    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return x_collision and y_collision

class Character(Sprite):
    def __init__(self, x, y, width, height, image, jump=False):
        super().__init__(x, y, width, height, image)
        self.jump = jump
        self.y_velocity = 1
        self.gravity = -0.005
        self.energy_loss = 0.95

    def hop(self, distance=300):
        if self.jump:
            self.y += distance
            self.jump = False
            self.y_velocity = 1

    def update_position(self):
        self.y += self.y_velocity
        self.y_velocity += self.gravity
        if self.y < -400:
            self.y_velocity = -self.y_velocity * self.energy_loss
            self.y = -400

class Obstacle(Sprite):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image)
        self.speed = speed

    def move(self):
        self.x -= self.speed

wizard = Character(-128, 200, 128, 128, "wizard.gif")

obstacles = []
for _ in range(5):
    x = random.randint(200, 400)
    y = random.randint(-200, 200)
    speed = random.randint(1, 5) / 10.0
    obstacle = Obstacle(x, y, 64, 64, "goblin.gif", speed)
    obstacles.append(obstacle)

def move_goblin():
    wizard.x -= 64

def move_pacman():
    wizard.x += 30

def jump_pacman(distance=300):
    wizard.hop(distance)

def move_obstacles():
    for obstacle in obstacles:
        obstacle.move()

wn.listen()
wn.onkeypress(move_goblin, "Left")
wn.onkeypress(move_pacman, "Right")
wn.onkeypress(jump_pacman, "space")


while True:

    wizard.update_position()

    move_obstacles()

    for obstacle in obstacles:
        obstacle.render(pen)
    wizard.render(pen)

    for obstacle in obstacles:
        if wizard.is_distance_collision(obstacle):
            wizard.image = "x.gif"

    wn.update()
    pen.clear()
