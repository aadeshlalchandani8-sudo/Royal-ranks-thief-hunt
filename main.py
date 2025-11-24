import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, DictProperty

class GameState:
    players = []
    scores = DictProperty({})
    king = ""
    minister = ""
    soldier = ""
    thief = ""
    correct_guess = 0

GS = GameState()

class InputScreen(Screen):
    def add_players(self):
        p1 = self.ids.p1.text
        p2 = self.ids.p2.text
        p3 = self.ids.p3.text
        p4 = self.ids.p4.text

        GS.players = [p1, p2, p3, p4]
        for p in GS.players:
            GS.scores[p] = 0
        self.manager.current = "game"

class GameScreen(Screen):
    king = StringProperty("")
    minister = StringProperty("")
    soldier = StringProperty("")
    thief = StringProperty("")

    def on_pre_enter(self):
        roles = [1, 2, 3, 4]
        random.shuffle(roles)

        GS.king = GS.players[roles.index(1)]
        GS.minister = GS.players[roles.index(2)]
        GS.soldier = GS.players[roles.index(3)]
        GS.thief = GS.players[roles.index(4)]

        self.king = GS.king
        self.minister = GS.minister
        self.soldier = GS.soldier
        self.thief = GS.thief

    def check_guess(self, guess):
        thief_code = random.randint(1, 2)
        if guess == thief_code:
            GS.scores[GS.minister] += 500
        else:
            GS.scores[GS.thief] += 500

        GS.scores[GS.king] += 1000
        GS.scores[GS.soldier] += 100

        self.manager.current = "result"

class ResultScreen(Screen):
    leaderboard = StringProperty("")

    def on_pre_enter(self):
        sorted_scores = sorted(GS.scores.items(), key=lambda x: x[1], reverse=True)
        result = ""
        for name, score in sorted_scores:
            result += f"{name} : {score} pts\n"
        self.leaderboard = result

class RoyalRanks(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name="input"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ResultScreen(name="result"))
        return sm

if __name__ == "__main__":
    RoyalRanks().run()
        
