import turtle
import math

def draw_square(t: turtle.Turtle, size: float):
    """Малює квадрат зі стороною size, починаючи з поточної позиції/напрямку."""
    for _ in range(4):
        t.forward(size)
        t.left(90)

def pythagoras_tree(t: turtle.Turtle, size: float, depth: int, angle: float = 45.0):
    """
    Малює дерево Піфагора.
    size  - розмір базового квадрату
    depth - рівень рекурсії
    angle - кут розгалуження (класично 45°)
    """
    if depth == 0 or size <= 1:
        return

    # 1) Малюємо базовий квадрат
    draw_square(t, size)

    # 2) Переходимо на верхню сторону квадрату
    t.forward(size)
    t.left(90)
    t.forward(size)
    t.right(90)

    # Запам'ятаємо позицію/напрямок у точці старту "верхнього" квадрату
    start_pos = t.position()
    start_heading = t.heading()

    # 3) Ліва гілка: квадрат повернутий на +angle
    t.left(angle)
    left_size = size * math.cos(math.radians(angle))
    pythagoras_tree(t, left_size, depth - 1, angle)

    # 4) Повертаємося назад у точку розгалуження
    t.penup()
    t.setposition(start_pos)
    t.setheading(start_heading)
    t.pendown()

    # 5) Права гілка: квадрат повернутий на -(90-angle)
    t.right(90 - angle)
    right_size = size * math.sin(math.radians(angle))
    pythagoras_tree(t, right_size, depth - 1, angle)

    # 6) Повертаємося у початкову точку поточного квадрату (для коректної рекурсії)
    t.penup()
    # Ми стоїмо на верхній стороні; повернемось до нижнього лівого кута поточного квадрату:
    t.setposition(start_pos)
    t.setheading(start_heading)
    t.right(90)
    t.forward(size)
    t.left(90)
    t.backward(size)
    t.pendown()

def main():
    depth = int(input("Введіть рівень рекурсії (наприклад 6..12): ").strip())

    screen = turtle.Screen()
    screen.title("Дерево Піфагора (Pythagoras Tree)")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(1)

    # Стартова позиція
    t.penup()
    t.goto(-80, -250)
    t.setheading(0)
    t.pendown()

    # Базовий квадрат
    pythagoras_tree(t, size=120, depth=depth, angle=45)

    screen.mainloop()

if __name__ == "__main__":
    main()
