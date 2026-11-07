
"""Игра «Изгиб Питона»."""

from random import choice

import pygame

# Размеры игрового поля.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость игры.
SPEED = 20

# Центральная позиция поля.
CENTER_POSITION = (
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2,
)

DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# Все возможные позиции на игровом поле.
ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

# Настройка игрового окна.
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self):
        """Задать начальную позицию и цвет."""
        self.position = CENTER_POSITION
        self.body_color = None

    def draw(self):
        """Метод отрисовки для переопределения."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Создать яблоко."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self, occupied=None):
        """Выбрать случайную свободную позицию."""
        if occupied is None:
            occupied = {CENTER_POSITION}

        free_cells = ALL_CELLS - set(occupied)

        if free_cells:
            self.position = choice(tuple(free_cells))
        else:
            self.position = None

    def draw(self):
        """Нарисовать яблоко."""
        if self.position is None:
            return

        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Создать змейку в начальном состоянии."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновить направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Переместить змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

        self.position = new_head

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.position = CENTER_POSITION
        self.direction = choice(DIRECTIONS)
        self.next_direction = None
        self.last = None

    def draw(self):
        """Нарисовать змейку."""
        for position in self.positions:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обработать нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            if event.key == pygame.K_UP:
                new_direction = UP
            elif event.key == pygame.K_DOWN:
                new_direction = DOWN
            elif event.key == pygame.K_LEFT:
                new_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                new_direction = RIGHT
            else:
                continue

            opposite_direction = (
                -game_object.direction[0],
                -game_object.direction[1],
            )

            if new_direction != opposite_direction:
                game_object.next_direction = new_direction


def main():
    """Запустить основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    record = 1

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        elif head == apple.position:
            snake.length += 1

            if snake.last is not None:
                snake.positions.append(snake.last)

            record = max(record, snake.length)
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.set_caption(
            f'Змейка | Длина: {snake.length} | Рекорд: {record}'
        )

        pygame.display.update()


if __name__ == '__main__':
    main()
