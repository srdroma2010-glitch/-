from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
import random

COLS = 15
ROWS = 22


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reset()
        Clock.schedule_interval(self.update, 0.15)

    def reset(self):
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.new_food()
        self.score = len(self.snake)
        self.alive = True
        self.touch_start = None
        self.draw_game()

    def new_food(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.snake:
                return pos

    def update(self, dt):
        if not self.alive:
            return
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        new_head = (hx + self.direction[0], hy + self.direction[1])
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.alive = False
            self.draw_game()
            return
        if new_head in self.snake[:-1]:
            self.alive = False
            self.draw_game()
            return
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.new_food()
        else:
            self.snake.pop()
        self.draw_game()

    def draw_game(self):
        self.canvas.clear()
        w, h = self.size
        cw = w / COLS
        ch = h / ROWS
        with self.canvas:
            Color(0.06, 0.09, 0.13)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.1, 0.15, 0.22)
            for i in range(COLS + 1):
                Rectangle(pos=(self.x + i * cw, self.y), size=(1, h))
            for j in range(ROWS + 1):
                Rectangle(pos=(self.x, self.y + j * ch), size=(w, 1))
            fx, fy = self.food
            Color(1, 0.3, 0.3)
            Ellipse(pos=(self.x + fx * cw + cw * 0.15, self.y + (ROWS - 1 - fy) * ch + ch * 0.15), size=(cw * 0.7, ch * 0.7))
            for i, (sx, sy) in enumerate(self.snake):
                if i == 0:
                    Color(0.5, 1, 0.6)
                else:
                    t = i / max(1, len(self.snake) - 1)
                    Color(0.2, 0.7 - t * 0.3, 0.4)
                Ellipse(pos=(self.x + sx * cw + cw * 0.1, self.y + (ROWS - 1 - sy) * ch + ch * 0.1), size=(cw * 0.8, ch * 0.8))

    def on_touch_down(self, touch):
        if not self.alive:
            self.reset()
            return True
        self.touch_start = touch.pos
        return True

    def on_touch_up(self, touch):
        if self.touch_start is None:
            return False
        dx = touch.pos[0] - self.touch_start[0]
        dy = touch.pos[1] - self.touch_start[1]
        self.touch_start = None
        if max(abs(dx), abs(dy)) < 25:
            return False
        if abs(dx) > abs(dy):
            if dx > 0 and self.direction != (-1, 0):
                self.next_direction = (1, 0)
            elif dx < 0 and self.direction != (1, 0):
                self.next_direction = (-1, 0)
        else:
            if dy > 0 and self.direction != (0, -1):
                self.next_direction = (0, 1)
            elif dy < 0 and self.direction != (0, 1):
                self.next_direction = (0, -1)
        return True


class SnakeApp(App):
    def build(self):
        Window.clearcolor = (0.06, 0.09, 0.13, 1)
        return SnakeGame()


if __name__ == '__main__':
    SnakeApp().run()
