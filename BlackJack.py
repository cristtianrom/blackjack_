import random

# Se crea la baraja de cartas
def baraja():
    return [(v, p) for v in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] for p in ['Picas', 'Corazones', 'Diamantes', 'Treboles']]

# Se barajea
def barajear(mazo):
    return random.sample(mazo, len(mazo))

#Se calcula el valor a las manos
def valor_mano(mano):
    def valor_carta(carta):
        return {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}[carta[0]]
    return valor_mano_aux(sum(map(valor_carta, mano)), sum(1 for carta in mano if carta[0] == 'A'))

# Esta función es auxiliar si hay ases y si el total supera 21
def valor_mano_aux(total, ases):
    if total > 21 and ases > 0:
        return valor_mano_aux(total - 10, ases - 1)
    return total

# Se pide una carta para añadirla a la mano
def pedir_carta(mazo, mano):
    return mano.append(mazo.pop(0)) or mano[-1]

# Se reparten las cartas (iniciales)
def repartir_cartas():
    return repartir_cartas_aux(barajear(baraja()))

def repartir_cartas_aux(mazo):
    return (mazo[4:], [mazo[0], mazo[1]], [mazo[2], mazo[3]])

# Se verifica si la mano es un blackjack
def es_blackjack(mano):
    return valor_mano(mano) == 21 and len(mano) == 2

# Funcion principal
def jugar_blackjack(mazo, jugador, dealer):
    if es_blackjack(jugador) or es_blackjack(dealer):
        return (mazo, jugador, dealer)
    return jugar_blackjack_aux(mazo, jugador, dealer, input("¿Quieres pedir otra carta? (s/n): ").lower())

# Función para las decisiones del jugador
def jugar_blackjack_aux(mazo, jugador, dealer, accion):
    if accion == 's':
        print(f"Has tomado: {pedir_carta(mazo, jugador)}")
        if valor_mano(jugador) > 21:
            imprimir_manos(jugador, dealer, True)
            print("¡Te pasaste! El dealer gana.")
            return (mazo, jugador, dealer, True)
        return jugar_blackjack(mazo, jugador, dealer)
    else:
        imprimir_manos(jugador, dealer, True)
        input("Presiona Enter para continuar y ver el resultado...")
        return jugar_blackjack_dealer(mazo, jugador, dealer)

# Función para las decisiones del dealer
def jugar_blackjack_dealer(mazo, jugador, dealer):
    if valor_mano(dealer) < 17 or (valor_mano(dealer) == 17 and any(carta[0] == 'A' for carta in dealer)): # El dealer debe tener más de 17, caso contrario debe tomar una carta hasta ser mayor
        pedir_carta(mazo, dealer)
        return jugar_blackjack_dealer_aux(mazo, dealer, jugador)
    return (mazo, jugador, dealer)

def jugar_blackjack_dealer_aux(mazo, dealer, jugador):
    return jugar_blackjack_dealer(mazo, jugador, dealer)

# Se imprimen las manos del jugador y del dealer
def imprimir_manos(jugador, dealer, mostrar_valor_dealer):
    print(f"Mano del jugador: {jugador} - Valor: {valor_mano(jugador)}")
    if mostrar_valor_dealer:
        print(f"Mano del dealer: {dealer} - Valor: {valor_mano(dealer)}")
    else:
        print(f"Mano del dealer: {dealer[0]}, ?") # la segunda carta del dealer se revela cuando el jugador haya terminado su turno, es decir, cuando se haya plantado

# determina el resultado del juego
def resultado(valor_jugador, valor_dealer, jugador, dealer):
    if es_blackjack(jugador) and es_blackjack(dealer):
        print("Empate con blackjack.")
    elif es_blackjack(jugador):
        print("¡Blackjack! El jugador gana.")
    elif es_blackjack(dealer):
        print("¡Blackjack! El dealer gana.")
    elif valor_jugador > 21:
        print("¡Te pasaste! El dealer gana.")
    elif valor_dealer > 21:
        print("¡El dealer se pasó! El jugador gana.")
    elif valor_jugador > valor_dealer:
        print("¡Ganaste!")
    elif valor_jugador < valor_dealer:
        print("El dealer gana.")
    else:
        print("Empate.")

# función principal
def juego_blackjack():
    def juego_aux(mazo, jugador, dealer):
        imprimir_manos(jugador, dealer, False)
        return jugar_blackjack(mazo, jugador, dealer)

    def juego_aux2(result):
        if len(result) == 4 and result[3]:
            return result
        return juego_aux3(result)

    def juego_aux3(result):
        return imprimir_y_resultado(*result)

    def imprimir_y_resultado(mazo, jugador, dealer):
        imprimir_manos(jugador, dealer, True)
        return resultado(valor_mano(jugador), valor_mano(dealer), jugador, dealer)

    return juego_aux2(juego_aux(*repartir_cartas()))

def main():
    juego_blackjack()

if __name__ == "__main__":
    main()
