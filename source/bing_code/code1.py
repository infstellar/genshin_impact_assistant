import math
import turtle

def draw_circle(x, y, r):
    turtle.penup()
    turtle.goto(x + r, y)
    turtle.pendown()
    turtle.circle(r)

def draw_points(x, y, r):
    n = int(2 * math.pi * r / 5)
    for i in range(n):
        angle = 2 * math.pi / n * i
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        turtle.penup()
        turtle.goto(px, py)
        turtle.pendown()
        turtle.dot(5)

turtle.speed(0)

draw_circle(0, 0, 5)
draw_circle(0, 0, 10)
draw_circle(0, 0, 15)
draw_circle(0, 0, 20)
draw_circle(0, 0, 25)

draw_points(0, 5, 25)
draw_points(0, 10, 20)
draw_points(0, 15, 15)
draw_points(0, 20, 10)
draw_points(0, 25, 5)

turtle.done()