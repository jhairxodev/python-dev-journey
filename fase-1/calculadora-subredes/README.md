# Calculadora de subredes

Programa de terminal que recibe una red IPv4 en notación CIDR (como `192.168.10.0/26`) y calcula su máscara, broadcast, hosts útiles y el rango de IPs que se pueden asignar.

Es el proyecto de la semana 1 de mi ruta [python-dev-journey](../../README.md).

## Cómo se usa

Necesita Python 3.10 o superior. No usa librerías externas: solo `ipaddress`, que ya viene con Python.

```bash
python3 subredes.py
```

## Ejemplo

```text
$ python3 subredes.py
Introduzca la red (ejemplo: 192.168.10.0/26): 192.168.10.0/26

Red:          192.168.10.0/26
Máscara:      255.255.255.192
Broadcast:    192.168.10.63
Hosts útiles: 62
Primer host:  192.168.10.1
Último host:  192.168.10.62
```

Con una entrada que no es red:

```text
$ python3 subredes.py
Introduzca la red (ejemplo: 192.168.10.0/26): hola
"hola" no es una red válida. Ejemplo: 192.168.10.0/26
```

## Casos raros que probé

| Entrada | Qué responde | Por qué |
|---|---|---|
| `192.168.10.0/24` | 254 hosts útiles | 256 direcciones menos la de red y la de broadcast |
| `192.168.10.0/30` | 2 hosts útiles | La red más chica para un enlace normal |
| `10.0.0.0/31` | 2 hosts útiles: `10.0.0.0` y `10.0.0.1` | En enlaces punto a punto (RFC 3021) no se reservan red ni broadcast |
| `10.0.0.5/32` | 1 host: `10.0.0.5` | Una sola dirección |
| `192.168.10.0` | La toma como `/32` | Sin prefijo, `ipaddress` asume una sola IP |
| `192.168.10.5/26` | Calcula la red `192.168.10.0/26` | Con `strict=False` acepta una IP de equipo y saca su red |
| `10.0.0.0/8` | 16,777,214 hosts, al instante | Se calcula con aritmética, sin crear la lista de IPs |
| `300.1.1.1/24`, `hola` o vacío | Mensaje de red no válida | El `ValueError` se atrapa y no truena |
| `2001:db8::/64` | Mensaje de red no válida | Solo acepta IPv4 |

## Cómo está hecho

- `leer_red(texto)` valida el texto y regresa la red, o `None` si no es una red IPv4.
- `calcular_subred(red)` es una función pura: recibe la red y regresa un diccionario, sin `input()` ni `print()`.
- `main()` es lo único que habla con el usuario.

## Lo que aprendí

- **Para contar no hace falta crear la lista.** Mi primera versión usaba `list(red.hosts())`: con una `/8` tardaba unos 12 segundos y usaba casi 2 GB de RAM, y con una red IPv6 grande se colgaba. Ahora calcula con `num_addresses`, `network_address + 1` y `broadcast_address - 1`, y responde al instante con cualquier tamaño.
- **Un type hint es una promesa, no un candado.** `ip_network()` aceptaba IPv6 aunque mi función dijera que regresaba `IPv4Network`. Usar `IPv4Network()` directamente cierra ese hueco.
- **Atrapar la excepción concreta.** `except ValueError` en lugar de un `except` que se trague cualquier error.
