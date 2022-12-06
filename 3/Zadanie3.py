import typing
from typing import Callable
import msvcrt as kb


def try_input(
    prompt, /,
    check: Callable[[str], bool] = lambda _: True,
    convert: typing.Type = str,
    error: str | None = None
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


class StringMenu:
    options: list[tuple[str, Callable]]

    def __init__(self):
        self.options = []

    def add_option(self, option: str, callback: Callable = lambda: None) -> "StringMenu":
        self.options.append((option, callback))
        return self

    def _print(self):
        print('Menu'.center(max(map(lambda x: len(x[0]), self.options)) + 3, '-'))
        for i, option in enumerate(self.options, start=1):
            print(f"{i}) {option[0]}")

    def ask_and_do(self):
        self._print()
        selected = 0
        is_key = False
        print("Wybrano (↓↑):", self.options[selected][0], end='', flush=True)
        while (char := kb.getch()) != b'\r':
            if is_key:
                is_key = False
                key_code = ord(char.decode('utf-8'))
                last_size = len(self.options[selected][0])
                if key_code == 72:
                    print('\b \b' * last_size, end='')
                    selected = max(selected - 1, 0)
                    print(self.options[selected][0], end='')
                if key_code == 80:
                    print('\b \b' * last_size, end='')
                    selected = min(selected + 1, len(self.options) - 1)
                    print(self.options[selected][0], end='')
                print(flush=True, end='')
            if char == b'\xe0':
                is_key = True
        print('\n')
        self.options[selected][1]()
        print()


class Calculator:
    @staticmethod
    def ask_two_numbers(format_prompt: str, convert: typing.Type=float):
        a, b = \
            try_input(format_prompt % 1, convert=convert, error="Proszę wprowadzić prawidłową liczbę"),\
            try_input(format_prompt % 2, convert=convert, error="Proszę wprowadzić prawidłową liczbę")
        if a.is_integer(): a = int(a)
        if b.is_integer(): b = int(b)
        return a, b

    @staticmethod
    def addition():
        a, b = Calculator.ask_two_numbers("Podaj %s liczbę:", float)
        print(f"Wynik ({a} + {b}) = {a + b}")

    @staticmethod
    def subtraction():
        a, b = Calculator.ask_two_numbers("Podaj %s liczbę:", float)
        print(f"Wynik ({a} - {b}) = {a - b}")

    @staticmethod
    def multiplication():
        a, b = Calculator.ask_two_numbers("Podaj %s liczbę:", float)
        print(f"Wynik ({a} * {b}) = {a * b}")

    @staticmethod
    def division():
        a = try_input("Podaj licznik:", convert=float, error="Proszę wprowadzić prawidłową liczbę")
        b = try_input("Podaj mianownik:", check=lambda x: float(x) != 0.0,
                      convert=float, error="Proszę wprowadzić prawidłową liczbę")
        print(f"Wynik ({a} / {b}) = {a / b}")

    @staticmethod
    def power():
        a = try_input("Podaj podstawę potengi:", convert=float, error="Proszę wprowadzić prawidłową liczbę")
        b = try_input("Podaj licznik:", check=lambda x: not(float(x) == a == 0),
                      convert=float, error="Proszę wprowadzić prawidłową liczbę")

        print(f"Wynik ({a} ^ {b}) = {a ** b}")

    @staticmethod
    def factorial():
        a = try_input("Podaj liczbę:", convert=int, error="Proszę wprowadzić prawidłową liczbę")
        wynik = 1
        for i in range(2, a + 1):
            wynik *= i
        print(f"Wynik ({a}!) = {wynik}")

    @staticmethod
    def binary():
        a = try_input("Podaj liczbę:", convert=int, error="Proszę wprowadzić prawidłową liczbę")
        print("Wynik", bin(a)[2:])

    @staticmethod
    def octal():
        a = try_input("Podaj liczbę:", convert=int, error="Proszę wprowadzić prawidłową liczbę")
        print("Wynik", oct(a)[2:])

    @staticmethod
    def hexadecimal():
        a = try_input("Podaj liczbę:", convert=int, error="Proszę wprowadzić prawidłową liczbę")
        print("Wynik", hex(a)[2:])


while True:
    StringMenu()\
        .add_option("Dodawanie", Calculator.addition)\
        .add_option("Odejmowanie", Calculator.subtraction)\
        .add_option('Mnożenie', Calculator.multiplication)\
        .add_option('Dzielenie', Calculator.division)\
        .add_option('Potęgowanie', Calculator.power)\
        .add_option('Silnia', Calculator.factorial)\
        .add_option('System binarny (dwójkowy)', Calculator.binary)\
        .add_option('System oktalny (usemkowy)', Calculator.octal)\
        .add_option('System heksadecymalny (szesnastkowy)', Calculator.hexadecimal)\
        .add_option('Wyjście z programu', exit)\
        .ask_and_do()
