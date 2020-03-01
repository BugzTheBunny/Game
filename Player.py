from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Triangle
from kivy.core.window import Window
from kivy.clock import Clock
import random
import time



def collide(player, object):
    player = (player.pos,player.size)
    object = (object.pos,object.size)
    p_x = player[0][0]
    p_y = player[0][1]
    e_x = object[0][0]
    e_y = object[0][1]

    p_w = player[1][0]
    p_h = player[1][1]
    e_w = object[1][0]
    e_h = object[1][1]

    if (p_x < e_x + e_w + 0.01 and
            p_x + p_w + 0.01 > e_x and
            p_y < e_y + e_h + 0.01 and
            p_y + p_h + 0.01 > e_y):
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
            self.ground = Rectangle(pos=(0, 0), size=(800, 20))
            self.player = Rectangle(source="player.png", pos=(0, self.ground.size[1]), size=(48, 40))
            self.trap = Triangle(pos=(5, 5))
            self.enemy = Rectangle(pos=(100, 100), size=(50, 50))

        self.keysPressed = set()
        Clock.schedule_interval(self.move_step, 0)
        Clock.schedule_interval(self.jump, 0)
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

    def jump(self,dt):
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        step_size = 60 * dt

        if collide(self.player, self.ground) and "w" in self.keysPressed:
            self.player.source = 'player_jump.png'
            for (i) in range(400):
                jump = i/2
                self.player.pos = (currentx, currenty+jump)

    def move_step(self, dt):
        """
        dt - fps
        and movable text
        :param dt:
        :return:
        """
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        step_size = 60 * dt

        # if collide(self.player, self.ground) and "w" in self.keysPressed:
        #     self.player.source = 'player_jump.png'
        #     for (i) in range(400):
        #         time.sleep(0.1)
        #         jump = i/2
        #         self.player.pos = (currentx, currenty+jump)
        #         print(self.player.pos)
        # if "s" in self.keysPressed:
        #     currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size * 2
        if "d" in self.keysPressed:
            currentx += step_size * 2


        # Gravity (If you wont press W)
        if 'w' not in self.keysPressed and collide(self.player, self.ground) is False:
            currenty -= random.randint(6,7)
            self.player.pos = (currentx, currenty)
            self.player.source = 'player.png'
        if collide(self.player, self.enemy):
            self.enemy.pos = (random.randint(0, 500), random.randint(0, 500))

        if collide(self.player, self.ground):
            self.player.pos = (currentx, self.ground.size[1])
            if 'd' not in self.keysPressed:
                self.player.source = 'player.png'
            else:
                self.player.source = 'player_jump.png'
            # print(f'{collide(self.player, self.ground)} - {self.player.pos} {self.ground.pos}')