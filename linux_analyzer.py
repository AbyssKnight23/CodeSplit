def detectar_bits_linux(data):

    if data[0:4] != b'\x7fELF':
        return "No es ELF"

    clase = data[4]

    if clase == 1:
        return "32 bits ELF"

    elif clase == 2:
        return "64 bits ELF"

    return "ELF desconocido"