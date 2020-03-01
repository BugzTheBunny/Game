from kivy.app import App
from Player import GameWidget

class myGame(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    app = myGame()
    app.run()