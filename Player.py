from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Triangle
from kivy.core.window import Window
from kivy.clock import Clock
import random


def collide(player, object):
    p_x = player[0][0]
    p_y = player[0][1]
    e_x = object[0][0]
    e_y = object[0][1]

    p_w = player[1][0]
    p_h = player[1][1]
    e_w = object[1][0]
    e_h = object[1][1]

    if (p_x < e_x + e_w and
            p_x + p_w > e_x and
            p_y < e_y + e_h and
            p_y + p_h > e_y):
        return True
    else:
        return False


class GameWidget(Widget):
    """
    This will be the game widget.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_close, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        with self.canvas:
            self.ground = Rectangle(pos=(0, 0), size=(800, 40))
            self.player = Rectangle(source="player.png", pos=(0, self.ground.size[1]), size=(48, 40))
            self.trap = Triangle(pos=(5, 5))
            self.enemy = Rectangle(pos=(100, 100), size=(50, 50))

        self.keysPressed = set()
        gravity = 0
        Clock.schedule_interval(self.move_step, 0)

    def _on_keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifier):
        self.keysPressed.add(text)

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_step(self, dt):
        """
        dt - fps
        and movable text
        :param dt:
        :return:
        """
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        step_size = 100 * dt

        if "w" in self.keysPressed:
            self.player.source = 'player_jump.png'
            currenty += step_size * 10
        if "s" in self.keysPressed:
            currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size
        self.player.pos = (currentx, currenty)

        # Gravity (If you wont press W)
        if 'w' not in self.keysPressed:
            currenty -= random.randint(3, 7)
            self.player.pos = (currentx, currenty)
            self.player.source = 'player.png'

        if collide((self.player.pos, self.player.size), (self.enemy.pos, self.enemy.size)):
            self.enemy.pos = (random.randint(0, 500), random.randint(0, 500))

        if collide((self.player.pos, self.player.size), (self.ground.pos, self.ground.size)):
            self.player.pos = (currentx, self.ground.size[1])
