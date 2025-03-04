modo = 0


import threading, platform
from random import randrange

POSICION = 1
OS = platform.system()

con_inicial = False
g = open("log.txt", "w")
g.close()

def escribir(dato):
    f = open("log.txt", "a")
    f.write(str(dato) + "\n")
    f.close()

def obtenerDadosIngresados():
    global caja_entrada_dados, texto_ingresado
    texto_ingresado = caja_entrada_dados.get()

def seleccionarOpcion():
    global seleccion
    seleccion = True

class jugador:

    def __init__(self, nombre, color, fichas, GanoJugador=False, UltimaFicha=None):
        self.nombre = nombre
        self.color = color
        self.fichas = fichas
        self.UltimaFicha = UltimaFicha
        self.GanoJugador = GanoJugador
        self.Posicion = 0

    def DefinirUltimaFicha(self, jugadorActual, Ficha):
        self.UltimaFicha = Ficha

    def TirarUnDado(self, con_inicial):

        x = 0
        if not con_inicial:
            if modo < 3:
                print("%s PRESIONE ENTER PARA LANZAR EL DADO:" % self.nombre)
                input()
                x = randrange(1, 7)
                print("SU RESULTADO ES %d\n" % x)
            else:
                inp = ""
                texto_ingresado = ""
                while inp == "":
                    inp = texto_ingresado
                x = randrange(1, 7)
        else: #MODO DESARROLLADOR
            x = 0
            texto_ingresado = "7"
            while x <= 0 or x > 6:
                if modo < 3:
                    x = input("INGRESE EL VALOR DEL DADO " + self.nombre + ":\n")
                else:
                    x = texto_ingresado
                try:
                    x = int(x)
                except:
                    x = 0
        return x

    def TirarDosDados(self, con_inicial):

        global modo, texto_ingresado
        x = 0
        y = 0

        if not con_inicial:
            if modo < 3:
                print("%s PRESIONE ENTER PARA SACAR:" % self.nombre)
                input()
                x = randrange(1, 7)
                y = randrange(1, 7)
                print("SACO %d %d\n" % (x, y))
            else:
                inp = ""
                texto_ingresado = ""
                while inp == "":
                    inp = texto_ingresado
                x = randrange(1, 7)
                y = randrange(1, 7)
        else:
            texto_ingresado = "7"
            lis = []
            while x <= 0 or x > 6 or y <= 0 or y > 6:
                if modo < 3:
                    print("%s DIGITE EL VALOR DE LOS DADOS " % self.nombre)
                    lis = input().split()
                else:
                    lis = texto_ingresado.split()
                try:
                    x, y = tuple(map(int, lis))
                except:
                    x = 0
                    y = 0

        return (x, y)

class espacio(object):

    def __init__(self, numeroEspacio, etiqueta, x, y, tipoEspacio="normal", colorCasillaEspecial="ninguno",
                 orientacion="Ninguna"):

        self.colorCasillaEspecial = colorCasillaEspecial
        self.tipoEspacio = tipoEspacio
        self.numeroEspacio = numeroEspacio
        self.etiqueta = etiqueta
        self.orientacion = orientacion
        self.NoFichas = 0
        self.PosFicha = ""
        self.x = x
        self.y = y

class ficha:  # Declara la clase ficha

    def __init__(self, nombreFicha, colorFicha, espacioActual, estadoJuego="inicio"):

        global modo
        self.colorFicha = colorFicha
        self.espacioActual = espacioActual
        self.estadoJuego = estadoJuego
        self.nombreFicha = nombreFicha
        self.espacioActual = espacioActual

        # Inicializar la posición de la ficha
        if self.espacioActual.NoFichas == 0:
            self.xI = self.espacioActual.x + 40
            self.yI = self.espacioActual.y + 40
        elif self.espacioActual.NoFichas == 1:
            self.xI = self.espacioActual.x + 80
            self.yI = self.espacioActual.y + 40
        elif self.espacioActual.NoFichas == 2:
            self.xI = self.espacioActual.x + 40
            self.yI = self.espacioActual.y + 80
        elif self.espacioActual.NoFichas == 3:
            self.xI = self.espacioActual.x + 80
            self.yI = self.espacioActual.y + 80

        self.espacioActual.NoFichas += 1
        self.PosFicha = ""

    def imprimirPropiedades(self):

        return "FICHA %s: COLOR= %s ESPACIO=%s ESTADO=%s" % (
            self.nombreFicha, self.colorFicha, self.espacioActual.numeroEspacio, self.estadoJuego)

    def cambiarPosicion(self, NuevoEspacio):

        global modo
        self.espacioActual.NoFichas -= 1
        self.espacioActual = NuevoEspacio
        NuevoEspacio.NoFichas += 1

    def num(self):
        return self.nombreFicha

