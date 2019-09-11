# -*- coding: utf-8 -*-

from turtle import Turtle, Screen


def drawLable(turtle, numerator, denominator):
    turtle.forward(10)
    turtle.write('%d/%d' % (numerator, denominator))
    turtle.backward(10)


def drawHTree(turtle, order, center, length, numerator, denominator):

    if order < 0:
        return

    if center is not None:
        turtle.up()
        turtle.goto(center)
        turtle.down()

    drawLable(turtle, numerator, denominator)

    turtle.forward(length / 2)
    drawLable(turtle, numerator * 2, denominator)
    turtle.right(90)
    turtle.forward(length / 2)
    turtle.left(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator + denominator, denominator)

    turtle.left(90)
    turtle.forward(length)
    turtle.right(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator, denominator)

    turtle.right(90)
    turtle.forward(length / 2)
    turtle.right(90)
    turtle.forward(length)
    turtle.left(90)
    turtle.forward(length / 2)
    turtle.right(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator, denominator)

    turtle.right(90)
    turtle.forward(length)
    turtle.right(90)

    drawHTree(turtle, order - 1, None, length / 2, numerator, denominator)

    turtle.right(90)
    turtle.forward(length / 2)
    turtle.left(90)
    turtle.forward(length / 2)  # always leave the turtle where you found it!

    turtle.hideturtle()


yertle = Turtle()

drawHTree(yertle, 1, (0, 0), 512, 0, 1)

screen = Screen()

screen.exitonclick()
