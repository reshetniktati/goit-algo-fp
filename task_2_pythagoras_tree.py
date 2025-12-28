import turtle
from math import cos, sin, radians

def pythagoras_tree(x, y, size, angle, level, pen: turtle.Turtle):
    """
    Малює 'дерево Піфагора' рекурсивно:
    - на кожному кроці малюємо квадрат
    - з верхньої сторони квадрата будуємо 2 нові квадрати під кутами
    """

    if level == 0 or size < 2:
        return

    # Розраховуємо 4 вершини квадрата (починаємо з точки (x, y))
    a = (x, y)
    b = (x + size * cos(radians(angle)), y + size * sin(radians(angle)))
    c = (b[0] + size * cos(radians(angle + 90)), b[1] + size * sin(radians(angle + 90)))
    d = (a[0] + size * cos(radians(angle + 90)), a[1] + size * sin(radians(angle + 90)))

    # Малюємо квадрат
    pen.up()
    pen.goto(a)
    pen.down()
    pen.goto(b)
    pen.goto(c)
    pen.goto(d)
    pen.goto(a)

    # Дві нові "гілки" з верхньої сторони (між d і c)
    # Класичний варіант
    left_scale = 0.7
    right_scale = 0.7

    # Ліва гілка стартує з точки d
    pythagoras_tree(
        d[0], d[1],
        size * left_scale,
        angle + 45,
        level - 1,
        pen
    )

    # Права гілка стартує з точки c
    pythagoras_tree(
        c[0], c[1],
        size * right_scale,
        angle - 45,
        level - 1,
        pen
    )

def main():
    try:
        level = int(input("Введи рівень рекурсії (наприклад 8-12): ").strip())
    except ValueError:
        print("Будь ласка, введи ціле число.")
        return

    screen = turtle.Screen()
    screen.title("Фрактал: Дерево Піфагора (рекурсія)")
    screen.setup(width=1000, height=800)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)  # максимально швидко
    pen.pensize(1)

    # Стартові параметри
    start_x, start_y = -50, -250
    start_size = 120
    start_angle = 0

    pythagoras_tree(start_x, start_y, start_size, start_angle, level, pen)

    turtle.done()

if __name__ == "__main__":
    main()
