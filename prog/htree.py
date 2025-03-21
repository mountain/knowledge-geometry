# -*- coding: utf-8 -*-

import turtle

from fractions import gcd
from turtle import Turtle, Screen


def drawLable(turtle, numerator, denominator, step=5):
    g = gcd(numerator, denominator)
    turtle.penup()
    turtle.right(90)
    turtle.forward(step)
    turtle.right(90)
    turtle.forward(step)
    if denominator != g:
        turtle.write('%d/%d' % (numerator / g, denominator / g), font=("Arial", 8, "bold"))
    else:
        turtle.write('%d' % (numerator / g), font=("Arial", 8, "bold"))
    turtle.backward(step)
    turtle.left(90)
    turtle.backward(step)
    turtle.left(90)
    turtle.pendown()


def drawHTree(turtle, order, length, numerator, denominator, shiftx=0, shifty=0):
    if order < 0:
        drawLable(turtle, numerator, denominator)
    else:
        turtle.forward(length / 2)
        turtle.right(90)
        turtle.forward(length / 2)
        turtle.left(90)
        drawHTree(turtle, order - 1, length / 2, numerator - denominator * 2, denominator * 2)
        turtle.left(90)
        turtle.forward(length / 2)
        drawLable(turtle, numerator, denominator * 2, step=10)
        turtle.forward(length / 2)
        turtle.right(90)
        drawHTree(turtle, order - 1, length / 2, numerator + denominator * 2, denominator * 2)
        turtle.right(90)
        turtle.forward(length / 2)
        turtle.right(90)
        turtle.forward(length / 2)
        drawLable(turtle, numerator, denominator)
        turtle.forward(length / 2)
        turtle.right(90)
        turtle.forward(length / 2)
        turtle.right(90)
        drawHTree(turtle, order - 1, length / 2, numerator * 2 + denominator, denominator)
        turtle.right(90)
        turtle.forward(length / 2)
        drawLable(turtle, numerator * 2, denominator, step=0)
        turtle.forward(length / 2)
        turtle.left(90)
        drawHTree(turtle, order - 1, length / 2, numerator * 2 - denominator, denominator)
        turtle.left(90)
        turtle.forward(length / 2)
        turtle.right(90)
        turtle.forward(length / 2)

    turtle.hideturtle()


yertle = Turtle()

yertle.goto(0, 0)
yertle.right(90)

drawHTree(yertle, 2, 256, 0, 1)

turtle._CFG['width'] = 0.5
turtle._CFG['height'] = 0.75
turtle._CFG['canvwidth'] = 800
turtle._CFG['canvheight'] = 800

screen = Screen()
ts = yertle.getscreen()
ts.getcanvas().postscript(file="../images/labled-htree.eps")

screen.exitonclick()
