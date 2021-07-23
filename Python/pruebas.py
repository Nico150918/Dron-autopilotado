while True:
    print("Modos de uso")
    print("1: Probar sensor de distancia")
    print("2: Enviar datos independientes")
    print("3: Iniciar vuelo desde fichero")
    print("Otro: Abandonar el sistema")
    mode = input("Selecciona el modo de uso:")
    print(int(mode))
    if int(mode) == 1:
        print("modo1")
    elif int(mode) == 2:
        print("mode2")
    elif int(mode) == 3:
        print("mode3")
    else:
        print("Salir")
        break