def CrearTablero():

    global modo
    tablero = []

    for x in range(68):
        orientacion = "" #PARA EL MODO GRÁFICO
        xF = 0
        yF = 0

        if modo > 1:
            if x + 1 in [y1 for y1 in range(1, 9)]:
                orientacion = "vertical"
                z = x
                xF = z * 18 + 252
                yF = 254
            elif x + 1 in [y1 for y1 in range(9, 17)]:
                orientacion = "horizontal"
                z = x - 8
                xF = 396
                yF = z * 18 + 308
            elif x + 1 == 17:
                orientacion = "horizontal"
                xF = 448
                yF = 432
            elif x + 1 in [y1 for y1 in range(18, 26)]:
                orientacion = "horizontal"
                z = x - 17
                xF = 504
                yF = 434 - z * 18
            elif x + 1 in [y1 for y1 in range(26, 34)]:
                orientacion = "vertical"
                z = x - 25
                xF = z * 18 + 558
                yF = 254
            elif x + 1 == 34:
                orientacion = "vertical"
                xF = 684
                yF = 200
            elif x + 1 in [y1 for y1 in range(35, 43)]:
                orientacion = "vertical"
                z = x - 34
                xF = 684 - z * 18
                yF = 146
            elif x + 1 in [y1 for y1 in range(43, 51)]:
                orientacion = "horizontal"
                z = x - 42
                xF = 504
                yF = 128 - z * 18
            elif x + 1 == 51:
                orientacion = "horizontal"
                xF = 448
                yF = 2
            elif x + 1 in [y1 for y1 in range(52, 60)]:
                orientacion = "horizontal"
                z = x - 51
                xF = 396
                yF = z * 18 + 2
            elif x + 1 in [y1 for y1 in range(60, 68)]:
                orientacion = "vertical"
                z = x - 59
                xF = 378 - z * 18
                yF = 146
            elif x + 1 == 68:
                orientacion = "vertical"
                xF = 252
                yF = 200

        if x + 1 in [5, 22, 39, 56]:
            NuevaCasilla = espacio(x + 1, None, xF, yF, "salida", "ninguno", orientacion)
        elif x + 1 in [12, 17, 29, 34, 46, 51, 63, 68]:
            NuevaCasilla = espacio(x + 1, None, xF, yF, "seguro", "ninguno", orientacion)
        else:
            NuevaCasilla = espacio(x + 1, None, xF, yF, 'normal', "ninguno", orientacion)

        tablero.append(NuevaCasilla)

    tablero.append(espacio(69, None, 255, 311, "inicio", "rojo"))
    tablero.append(espacio(70, None, 561, 311, "inicio", "verde"))
    tablero.append(espacio(71, None, 561, 5, "inicio", "amarillo"))
    tablero.append(espacio(72, None, 255, 5, "inicio", "azul"))

    for x in range(28):
        if x < 7:
            z = x
            NuevaCasilla = espacio(72 + x + 1, None, z * 18 + 270, 200, "especial", "rojo", "vertical")
        elif x < 14:
            z = x - 7
            NuevaCasilla = espacio(72 + x + 1, None, 450, 416 - z * 18, "especial", "verde", "horizontal")
        elif x < 21:
            z = x - 14
            NuevaCasilla = espacio(72 + x + 1, None, 666 - z * 18, 200, "especial", "amarillo", "vertical")
        else:
            z = x - 21
            NuevaCasilla = espacio(72 + x + 1, None, 450, z * 18 + 20, "especial", "azul", "horizontal")

        tablero.append(NuevaCasilla)

    tablero.append(espacio(101, None, 399, 149, "llegada"))
    return tablero

