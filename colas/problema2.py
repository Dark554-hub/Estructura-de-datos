from cola import Cola

SERVICIOS = {
    1: "Siniestros",
    2: "Pólizas",
    3: "Pagos",
    4: "Atención general",
}

colas = {num: Cola() for num in SERVICIOS}
contadores = {num: 0 for num in SERVICIOS}


def llegada_cliente(servicio):
    contadores[servicio] += 1
    numero = f"S{servicio}-{contadores[servicio]:03d}"
    colas[servicio].encolar(numero)
    print(f"Su número de atención es: {numero} ({SERVICIOS[servicio]}). "
          f"Clientes en espera: {colas[servicio].tamano()}")


def atender_cliente(servicio):
    if colas[servicio].esta_vacia():
        print(f"No hay clientes en espera en {SERVICIOS[servicio]}.")
    else:
        numero = colas[servicio].desencolar()
        print(f">>> Llamando al número {numero} ({SERVICIOS[servicio]})")


def main():
    print("Servicios disponibles:")
    for num, nombre in SERVICIOS.items():
        print(f"  {num}. {nombre}")
    print("\nComandos: C<n> = llega cliente | A<n> = atender | S = salir\n")

    while True:
        entrada = input("> ").strip().upper()

        if entrada == "S":
            print("Sistema cerrado.")
            break

        if len(entrada) < 2 or entrada[0] not in ("C", "A") or not entrada[1:].isdigit():
            print("Comando inválido. Ejemplo: C1 o A2")
            continue

        servicio = int(entrada[1:])
        if servicio not in SERVICIOS:
            print("Servicio inexistente.")
            continue

        if entrada[0] == "C":
            llegada_cliente(servicio)
        else:
            atender_cliente(servicio)


if __name__ == "__main__":
    main()