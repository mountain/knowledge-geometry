# -*- coding: utf-8 -*-

from fractions import gcd
from turtle import Turtle, Screen


def drawLable(turtle, numerator, denominator):
    g = gcd(numerator, denominator)
    if denominator != g:
        turtle.write('%d/%d' % (numerator / g, denominator / g), font=("Arial", 8, "bold"))
    else:
        turtle.write('%d' % (numerator / g), font=("Arial", 8, "bold"))


def drawHTree(turtle, order, center, length, numerator, denominator):

    if order < 0:
        return

    if center is not None:
        turtle.up()
        turtle.goto(center)
        turtle.down()
        turtle.right(90)

    drawLable(turtle, numerator, denominator)

    turtle.forward(length / 2)
    drawLable(turtle, numerator, denominator * 2)
    turtle.right(90)
    turtle.forward(length / 2)
    turtle.left(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator - denominator, denominator)

    turtle.left(90)
    turtle.forward(length)
    turtle.right(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator + denominator, denominator)

    turtle.right(90)
    turtle.forward(length / 2)
    turtle.right(90)
    turtle.forward(length)
    drawLable(turtle, numerator * 2, denominator)
    turtle.left(90)
    turtle.forward(length / 2)
    turtle.right(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator - denominator, denominator)

    turtle.right(90)
    turtle.forward(length)
    turtle.right(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator + denominator, denominator)

    turtle.right(90)
    turtle.forward(length / 2)
    turtle.left(90)
    turtle.forward(length / 2)  # always leave the turtle where you found it!

    turtle.hideturtle()


yertle = Turtle()

drawHTree(yertle, 1, (0, 0), 512, 0, 1)

screen = Screen()

screen.exitonclick()