def CrearJugadoresYFichas(tablero, numeroJugadores, nombres):

    jugadores = []
    for x in range(numeroJugadores):  # Itera en el número de jugadores que hayan ingresado
        fichas = []
        if x == 0:  # Si x es 0, sera el primer jugador, y por ende fichas rojas
            """
            68-> Rojo
            69-> Verde
            70-> Amarillo
            71-> Azul
            """
            for z in range(4):  # Crea las 4 fichas rojas
                NuevaFicha = ficha("rojo%d" % (z + 1), "rojo",
                                   tablero[68])  # Le asigna el número de ficha con su posición
                fichas.append(NuevaFicha)  # Lo agrega en una lista de fichas
            jugadores.append(jugador(nombres[0], "rojo", fichas))  # Crea un objeto jugador y lo agrega a una lista
            jugadores[0].UltimaFicha = jugadores[0].fichas[3]
        elif x == 1:
            for z in range(4):
                NuevaFicha = ficha("verde%d" % (z + 1), "verde", tablero[69])
                fichas.append(NuevaFicha)
            jugadores.append(jugador(nombres[1], "verde", fichas))
            jugadores[1].UltimaFicha = jugadores[1].fichas[3]
        elif x == 2:
            for z in range(4):
                NuevaFicha = ficha("amarillo%d" % (z + 1), "amarillo", tablero[70])
                fichas.append(NuevaFicha)
            jugadores.append(jugador(nombres[2], "amarillo", fichas))
            jugadores[2].UltimaFicha = jugadores[2].fichas[3]
        elif x == 3:
            for z in range(4):
                NuevaFicha = ficha("azul%d" % (z + 1), "azul", tablero[71])
                fichas.append(NuevaFicha)
            jugadores.append(jugador(nombres[3], "azul", fichas))
            jugadores[3].UltimaFicha = jugadores[3].fichas[3]

    return jugadores


def pedirDatos():

    global modo, texto_ingresado
    texto_ingresado = ""
    n = 0

    while (n <= 0 or n > 4):
        if modo < 3:
            print("INGRESE EL NÚMERO DE JUGADORES:")
            n = input()
        else:
            n = texto_ingresado
        try:
            n = int(n)
        except:
            n = 0

    nombres = []

    for z in range(n):
        color = ""
        if (z == 0): color = "#ED0D0D"
        if (z == 1): color = "#04B112"
        if (z == 2): color = "#ECC811"
        if (z == 3): color = "#2926DA"

        if modo < 3:
            print("INGRESE EL NOMBRE DEL JUGADOR %d" % (z + 1))
            nombre = ""
        else:
            print("INGRESE EL NOMBRE DEL JUGADOR %d" % (z + 1))

        nombre = ""
        texto_ingresado = ""
        while (len(nombre) <= 0 or len(nombre) > 10):
            if modo < 3:
                nombre = input()
            else:
                nombre = texto_ingresado

        nombres.append(nombre)

    x = ""
    if modo == 3:
        print("PRESIONE CONTINUAR:")
        texto_ingresado = ""
        while x == "":
            x = texto_ingresado
    else:
        print("ENTER PARA CONTINUAR EL JUEGO :")
        x = input()

    return nombres

def ObtenerMayor(listaJugadores):

    arreglo = []
    for i in range(len(listaJugadores)):
        arreglo.append(listaJugadores[i].valor)
    return max(arreglo)

