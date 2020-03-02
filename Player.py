from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Triangle
from kivy.core.window import Window
from kivy.clock import Clock
import random
import time


def collide(player, object):
    player = (player.pos, player.size)
    object = (object.pos, object.size)

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
        ride_animations = ['src/ride_1.png', 'src/ride_2.png']
        with self.canvas:

            # Backgrounds
            self.background2 = Rectangle(source='src/background.jpg', size=(800, 600))
            self.background = Rectangle(source='src/background.jpg', size=(802, 600), pos=(800, 0))
            self.sun = Rectangle(source='src/sun.png',size=(150,150), pos=(500,450))
            # Ground Model
            self.ground = Rectangle(pos=(0, 0), size=(800, 20))
            # Player Model
            self.player = Rectangle(source=random.choice(ride_animations), pos=(0, self.ground.size[1]), size=(96, 80))
            # Rocket Model
            self.rocket = Rectangle(source='src/enemy_rocket.png', size=(60, 30))
            # Enemy Model
            self.enemy = Rectangle(pos=(100, 100), size=(50, 50))
            # Platform Model
            self.platform = Rectangle(pos=(799, random.randint(100, 400)), size=(random.randint(100, 400), 20))

        self.keysPressed = set()
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
        ride_animations = ['src/ride_1.png', 'src/ride_2.png']
        rocket_x = self.rocket.pos[0]
        rocket_y = self.rocket.pos[1]

        platform_x = self.platform.pos[0]
        platform_y = self.platform.pos[1]

        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        bg_1_x = self.background.pos[0]
        bg_2_x = self.background2.pos[0]

        sun_x = self.sun.pos[0]

        step_size = 300 * dt


        if "a" in self.keysPressed:
            currentx -= step_size * 3
        if "d" in self.keysPressed:
            currentx += step_size * 3

        # Gravity (While not pressing W)
        if 'w' not in self.keysPressed:
            if collide(self.player, self.ground) is False and collide(self.player, self.platform) is False:
                currenty -= 3  # Gravity power
            self.player.pos = (currentx, currenty)
            self.player.source = random.choice(ride_animations)

        # ==============================================
        # Ride on Ground
        if collide(self.player, self.ground):
            self.player.pos = (currentx, currenty + self.ground.pos[1])
            if 'd' not in self.keysPressed:
                self.player.source = random.choice(ride_animations)
            else:
                self.player.source = 'player_jump.png'

        # Ride on platform
        elif collide(self.player, self.platform):
            self.player.pos = (currentx, self.platform.pos[1] + 20)
            if 'd' not in self.keysPressed:
                self.player.source = random.choice(ride_animations)
            else:
                self.player.source = 'player_jump.png'

        if collide(self.player, self.ground) and "w" in self.keysPressed or collide(self.player, self.platform) and "w" in self.keysPressed:
            if currenty < 200:
                currenty += step_size * 30
            self.player.source = 'player_jump.png'
            self.player.pos = (currentx, currenty)

        # ==============================================
        # If you hit a rocket.
        if collide(self.player, self.rocket):
            print('BOOM!')

        # point HIT
        if collide(self.player, self.enemy):
            self.enemy.pos = (random.randint(0, 500), random.randint(0, 500))

        # ==============================================
        # rocket
        if self.rocket.pos[0] > -5:
            self.rocket.pos = (rocket_x - random.randint(0, 10), rocket_y)
        else:
            self.rocket.pos = (799, random.randint(0, 100))
        # Platform
        if self.platform.pos[0] > -self.platform.size[0]:
            self.platform.pos = (platform_x - 1, platform_y)
        else:
            self.platform.pos = (799, random.randint(0, 30))

        # Background movement
        if bg_1_x > -800:
            self.background.pos = (bg_1_x - 0.5, self.background.pos[1])
        elif bg_1_x == -800:
            bg_1_x = 800
            self.background.pos = (bg_1_x, self.background.pos[1])
        if bg_2_x > -800:
            self.background2.pos = (bg_2_x - 0.5, self.background2.pos[1])
        elif bg_2_x == -800:
            bg_2_x = 800
            self.background2.pos = (bg_2_x, self.background2.pos[1])

        sun_x -= 0.2
        self.sun.pos = (sun_x,self.sun.pos[1])
