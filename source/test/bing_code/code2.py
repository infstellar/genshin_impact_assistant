import math
import turtle

# turtle.speed(0)
# x,y=(50,50)
# points = []
# rate = 1
# for r in range(5*rate, 30*rate, 5*rate):
#     n = int(2 * math.pi * r / 15)
#     for i in range(n):
#         angle = 2 * math.pi / n * i
#         px = x + r * math.cos(angle)
#         py = y + r * math.sin(angle)
#         turtle.penup()
#         turtle.goto(px, py)
#         turtle.pendown()
#         turtle.dot(5)
#         points.append((px, py))
# turtle.done()

def get_circle_points(x,y, show_res = False):
    points = []
    for r in range(5, 30, 5):
        n = int(2 * math.pi * r / 15)
        for i in range(n):
            angle = 2 * math.pi / n * i
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            if show_res:
                turtle.penup()
                turtle.goto(px, py)
                turtle.pendown()
                turtle.dot(5)
            points.append((px, py))
    return points

print(get_circle_points(50,50))

