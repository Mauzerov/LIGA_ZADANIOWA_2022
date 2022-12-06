from typing import Any, Type
from random import choice
import msvcrt
from typing import Callable


def exit_input(prompt: str = '', /, on_esc=lambda: None) -> str:
    value = ''
    print(prompt, end='', flush=True)
    while (char := msvcrt.getwche()) != '\r':
        if char == '\b':
            value = value[:-1]
            msvcrt.putwch(' ')
            msvcrt.putwch('\b')
            continue
        if char == '\x1b':
            on_esc()
            continue
        value += char
    return value


def try_input(
        prompt: str, /,
        condition: Callable[[str], tuple[bool, Any]] = lambda _: (True, None),
        convert: Type = str,
        on_esc=lambda: None,
        error: str = None) -> Any:
    while True:
        value = exit_input(prompt, on_esc)
        try:
            result, msg = condition(value)
            if result:
                print(flush=True)
                return convert(value)
            elif msg is not None:
                error = msg
        except ValueError:
            pass
        if error is not None:
            print(flush=True)
            print(error)


przedmioty = [1, 2, 3, 4, 5]
ilosc_ocen = try_input("Podaj Ilość Ocen: ",
                       condition=lambda x: (0 < int(x) <= 30, "Za duża liczba ocen"),
                       convert=int,
                       on_esc=exit,
                       error="Proszę wprowadzić liczbę całkowitą w zakresie od 1 do 30")

oceny = []

for i in range(ilosc_ocen):
    przedmiot = choice(przedmioty)
    waga = try_input(f"Podaj Wagę Oceny z {przedmiot}: ",
                     condition=lambda x: (0 < int(x) <= 5, None),
                     convert=int,
                     on_esc=exit,
                     error="Proszę wprowadzić liczbę całkowitą w zakresie od 1 do 5")

    ocena = try_input(f"Podaj Ocenę z {przedmiot}: ",
                      condition=lambda x: (0 < int(x) <= 6, None),
                      convert=int,
                      on_esc=exit,
                      error="Nieprawidłowa ocena, proszę wprowadzić ponownie")

    oceny.append((ocena, waga, przedmiot))

for ocena, waga, przedmiot in oceny:
    print(f'{przedmiot=} {ocena=} {waga=}')


suma_ocen, suma_wag = sum(map(lambda o: o[0] * o[1], oceny)), sum(map(lambda o: o[1], oceny))
srednia = round(suma_ocen / suma_wag, 2)
print(f"Średnia: {srednia}. " + ("Gratuluję otrzymujesz wyróżnienie :-)" if srednia >= 4.75 else ''), flush=True)
