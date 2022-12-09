import typing


def try_input(
        prompt: str, /,
        check: typing.Callable[[str], bool] = lambda _: True,
        convert: typing.Type = str,
        error: str = None) -> typing.Any:
    print(prompt, end=' ')
    while True:
        value = input()
        try:
            if not check(value):
                raise ValueError
            return convert(value)
        except ValueError:
            if error is not None:
                print(error, end='')


class Player:
    score: int
    strike_multiplier: [int]
    spare_multiplier: int
    number: int

    def __init__(self):
        self.score = 0
        self.strike_multiplier = []
        self.spare_multiplier = 0

    def get_multiplier_and_reduce(self):
        for i in range(len(self.strike_multiplier)):
            self.strike_multiplier[i] -= 1
        amount = len(self.strike_multiplier)
        self.strike_multiplier = [x for x in self.strike_multiplier if x > 0]
        return amount

    def require_multiplier(self):
        flag = self.strike_multiplier or self.spare_multiplier
        self.spare_multiplier = max(self.spare_multiplier - 1, 0)
        return not not flag

    def set_strike_multiplier(self):
        self.strike_multiplier += [2]
        print("Strike")

    def set_spare_multiplier(self):
        self.spare_multiplier += 1
        print("Spare")


class Throw:
    def __init__(self):
        self.pins = 10

    def __call__(self, pins: int) -> bool:
        self.pins -= pins
        return self.pins == 0


class Frame:
    COUNT = 10
    number: int

    def __init__(self, number: int, players: [Player], on_frame_end: typing.Callable = lambda: None):
        self.number = number
        print(f"Frame {number}")
        for player in players:
            multiplier = player.get_multiplier_and_reduce()

            pins = try_input(f"Player {player.number} shoot: ",
                             check=lambda x: 0 <= int(x) <= 10, convert=int,
                             error="Wprowadź ponownie")

            throw = Throw()
            if throw(pins):
                player.set_strike_multiplier()
            else:
                player.throws.append(throw)
                player.score += pins + (pins * multiplier)
                player.throws[-1] += pins + (pins * multiplier)
                multiplier = player.get_multiplier_and_reduce()
                pins = try_input(f"Player {player.number} shoot: ",
                                 check=lambda x: 0 <= int(x) <= throw.pins, convert=int,
                                 error="Wprowadź ponownie")
                if throw(pins):
                    player.set_spare_multiplier()

            player.score += pins + (pins * multiplier)

            if throw.pins == 10:
                print("Miss")

            if number == Frame.COUNT:
                if throw.pins == 0:
                    multiplier = player.get_multiplier_and_reduce()
                    pins = try_input(f"Player {player.number} shoot: ",
                                     check=lambda x: 0 <= int(x) <= 10, convert=int,
                                     error="Wprowadź ponownie")
                    if pins == 10:
                        player.set_strike_multiplier()
                    player.score += pins + (pins * multiplier)
        on_frame_end()


class Game:
    def __init__(self, players: ['Player']):
        self.players = players
        self.frames = [Frame(i, players, self.scoreboard) for i in range(1, Frame.COUNT + 1)]

    def scoreboard(self):
        print("-------" + "-" * len(str(len(self.players))) + "+-" + \
              "-" * len(str(max(self.players, key=lambda x: x.score).score)))
        for i, player in enumerate(self.players):
            print(f"Gracz {i + 1} | {player.score}")


def main():
    players = [Player() for _ in range(try_input("Ile graczy? ", check=lambda x: 0 < int(x) <= 4, convert=int))]
    for i, player in enumerate(players):
        player.number = i + 1
    game = Game(players)
    #game.scoreboard()

    print("Wygrał gracz numer", max(players, key=lambda x: x.score).number)


if __name__ == '__main__':
    main()
