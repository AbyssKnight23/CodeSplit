def detectar_bits(data):

    # Comprobamos tamaño minimo
    if len(data) < 64:
        return "Archivo demasiado pequeño"

    # Verificamos que sea ejecutable PE
    if data[0:2] != b'MZ':
        return "No es ejecutable PE"

    # Offset donde empieza la cabecera PE
    pe_offset = int.from_bytes(data[60:64], "little")

    # Verificamos firma PE
    if data[pe_offset:pe_offset+4] != b'PE\x00\x00':
        return "PE inválido"

    # Leemos el campo Machine (arquitectura)
    machine = int.from_bytes(data[pe_offset+4:pe_offset+6], "little")

    # 32 bits
    if machine == 0x014c:
        return "32 bits (x86)"

    # 64 bits
    elif machine == 0x8664:
        return "64 bits (x64)"

    # Otro caso
    else:
        return "Arquitectura desconocida"