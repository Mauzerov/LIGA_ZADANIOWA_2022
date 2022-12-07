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
    # probably change to list of ints and decrement all at the same time (or just use a counter)
    # counter would be better, because it would be easier to implement triple strike,
    # and it would be easier to implement a game with more than 10 frames
    # counter:
    # def set_strike_multiplier(self):
    #     self.strike_multiplier += 2
    # def shoot(self, pins: int):
    #     old_score = self.score
    #     self.score += pins
    #     if self.strike_multiplier:
    #         self.score += self.previous_shoot
    #         self.strike_multiplier -= 1
    #     if self.spare_multiplier:
    #         self.score += self.previous_shoot
    #         self.spare_multiplier -= 1
    #     self.previous_shoot = self.score - old_score
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
        self.strike_multiplier = 2
        print("STRIKE")

    def set_spare_multiplier(self):
        self.spare_multiplier = 1
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
            "Wprowadź ilość zbitych kręgli",
            convert=int, check=lambda x: 0 <= int(x) <= self.pins,
            error="Wprowadź ponownie")
        self.pins -= pins
        player = self.players[self.current_player]
        has_bonus = not not player.strike_multiplier or not not player.spare_multiplier

        if self.pins == 0:
            player.set_strike_multiplier()
        else:
            pins = try_input(
                "Wprowadź ilość zbitych kręgli",
                convert=int, check=lambda x: 0 <= int(x) <= self.pins,
                error="Wprowadź ponownie")
            self.pins -= pins

            if self.pins == 0:
                player.set_spare_multiplier()

        pins_total = 10 - self.pins
        if has_bonus:
            print("Bonus", pins_total)
            player.score += pins_total
        player.score += pins_total
        # player.previous_shoot = (pins_total + player.previous_shoot) if has_bonus else 0
        # #player.shoot(pins)
        # if pins == 10:
        #     player.set_strike_multiplier()
        #     second_pins = 0
        # else:
        #     second_pins = try_input(
        #         "Wprowadź ilość zbitych kręgli",
        #         convert=int, check=lambda x: 0 <= int(x) + pins <= 10,
        #         error="Wprowadź ponownie")
        #
        #     if pins + second_pins == 10:
        #         return player.set_spare_multiplier()
        #     elif pins + second_pins == 0:
        #         return print("Miss")
        #
        # if last and pins + second_pins == 10:
        #     last_pins = try_input(
        #         "Wprowadź ilość zbitych kręgli",
        #         convert=int, check=lambda x: 0 <= int(x) <= 10,
        #         error="Wprowadź ponownie")
        #     player.shoot(last_pins)

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
        print("-------" + "-" * len(str(len(self.players))))
        for i, player in enumerate(self.players):
            print(f"Gracz {i + 1} | {player.score}")


if __name__ == '__main__':
    Game(10) \
        .add_player(Player()) \
        .play()