def OrdenDeJuego(ListaJugadores, modoDesarrollador=False):

    global con_inicial, modo
    aux = ListaJugadores[:]
    while (len(aux) != 1):
        for x in aux:
            x.valor = x.TirarUnDado(con_inicial)
        aux2 = []
        for x in aux:
            if not (x.valor != ObtenerMayor(aux)):
                aux2.append(x)
        aux = aux2
    if modo < 3:
        print(aux[0].nombre + " EMPEZARÁ EL JUEGO")

    return ListaJugadores.index(aux[0])

def GameOver(Jugadores):

    numberWonPlayers = 0
    for jugadorActual in Jugadores:
        if jugadorActual.GanoJugador:
            numberWonPlayers += 1
    if (numberWonPlayers == len(Jugadores) - 1 and len(Jugadores) > 1) or (
            numberWonPlayers == 1 and len(Jugadores) == 1):
        global POSICION
        jugadorFaltante = [jug for jug in Jugadores if not jug.GanoJugador]
        if not len(jugadorFaltante) == 0:
            jugadorFaltante[0].Posicion = POSICION
        return True
    return False

def posiblesMovimientos(JugadorActual, resultadoDado, ListaJugadores):

    listaPosiblesMovimientos = []
    listaCasillasCarcel = [69, 70, 71, 72]
    numeros = {}
    numeros2 = {}

    for jugador in ListaJugadores:
        for ficha in jugador.fichas:
            casillaActual = ficha.espacioActual.numeroEspacio
            if casillaActual in numeros and not casillaActual in listaCasillasCarcel:
                numeros[casillaActual][1] += 1
                if numeros[casillaActual][0].colorFicha != ficha.colorFicha and casillaActual in [5, 22, 39, 56]:
                    numeros2[casillaActual] = [numeros[casillaActual][0], ficha]
            elif not casillaActual in listaCasillasCarcel:
                numeros[casillaActual] = [ficha, 1]

    listaBloqueos = [item for item, valor in numeros.items() if valor[1] == 2]
    listaConUnaFicha = [(item, valor[0]) for item, valor in numeros.items() if valor[1] == 1]
    tuplaCasillasUnaFicha = tuple([valor for valor, ficha in listaConUnaFicha])
    dat = {"rojo": 5, "verde": 22, "amarillo": 39, "azul": 56}
    diccionarioSeguros = {"rojo": 68, "verde": 17, "amarillo": 34, "azul": 51}
    diccionarioPrimeraEspecial = {"rojo": 73, "verde": 80, "amarillo": 87, "azul": 94}

    numeroSeguroSalida = diccionarioSeguros[JugadorActual.color]
    numeroPrimeraEspecial = diccionarioPrimeraEspecial[JugadorActual.color]
    numeroDiccionarioSeguros = diccionarioSeguros[JugadorActual.color]

    colorJugador = JugadorActual.color

    for fichaActual in JugadorActual.fichas:
        bloqueo = False
        casillaFicha = fichaActual.espacioActual.numeroEspacio
        nombreFicha = fichaActual.nombreFicha
        posicionFinal = casillaFicha + resultadoDado

        if casillaFicha in listaCasillasCarcel and resultadoDado != 5:
            continue
        if casillaFicha in listaCasillasCarcel and resultadoDado == 5:
            if not (dat[colorJugador] in listaBloqueos and not dat[colorJugador] in numeros2):
                if (dat[colorJugador] in tuplaCasillasUnaFicha and numeros[dat[colorJugador]][0].colorFicha != fichaActual.colorFicha):
                    return [(nombreFicha + " sale de la carcel a la casilla: %d. Captura a %s." % (
                        dat[colorJugador], numeros[dat[colorJugador]][0].nombreFicha), fichaActual,
                             numeros[dat[colorJugador]][0])]
                elif dat[colorJugador] in numeros2:
                    if numeros2[dat[colorJugador]][0].colorFicha != fichaActual.colorFicha and \
                            numeros2[dat[colorJugador]][1].colorFicha == fichaActual.colorFicha:
                        return [(nombreFicha + " sale de la carcel a la casilla: %d. Captura a %s." % (
                            dat[colorJugador], numeros2[dat[colorJugador]][0].nombreFicha), fichaActual,
                                  numeros2[dat[colorJugador]][0])]
                    elif numeros2[dat[colorJugador]][1].colorFicha != fichaActual.colorFicha and \
                            numeros2[dat[colorJugador]][0].colorFicha == fichaActual.colorFicha:
                        return [(nombreFicha + " sale de la carcel a la casilla: %d. Captura a %s." % (
                            dat[colorJugador], numeros2[dat[colorJugador]][1].nombreFicha), fichaActual,
                                  numeros2[dat[colorJugador]][1])]
                    else:
                        continue
                else:
                    return [(nombreFicha + " sale de la carcel a la casilla: %d." % dat[colorJugador], fichaActual)]
            else:
                continue
        else:
            for x in range(casillaFicha + 1, posicionFinal + 1):
                if (casillaFicha <= numeroSeguroSalida and x > numeroSeguroSalida) or (
                        colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and x > 85):
                    if (colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and x > 85):
                        if x % 68 + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 in listaBloqueos:
                            bloqueo = True
                            break
                        elif x % 68 + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 > numeroPrimeraEspecial + 7:
                            bloqueo = True
                            break
                    else:
                        if x + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 in listaBloqueos:
                            bloqueo = True
                            break
                        elif x + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 > numeroPrimeraEspecial + 7:
                            bloqueo = True
                            break
                elif casillaFicha <= 68 and x <= 68 and x in listaBloqueos:
                    bloqueo = True
                    break
                elif x % 68 in listaBloqueos:
                    bloqueo = True
                    break
                elif x in listaBloqueos or x > numeroPrimeraEspecial + 7:
                    bloqueo = True
                    break

        CasillaEspecial = 0
        ListaCasillasSeguro = (12, 17, 29, 34, 46, 51, 63, 68)
        ListaCasillasSalida = (5, 22, 39, 56)
        if (casillaFicha <= numeroSeguroSalida and posicionFinal > numeroSeguroSalida) or (
                colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and posicionFinal > 85):
            if (colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and posicionFinal > 85):
                CasillaEspecial = posicionFinal % 68 + (numeroPrimeraEspecial - numeroSeguroSalida - 1)
            else:
                CasillaEspecial = posicionFinal + (numeroPrimeraEspecial - numeroSeguroSalida - 1)
            if CasillaEspecial == numeroPrimeraEspecial + 7:
                CasillaEspecial = 101

        if not bloqueo:
            if CasillaEspecial == 101 or posicionFinal == numeroPrimeraEspecial + 7:
                textoRespuesta = '{} corona'.format(nombreFicha)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal <= 68 and posicionFinal in tuplaCasillasUnaFicha and CasillaEspecial == 0:
                fichaCapturada = numeros[posicionFinal][0]
                if fichaCapturada.colorFicha != colorJugador and not posicionFinal in ListaCasillasSeguro and not posicionFinal in ListaCasillasSalida:
                    textoRespuesta = '{} captura a {} en casilla {}'.format(nombreFicha, fichaCapturada.nombreFicha,
                                                                            posicionFinal)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual, fichaCapturada))
                else:
                    textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal > 68 and (posicionFinal % 68 in tuplaCasillasUnaFicha) and CasillaEspecial == 0 and casillaFicha <= 68:
                fichaCapturada_2 = numeros[posicionFinal % 68][0]
                if fichaCapturada_2.colorFicha != colorJugador and not posicionFinal % 68 in ListaCasillasSeguro and not posicionFinal % 68 in ListaCasillasSalida:
                    textoRespuesta = '{} captura a {} en casilla {}'.format(nombreFicha, fichaCapturada_2.nombreFicha,
                                                                            posicionFinal % 68)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual, fichaCapturada_2))
                else:
                    textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal % 68)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif CasillaEspecial != 0:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, CasillaEspecial)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal <= 68:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal > 68 and casillaFicha > 68:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal > 68:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal % 68)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

    if len(listaPosiblesMovimientos) == 0:
        return None
    return listaPosiblesMovimientos

