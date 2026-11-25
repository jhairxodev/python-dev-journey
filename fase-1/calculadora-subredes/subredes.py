import ipaddress


def leer_red(texto: str) -> ipaddress.IPv4Network | None:
    try:
        return ipaddress.IPv4Network(texto.strip(), strict=False)
    except ValueError:
        return None


def calcular_subred(red: ipaddress.IPv4Network) -> dict[str, str | int]:
    if red.prefixlen >= 31:  # /31 y /32: todas las direcciones son usables
        primer_host = red.network_address
        ultimo_host = red.broadcast_address
        hosts_utiles = red.num_addresses
    else:
        primer_host = red.network_address + 1
        ultimo_host = red.broadcast_address - 1
        hosts_utiles = red.num_addresses - 2
    return {
        "red": str(red),
        "mascara": str(red.netmask),
        "broadcast": str(red.broadcast_address),
        "hosts_utiles": hosts_utiles,
        "primer_host": str(primer_host),
        "ultimo_host": str(ultimo_host),
    }


def main() -> None:
    entrada = input("Introduzca la red (ejemplo: 192.168.10.0/26): ")
    red = leer_red(entrada)
    if red is None:
        print(f'"{entrada.strip()}" no es una red válida. Ejemplo: 192.168.10.0/26')
        return
    datos = calcular_subred(red)
    print()
    print(f"Red:          {datos['red']}")
    print(f"Máscara:      {datos['mascara']}")
    print(f"Broadcast:    {datos['broadcast']}")
    print(f"Hosts útiles: {datos['hosts_utiles']}")
    print(f"Primer host:  {datos['primer_host']}")
    print(f"Último host:  {datos['ultimo_host']}")


if __name__ == "__main__":
    main()
