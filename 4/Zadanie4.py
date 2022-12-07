# Bowling Simulation
import typing


def try_input(
        prompt: str, /,
        check: typing.Callable[[str], bool] = lambda _: True,
        convert: typing.Type = str,
        error: str = None
) -> typing.Any:
    print(prompt, end=' ')
    while True:
        value = input()
        try:
            if not check(value):
                raise ValueError
            return convert(value)
        except ValueError:
            if error is not None:
                print(error)


class Player:
    score: int
    """ `0` means no multiplier """
    strike_multiplier: int
    """ `0` means no multiplier """
    spare_multiplier: int

    def __init__(self):
        self.score = 0
        self.strike_multiplier = 0
        self.spare_multiplier = 0

    def set_strike_multiplier(self):
        self.strike_multiplier = 2
        print("STRIKE")

    def set_spare_multiplier(self):
        self.spare_multiplier = 1
        print("SPARE")

    def shoot(self, pins: int):
        if self.strike_multiplier:
            self.strike_multiplier -= 1
            self.score += pins
        if self.spare_multiplier:
            self.spare_multiplier -= 1
            self.score += pins
        self.score += pins


class Game:
    players: list[Player]
    current_player = 0

    def __init__(self, rounds=10):
        self.players = []
        self.rounds=rounds

    def add_player(self, player: Player) -> "Game":
        self.players.append(player)
        return self

    def next(self, last=False):
        print(f"Gracz numer: {self.current_player + 1}")
        pins = try_input(
            "Wprowadź ilość zbitych kręgli",
            convert=int, check=lambda x: 0 <= int(x) <= 10,
            error="Wprowadź ponownie")
        player = self.players[self.current_player]
        player.shoot(pins)
        if pins == 10:
            player.set_strike_multiplier()
            second_pins = 0
        else:
            second_pins = try_input(
                "Wprowadź ilość zbitych kręgli",
                convert=int, check=lambda x: 0 <= int(x) + pins <= 10,
                error="Wprowadź ponownie")

            if pins + second_pins == 10:
                return player.set_spare_multiplier()
            elif pins + second_pins == 0:
                return print("Miss")

        if last and pins + second_pins == 10:
            last_pins = try_input(
                "Wprowadź ilość zbitych kręgli",
                convert=int, check=lambda x: 0 <= int(x) <= 10,
                error="Wprowadź ponownie")
            player.shoot(last_pins)

    def play(self):
        for i in range(self.rounds - 1):
            self.current_player = 0
            print(f"Runda {i + 1}")
            for _ in self.players:
                self.next()
                self.current_player += 1
        print(f"Runda {self.rounds}")
        self.current_player = 0
        for _ in self.players:
            self.next(True)
            self.current_player += 1
        self.scoreboard()

    def scoreboard(self):
        print("------" + "-" * len(str(len(self.players))))
        for i, player in enumerate(self.players):
            print(f"Gracz {i + 1} | {player.score}")


if __name__ == '__main__':
    Game(12)\
        .add_player(Player())\
        .add_player(Player())\
        .play()