def realizarMovimiento(movimientoRealizar, tablero, jugadorActual, Jugadores):

    if movimientoRealizar is None:
        return

    FichaCapturada = None
    listaCasillasCarcel = {'rojo': 69, 'verde': 70, 'amarillo': 71, 'azul': 72}
    listaCasillasSalida = {'rojo': 5, 'verde': 22, 'amarillo': 39, 'azul': 56}
    FichaMover = movimientoRealizar[1]
    descripcionMovimiento = movimientoRealizar[0]

    if len(movimientoRealizar) == 3:
        FichaCapturada = movimientoRealizar[2]

    if 'sale' in descripcionMovimiento:
        if "Captura" in descripcionMovimiento:
            FichaCapturada = movimientoRealizar[2]
            FichaCapturada.estadoJuego = "inicio"
            casillaCarcel = listaCasillasCarcel[FichaCapturada.colorFicha]
            FichaCapturada.cambiarPosicion(tablero[casillaCarcel - 1])
            FichaMover.cambiarPosicion(tablero[listaCasillasSalida[FichaMover.colorFicha] - 1])
            FichaMover.estadoJuego = "activo"
            listaMovi = posiblesMovimientos(jugadorActual, 20, Jugadores)
            if listaMovi and len(listaMovi) == 1:
                realizarMovimiento(listaMovi[0], tablero, jugadorActual, Jugadores)
            elif listaMovi and len(listaMovi) > 1:
                realizarMovimiento(opciones(listaMovi, jugadorActual), tablero, jugadorActual, Jugadores)
        else:
            FichaMover.cambiarPosicion(tablero[listaCasillasSalida[FichaMover.colorFicha] - 1])
            FichaMover.estadoJuego = "activo"

    elif 'captura' in descripcionMovimiento:
        posicionFinal = int(descripcionMovimiento.split()[-1])
        casillaCarcel = listaCasillasCarcel[FichaCapturada.colorFicha]
        FichaCapturada.cambiarPosicion(tablero[casillaCarcel - 1])  # Cambia de posición
        FichaCapturada.estadoJuego = "inicio"
        FichaMover.cambiarPosicion(tablero[posicionFinal - 1])
        listaMovi = posiblesMovimientos(jugadorActual, 20, Jugadores)
        if listaMovi and len(listaMovi) == 1:
            realizarMovimiento(listaMovi[0], tablero, jugadorActual, Jugadores)
        elif listaMovi and len(listaMovi) > 1:
            realizarMovimiento(opciones(listaMovi, jugadorActual), tablero, jugadorActual, Jugadores)

    elif 'mueve' in descripcionMovimiento:
        posicionFinal = int(descripcionMovimiento.split()[-1])
        FichaMover.cambiarPosicion(tablero[posicionFinal - 1])  # Cambia posición de la ficha

    elif 'corona' in descripcionMovimiento:
        jugadorActual.fichas.remove(FichaMover)
        if len(jugadorActual.fichas) == 0:
            global POSICION
            jugadorActual.Posicion = POSICION
            POSICION += 1
            jugadorActual.GanoJugador = True
        listaMovi = posiblesMovimientos(jugadorActual, 10, Jugadores)
        if listaMovi and len(listaMovi) == 1:
            realizarMovimiento(listaMovi[0], tablero, jugadorActual, Jugadores)
        elif listaMovi and len(listaMovi) > 1:
            realizarMovimiento(opciones(listaMovi, jugadorActual), tablero, jugadorActual, Jugadores)
        return

    jugadorActual.DefinirUltimaFicha(jugadorActual, FichaMover)

