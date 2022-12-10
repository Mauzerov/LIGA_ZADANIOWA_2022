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
    """ `0` means no multiplier """
    strike_multiplier: [int]
    """ `0` means no multiplier """
    spare_multiplier: int
    throws: [int]

    def __init__(self):
        self.score = 0
        self.strike_multiplier = []
        self.spare_multiplier = 0
        self.throws = []

    def get_multiplier_and_reduce(self):
        for i in range(len(self.strike_multiplier)):
            self.strike_multiplier[i] -= 1
        amount = len(self.strike_multiplier)
        self.strike_multiplier = [x for x in self.strike_multiplier if x > 0]
        return amount

    def require_multiplier(self):
        flag = self.strike_multiplier or self.spare_multiplier
        #self.strike_multiplier -= max(0, self.strike_multiplier - 1)
        self.spare_multiplier = max(self.spare_multiplier - 1, 0)
        return not not flag

    def set_strike_multiplier(self):
        self.strike_multiplier += [2]
        print("STRIKE")

    def set_spare_multiplier(self):
        self.spare_multiplier += 1
        print("SPARE")


class Throw:
    def __init__(self):
        self.pins = 10

    def __call__(self, pins: int) -> bool:
        if pins == 0:
            print("Miss")
        self.pins -= pins
        return self.pins == 0


class Frame:
    number: int

    def __init__(self, number: int, players: [Player]):
        self.number = number
        print(f"Frame {number}")
        for player in players:
            multiplier = player.get_multiplier_and_reduce()

            pins = try_input(f"Player {player.number} shoot: ",
                             check=lambda x: 0 <= int(x) <= 10, convert=int,
                             error="Proszę wprowadzić liczbę całkowitą w zakresie od 0 do 10")

            throw = Throw()
            player.throws.append(0)
            if throw(pins):
                player.set_strike_multiplier()
            else:
                player.throws.append(throw)
                player.score += pins + (pins * multiplier)
                player.throws[-1] += pins + (pins * multiplier)
                multiplier = player.get_multiplier_and_reduce()
                pins = try_input(f"Player {player.number} shoot: ",
                                 check=lambda x: 0 <= int(x) <= throw.pins, convert=int,
                                 error=f"Proszę wprowadzić liczbę całkowitą w zakresie od 0 do {throw.pins}")
                if throw(pins):
                    player.set_spare_multiplier()
            player.score += pins + (pins * multiplier)
            player.throws[-1] += pins + (pins * multiplier)
        # Todo Last frame (10th) is different

class Game:
    def __init__(self, players: ['Player']):
        self.players = players
        self.frames = [Frame(i, players) for i in range(1, 11)]


def main():
    players = [Player() for _ in range(try_input("Ile graczy? ", check=lambda x: 0 < int(x) <= 4, convert=int))]
    for i, player in enumerate(players):
        player.number = i + 1
    game = Game(players)
    for player in players:
        print(f"Player {player.number} score: {player.score} {player.throws}")


if __name__ == '__main__':
    main()


