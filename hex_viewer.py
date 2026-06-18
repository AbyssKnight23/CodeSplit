def mostrar_hex(data, limite=512):

    resultado = ""

    # Recorremos el archivo de 16 bytes en 16
    for i in range(0, min(len(data), limite), 16):

        chunk = data[i:i+16]  # Cogemos bloque de 16 bytes

        # Convertimos a HEX
        hex_values = " ".join(f"{b:02X}" for b in chunk)

        # Convertimos a ASCII (para verlo mas claro)
        ascii_values = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)

        # Formato tipo visor hexadecimal
        resultado += f"{i:08X}  {hex_values:<48}  {ascii_values}\n"

    return resultado