# Create bowling game simulator
# for n players where n is an integer given from standrd input
# game is lasting 10 frames during which playeer can pthrow ball twice except last frame where evene 3 times if he gets strike or spare
# if player gets strike he gets 10 points and 2 next throws are multiplied by 2
# if player gets spare he gets 10 points and 1 next throw is multiplied by 2
# if player gets 0 points he gets 0 points
# if player gets 1-9 points he gets 1-9 points
# if player gets atrike or spare print Strike or spare accordingly
# if player gets 0 points print Miss
# at the en print which player wins and how many pinst they had
# between every frame print scoreboard with players and their scores


class Player:
    score: int
    """ `0` means no multiplier """
    strike_multiplier: int
    """ `0` means no multiplier """
    spare_multiplier: int

    previous_shoot: int

    def __init__(self):
        self.score = 0
        self.previous_shoot = 0
        self.strike_multiplier = 0
        self.spare_multiplier = 0

    def set_strike_multiplier(self):
        self.strike_multiplier += 2
        print("STRIKE")

    def set_spare_multiplier(self):
        self.spare_multiplier += 1
        print("SPARE")

    def shoot(self, pins: int):
        old_score = self.score
        if self.strike_multiplier:
            self.strike_multiplier -= 1
            self.score += self.previous_shoot
        if self.spare_multiplier:
            self.spare_multiplier -= 1
            self.score += self.previous_shoot
        self.score += pins
        self.previous_shoot = self.score - old_score

    def __str__(self):
        return f"{self.score}"


class Game:
    players: list[Player]
    current_player = 0
    pins: int = 10

    def __init__(self, rounds=10):
        self.players = []
        self.rounds = rounds

    def add_player(self, player: Player) -> "Game":
        self.players.append(player)
        return self

    def next(self, last=False):
        print(f"Gracz numer: {self.current_player + 1}")
        self.pins = 10
        pins = try_input(
            "Podaj ilość uderzonych pinów: ",
            lambda x: x.isdigit() and int(x) <= self.pins,
            "Podaj liczbę całkowitą z zakresu 0 do 10",
        )
        pins = int(pins)
        self.pins -= pins
        self.players[self.current_player].shoot(pins)
        if pins == 10:
            self.players[self.current_player].set_strike_multiplier()
        elif self.pins == 0:
            self.players[self.current_player].set_spare_multiplier()
        elif pins == 0:
            print("MISS")
        else:
            print(f"Zdobyłeś {pins} punktów")
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0
            if not last:
                print("Następna runda")
            else:
                print("Koniec gry")
            print("Wyniki:")
            for i, player in enumerate(self.players):
                print(f"Gracz {i + 1}: {player}")

    def run(self):
        for i in range(self.rounds - 1):
            for _ in range(len(self.players)):
                self.next()
        for _ in range(len(self.players)):
            self.next(True)


def try_input(prompt, condition, error_message):
    while True:
        value = input(prompt)
        if condition(value):
            return value
        print(error_message)


def main():
    game = Game()
    players = try_input(
        "Podaj ilość graczy: ",
        lambda x: x.isdigit() and int(x) > 0,
        "Podaj liczbę całkowitą większą od 0",
    )
    players = int(players)
    for _ in range(players):
        game.add_player(Player())
    game.run()


if __name__ == "__main__":
    main()