def imprimirEstado(Jugador):
    for ficha in Jugador.fichas:
        print(ficha.imprimirPropiedades())

def opciones(Lista, JugadorActual):
    eleccion = 0
    global modo, seleccion
    seleccion = False

    if modo == 3:
        options = [opcion[0] for opcion in Lista]
        print("%s SELECCIONA Y OPRIME ENTER." % JugadorActual.nombre)
        for index, option in enumerate(options, start=1):
            print(f'{index} -> {option}')
        print("SELECCIONA UNA OPCION:")

        while not seleccion:
            eleccion = input()
            escribir(eleccion)
            try:
                eleccion = int(eleccion)
                if 1 <= eleccion <= len(options):
                    seleccion = True
                else:
                    print("INGRESE UNA OPCIÓN VÁLIDA.")
            except ValueError:
                print("INGRESE UNA OPCIÓN VÁLIDA.")

    if modo < 3:
        while eleccion <= 0 or eleccion > len(Lista):
            x = 1
            for opcion in Lista:
                print(f'{x} -> {opcion[0]}')
                x += 1
            print(f'{x} -> POSICIÓN Y ESTADO DE LAS FICHAS')
            eleccion = input()
            escribir(eleccion)
            try:
                eleccion = int(eleccion)
            except ValueError:
                eleccion = 0
            if eleccion == len(Lista) + 1:
                imprimirEstado(JugadorActual)

    return Lista[eleccion - 1]

