# ---------- OBTENER SECCION .TEXT ELF ----------

def obtener_text_section_linux(data):

    # Verificar ELF
    if data[0:4] != b'\x7fELF':
        return None

    elf_class = data[4]

    # ==================================================
    # ELF64
    # ==================================================

    if elf_class == 2:

        shoff = int.from_bytes(
            data[40:48],
            "little"
        )

        shentsize = int.from_bytes(
            data[58:60],
            "little"
        )

        shnum = int.from_bytes(
            data[60:62],
            "little"
        )

        shstrndx = int.from_bytes(
            data[62:64],
            "little"
        )

        shstr_offset = shoff + (
            shstrndx * shentsize
        )

        strtab_ptr = int.from_bytes(
            data[shstr_offset+24:shstr_offset+32],
            "little"
        )

        strtab_size = int.from_bytes(
            data[shstr_offset+32:shstr_offset+40],
            "little"
        )

        strtab = data[
            strtab_ptr:strtab_ptr+strtab_size
        ]

        for i in range(shnum):

            section = shoff + (
                i * shentsize
            )

            name_offset = int.from_bytes(
                data[section:section+4],
                "little"
            )

            end = strtab.find(
                b'\x00',
                name_offset
            )

            name = strtab[
                name_offset:end
            ].decode(
                errors="ignore"
            )

            if name == ".text":

                offset = int.from_bytes(
                    data[section+24:section+32],
                    "little"
                )

                size = int.from_bytes(
                    data[section+32:section+40],
                    "little"
                )

                return data[
                    offset:offset+size
                ]

    # ==================================================
    # ELF32
    # ==================================================

    elif elf_class == 1:

        shoff = int.from_bytes(
            data[32:36],
            "little"
        )

        shentsize = int.from_bytes(
            data[46:48],
            "little"
        )

        shnum = int.from_bytes(
            data[48:50],
            "little"
        )

        shstrndx = int.from_bytes(
            data[50:52],
            "little"
        )

        shstr_offset = shoff + (
            shstrndx * shentsize
        )

        strtab_ptr = int.from_bytes(
            data[shstr_offset+16:shstr_offset+20],
            "little"
        )

        strtab_size = int.from_bytes(
            data[shstr_offset+20:shstr_offset+24],
            "little"
        )

        strtab = data[
            strtab_ptr:strtab_ptr+strtab_size
        ]

        for i in range(shnum):

            section = shoff + (
                i * shentsize
            )

            name_offset = int.from_bytes(
                data[section:section+4],
                "little"
            )

            end = strtab.find(
                b'\x00',
                name_offset
            )

            name = strtab[
                name_offset:end
            ].decode(
                errors="ignore"
            )

            if name == ".text":

                offset = int.from_bytes(
                    data[section+16:section+20],
                    "little"
                )

                size = int.from_bytes(
                    data[section+20:section+24],
                    "little"
                )

                return data[
                    offset:offset+size
                ]

    return None