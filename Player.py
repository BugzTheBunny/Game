from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.core.window import Window
from kivy.clock import Clock
import random

def collide(player,enemy):
    p_x = player[0][0]
    p_y = player[0][1]
    e_x = enemy[0][0]
    e_y = enemy[0][1]

    p_w = player[1][0]
    p_h = player[1][1]
    e_w = enemy[1][0]
    e_h = enemy[1][1]

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
            self.player = Rectangle(pos=(200, 200), size=(20, 30))
            self.enemy = Rectangle(pos=(500,500), size = (50, 50))
            # If image:
            # Rectangle(source="player.png", size=(100, 50))

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

        step_size = 200 * dt
        # Movement.
        if "w" in self.keysPressed:
            gravity = 0
            currenty += step_size * 2.5
        if "s" in self.keysPressed:
            currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size
        self.player.pos = (currentx, currenty)

        # if self.player.pos == self.enemy.pos:
        #     print('Collide')
        # Gravity (If you wont press W)
        if 'w' not in self.keysPressed:
            currenty -= random.randint(3,7)
            self.player.pos = (currentx, currenty)

        if collide((self.player.pos, self.player.size),(self.enemy.pos,self.enemy.size)):
            self.enemy.pos = (random.random(100,800),random.random(100,800))