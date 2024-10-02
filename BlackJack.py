import random


def baraja():
    return [(v, p) for v in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] for p in
            ['D', 'C', 'T', 'P']]


def barajear(mazo):
    return random.sample(mazo, len(mazo))


def valor_mano(mano):
    def valor_carta(carta):
        return \
        {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}[
            carta[0]]

    return valor_mano_aux(sum(map(valor_carta, mano)), sum(1 for carta in mano if carta[0] == 'A'))


def valor_mano_aux(total, ases):
    if total > 21 and ases > 0:
        return valor_mano_aux(total - 10, ases - 1)
    return total


def pedir_carta(mazo, mano):
    return (mazo[1:], mano + [mazo[0]])


def repartir_cartas():
    return repartir_cartas_aux(barajear(baraja()))


def repartir_cartas_aux(mazo):
    return (mazo[4:], [mazo[0], mazo[1]], [mazo[2], mazo[3]])


def jugar_blackjack(mazo, jugador, dealer):
    return jugar_blackjack_aux(mazo, jugador, dealer, input("Quiere pedir otra carta? (s/n): ").lower())


def jugar_blackjack_aux(mazo, jugador, dealer, accion):
    if accion == 's':
        return jugar_blackjack(*pedir_carta(mazo, jugador), dealer)
    else:
        return jugar_blackjack_dealer(mazo, jugador, dealer)


def jugar_blackjack_dealer(mazo, jugador, dealer):
    if valor_mano(dealer) < 17:
        return jugar_blackjack_dealer(*pedir_carta(mazo, dealer), jugador)
    else:
        return (jugador, dealer)


def imprimir_manos(jugador, dealer, mostrar_valor_dealer):
    print(f"Mano del jugador: {jugador} - Valor: {valor_mano(jugador)}")
    if mostrar_valor_dealer:
        print(f"Mano del dealer: {dealer} - Valor: {valor_mano(dealer)}")
    else:
        print(f"Mano del dealer: {dealer[0]}, ?")


def resultado(valor_jugador, valor_dealer):
    print("Uy, se pasó. El dealer gana") if valor_jugador > 21 else (
        print("Ganaste") if valor_dealer > 21 or valor_jugador > valor_dealer else (
            print("El dealer gana") if valor_jugador < valor_dealer else print("Empate")
        )
    )


def juego_blackjack():
    def juego_aux(mazo, jugador, dealer):
        imprimir_manos(jugador, dealer, False)
        return juego_aux2(jugar_blackjack(mazo, jugador, dealer))

    def juego_aux2(result):
        return juego_aux3(result[0], result[1])

    def juego_aux3(jugador, dealer):
        imprimir_manos(jugador, dealer, True)
        return resultado(valor_mano(jugador), valor_mano(dealer))

    return juego_aux(*repartir_cartas())


def main():
    juego_blackjack()


if __name__ == "__main__":
    main()