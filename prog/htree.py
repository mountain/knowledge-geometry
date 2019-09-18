# -*- coding: utf-8 -*-

from fractions import gcd
from turtle import Turtle, Screen


def drawLable(turtle, numerator, denominator):
    g = gcd(numerator, denominator)
    if denominator != g:
        turtle.write('%d/%d' % (numerator / g, denominator / g), font=("Arial", 8, "bold"))
    else:
        turtle.write('%d' % (numerator / g), font=("Arial", 8, "bold"))


def drawHTree(turtle, order, length, numerator, denominator):

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
        drawLable(turtle, numerator, denominator * 2)
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
        drawLable(turtle, numerator * 2, denominator)
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

drawHTree(yertle, 5, 1536, 0, 1)

screen = Screen()
ts = yertle.getscreen()
ts.getcanvas().postscript(file="labled-htree.eps")

screen.exitonclick()
