# Bowling Simulation

class Player:
    score: int
    has_strike_multiplier: bool
    has_spare_multiplier: bool

    def __init__(self):
        self.score = 0
        self.has_strike_multiplier = False
        self.has_spare_multiplier = False

    def shoot(self, pins: int, second_shot: bool = True, *, previous: int = 0):
        if self.has_strike_multiplier or (self.has_spare_multiplier and not second_shot):
            self.score += pins
        if pins == 10 and not second_shot:
            print("STRIKE")
            self.has_strike_multiplier = True
            self.has_spare_multiplier = False
        elif previous + pins == 10 and second_shot:
            print("SPARE")
            self.has_spare_multiplier = True
            self.has_strike_multiplier = False
        elif second_shot:
            self.has_strike_multiplier = False
            self.has_spare_multiplier = False
        else:
            self.has_spare_multiplier = False
        self.score += pins


if __name__ == '__main__':
    player = Player()
    for i in range(3):
        print("Frame: ", i+1)
        pins = int(input("Pins: "))
        player.shoot(pins, False)
        if pins != 10:
            player.shoot(int(input("Pins: ")), previous=pins)
    print("Score: ", player.score)
