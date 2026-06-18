# ---------- OBTENER SECCION .TEXT ----------

def obtener_text_section(data):

    # Comprobamos tamaño minimo
    if len(data) < 64:
        return None

    # Verificamos que sea ejecutable PE
    if data[0:2] != b'MZ':
        return None

    # ---------- BUSCAR CABECERA PE ----------

    # Offset donde empieza PE
    pe_offset = int.from_bytes(data[60:64], "little")

    # Comprobamos firma PE
    if data[pe_offset:pe_offset+4] != b'PE\x00\x00':
        return None

    # ---------- LEER NUMERO DE SECCIONES ----------

    num_sections = int.from_bytes(data[pe_offset+6:pe_offset+8], "little")

    # Tamaño del Optional Header
    optional_header_size = int.from_bytes(data[pe_offset+20:pe_offset+22], "little")

    # ---------- IR A TABLA DE SECCIONES ----------

    section_table_offset = pe_offset + 24 + optional_header_size

    # ---------- RECORRER SECCIONES ----------

    for i in range(num_sections):

        # Cada entrada ocupa 40 bytes
        section_offset = section_table_offset + (i * 40)

        # Nombre de la seccion (8 bytes)
        name = data[section_offset:section_offset+8]

        # Convertimos a texto
        name = name.decode(errors="ignore").strip('\x00')

        # ---------- SI ES .text ----------

        if name == ".text":

            # Tamaño en memoria
            size = int.from_bytes(data[section_offset+16:section_offset+20], "little")

            # Offset en el archivo
            raw_ptr = int.from_bytes(data[section_offset+20:section_offset+24], "little")

            # Devolvemos los bytes de la seccion
            return data[raw_ptr:raw_ptr+size]

    # Si no encuentra la seccion
    return None