def IniciarJuego():

    global con_inicial, modo
    if modo > 1:
        # Se eliminan las referencias gráficas
        pass

    nom = tuple(pedirDatos())  # Retorna una tupla con los nombres de los jugadores

    Tablero = CrearTablero()  # Se crea el tablero
    Jugadores = CrearJugadoresYFichas(Tablero, len(nom), nom)  # Retorna la lista de objetos jugador 'Jugadores'
    indicePrimerJugador = OrdenDeJuego(Jugadores)

    while not GameOver(Jugadores):
        repetirLanzamiento = True
        contadorParesSeguidos = 0  # contador de 3 seguidos
        jugadorActual = Jugadores[indicePrimerJugador % len(Jugadores)]
        if jugadorActual.GanoJugador:
            continue

        while repetirLanzamiento:
            resultadoDado1, resultadoDado2 = jugadorActual.TirarDosDados(con_inicial)
            if resultadoDado1 == resultadoDado2:
                repetirLanzamiento = True
                contadorParesSeguidos += 1
                if contadorParesSeguidos == 3:
                    listaCasillasCarcel = {'rojo': 69, 'verde': 70, 'amarillo': 71, 'azul': 72}
                    UltimaFichaJugador = jugadorActual.UltimaFicha  # Invocamos la última ficha del jugador actual
                    nombreFicha = UltimaFichaJugador.nombreFicha  # Invocamos su nombre
                    posicionFinal = listaCasillasCarcel[UltimaFichaJugador.colorFicha]  # Posición en la cárcel
                    realizarMovimiento(['{} mueve a casilla {}'.format(nombreFicha, posicionFinal), UltimaFichaJugador],
                                       Tablero, jugadorActual, Jugadores)
                    UltimaFichaJugador.estadoJuego = 'inicio'
                    repetirLanzamiento = False
                    contadorParesSeguidos = 0
                    imprimirEstado(jugadorActual)
                    continue
            else:
                contadorParesSeguidos = 0
                repetirLanzamiento = False

            if resultadoDado1 + resultadoDado2 == 5:
                ListaMovi = posiblesMovimientos(jugadorActual, 5, Jugadores)
                if ListaMovi and len(ListaMovi) == 1 and "sale" in ListaMovi[0][0]:
                    realizarMovimiento(ListaMovi[0], Tablero, jugadorActual, Jugadores)
                    continue

            ListaMovi1 = posiblesMovimientos(jugadorActual, resultadoDado1, Jugadores)
            ListaMovi2 = posiblesMovimientos(jugadorActual, resultadoDado2, Jugadores)
            ListaMoviF = ""

            if ListaMovi1 and 'sale' in ListaMovi1[0][0]:
                realizarMovimiento(ListaMovi1[0], Tablero, jugadorActual, Jugadores)
                ListaMovi2 = posiblesMovimientos(jugadorActual, resultadoDado2, Jugadores)
                ListaMoviF = ListaMovi2
            elif ListaMovi2 and "sale" in ListaMovi2[0][0]:
                realizarMovimiento(ListaMovi2[0], Tablero, jugadorActual, Jugadores)
                ListaMovi1 = posiblesMovimientos(jugadorActual, resultadoDado1, Jugadores)
                ListaMoviF = ListaMovi1

            if type(ListaMoviF) != list:
                if ListaMovi1 and ListaMovi2:
                    global dadoSeleccionado
                    dadoSeleccionado = 0
                    if modo < 3:
                        while dadoSeleccionado <= 0 or dadoSeleccionado > 2:
                            print("Qué dado desea mover (?) :\n1. %d\n2. %d" % (resultadoDado1, resultadoDado2))
                            dadoSeleccionado = input()
                            try:
                                dadoSeleccionado = int(dadoSeleccionado)
                            except:
                                dadoSeleccionado = 0
                    for x in range(2):
                        if dadoSeleccionado == 1 and not ListaMovi1:
                            continue
                        elif dadoSeleccionado == 2 and not ListaMovi2:
                            continue
                        elif dadoSeleccionado == 1 and len(ListaMovi1) == 1:
                            realizarMovimiento(ListaMovi1[0], Tablero, jugadorActual, Jugadores)
                            ListaMovi2 = posiblesMovimientos(jugadorActual, resultadoDado2, Jugadores)
                            dadoSeleccionado = 2
                        elif dadoSeleccionado == 1 and len(ListaMovi1) > 1:
                            realizarMovimiento(opciones(ListaMovi1, jugadorActual), Tablero, jugadorActual, Jugadores)
                            ListaMovi2 = posiblesMovimientos(jugadorActual, resultadoDado2, Jugadores)
                            dadoSeleccionado = 2
                        elif dadoSeleccionado == 2 and len(ListaMovi2) == 1:
                            realizarMovimiento(ListaMovi2[0], Tablero, jugadorActual, Jugadores)
                            ListaMovi1 = posiblesMovimientos(jugadorActual, resultadoDado1, Jugadores)
                            dadoSeleccionado = 1
                        elif dadoSeleccionado == 2 and len(ListaMovi2) > 1:
                            realizarMovimiento(opciones(ListaMovi2, jugadorActual), Tablero, jugadorActual, Jugadores)
                            ListaMovi1 = posiblesMovimientos(jugadorActual, resultadoDado1, Jugadores)
                            dadoSeleccionado = 1
                    imprimirEstado(jugadorActual)
                elif ListaMovi1:
                    if len(ListaMovi1) == 1:
                        realizarMovimiento(ListaMovi1[0], Tablero, jugadorActual, Jugadores)
                        imprimirEstado(jugadorActual)
                    else:
                        realizarMovimiento(opciones(ListaMovi1, jugadorActual), Tablero, jugadorActual, Jugadores)
                        imprimirEstado(jugadorActual)
                elif ListaMovi2:
                    if len(ListaMovi2) == 1:
                        realizarMovimiento(ListaMovi2[0], Tablero, jugadorActual, Jugadores)
                    else:
                        realizarMovimiento(opciones(ListaMovi2, jugadorActual), Tablero, jugadorActual, Jugadores)
            elif ListaMoviF and len(ListaMoviF) == 1:
                realizarMovimiento(ListaMoviF[0], Tablero, jugadorActual, Jugadores)
                imprimirEstado(jugadorActual)
            elif ListaMoviF and len(ListaMoviF) > 1:
                realizarMovimiento(opciones(ListaMoviF, jugadorActual), Tablero, jugadorActual, Jugadores)
                imprimirEstado(jugadorActual)

        indicePrimerJugador += 1

    Jugadores.sort(key=lambda x: x.Posicion)
    for x in Jugadores:
        print(x.nombre + " terminó en posición: %d" % x.Posicion)

ele = 0
while (ele <=  0 or ele > 3):
    print("________PARCHIS:__________\nPresione 1 Para Continuar")
    ele = input()
    try:
        ele = int(ele)
    except:
        ele = 0

modo = ele
if modo > 1:

    pass
else:
    IniciarJuego()
