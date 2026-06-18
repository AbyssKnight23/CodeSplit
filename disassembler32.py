# ---------- DESENSAMBLADOR 32 BITS ----------

def desensamblar32(data, limite=200):

    resultado = ""
    i = 0

    registros = [
        "EAX", "ECX", "EDX", "EBX",
        "ESP", "EBP", "ESI", "EDI"
    ]

    while i < min(len(data), limite):

        byte = data[i]

        # ------------------------------
        # NOP
        # ------------------------------

        if byte == 0x90:
            resultado += f"{i:08X}  NOP\n"
            i += 1

        # ------------------------------
        # RET
        # ------------------------------

        elif byte == 0xC3:
            resultado += f"{i:08X}  RET\n"
            i += 1

        # ------------------------------
        # INT
        # ------------------------------

        elif byte == 0xCD and i + 1 < len(data):

            resultado += (
                f"{i:08X}  INT {data[i+1]:02X}\n"
            )

            i += 2

        # ------------------------------
        # MOV REG, IMM32
        # B8-BF
        # ------------------------------

        elif 0xB8 <= byte <= 0xBF:

            reg = registros[byte - 0xB8]

            valor = int.from_bytes(
                data[i+1:i+5],
                "little"
            )

            resultado += (
                f"{i:08X}  MOV {reg}, {valor}\n"
            )

            i += 5

        # ------------------------------
        # PUSH IMM32
        # ------------------------------

        elif byte == 0x68:

            valor = int.from_bytes(
                data[i+1:i+5],
                "little"
            )

            resultado += (
                f"{i:08X}  PUSH {valor}\n"
            )

            i += 5

        # ------------------------------
        # PUSH REG
        # 50-57
        # ------------------------------

        elif 0x50 <= byte <= 0x57:

            reg = registros[byte - 0x50]

            resultado += (
                f"{i:08X}  PUSH {reg}\n"
            )

            i += 1

        # ------------------------------
        # POP REG
        # 58-5F
        # ------------------------------

        elif 0x58 <= byte <= 0x5F:

            reg = registros[byte - 0x58]

            resultado += (
                f"{i:08X}  POP {reg}\n"
            )

            i += 1

        # ------------------------------
        # INC REG
        # 40-47
        # ------------------------------

        elif 0x40 <= byte <= 0x47:

            reg = registros[byte - 0x40]

            resultado += (
                f"{i:08X}  INC {reg}\n"
            )

            i += 1

        # ------------------------------
        # DEC REG
        # 48-4F
        # ------------------------------

        elif 0x48 <= byte <= 0x4F:

            reg = registros[byte - 0x48]

            resultado += (
                f"{i:08X}  DEC {reg}\n"
            )

            i += 1

        # ------------------------------
        # ADD EAX, IMM32
        # ------------------------------

        elif byte == 0x05:

            valor = int.from_bytes(
                data[i+1:i+5],
                "little"
            )

            resultado += (
                f"{i:08X}  ADD EAX, {valor}\n"
            )

            i += 5

        # ------------------------------
        # SUB EAX, IMM32
        # ------------------------------

        elif byte == 0x2D:

            valor = int.from_bytes(
                data[i+1:i+5],
                "little"
            )

            resultado += (
                f"{i:08X}  SUB EAX, {valor}\n"
            )

            i += 5

        # ------------------------------
        # CMP EAX, IMM32
        # ------------------------------

        elif byte == 0x3D:

            valor = int.from_bytes(
                data[i+1:i+5],
                "little"
            )

            resultado += (
                f"{i:08X}  CMP EAX, {valor}\n"
            )

            i += 5

        # ------------------------------
        # XOR EAX,EAX
        # ------------------------------

        elif (
            byte == 0x31
            and i + 1 < len(data)
            and data[i+1] == 0xC0
        ):

            resultado += (
                f"{i:08X}  XOR EAX, EAX\n"
            )

            i += 2

        # ------------------------------
        # TEST EAX,EAX
        # ------------------------------

        elif (
            byte == 0x85
            and i + 1 < len(data)
            and data[i+1] == 0xC0
        ):

            resultado += (
                f"{i:08X}  TEST EAX, EAX\n"
            )

            i += 2

        # ------------------------------
        # CALL
        # ------------------------------

        elif byte == 0xE8:

            offset = int.from_bytes(
                data[i+1:i+5],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  CALL {offset}\n"
            )

            i += 5

        # ------------------------------
        # JMP
        # ------------------------------

        elif byte == 0xE9:

            offset = int.from_bytes(
                data[i+1:i+5],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JMP {offset}\n"
            )

            i += 5

        # ------------------------------
        # JMP SHORT
        # ------------------------------

        elif byte == 0xEB:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JMP SHORT {offset}\n"
            )

            i += 2

        # ------------------------------
        # JE
        # ------------------------------

        elif byte == 0x74:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JE {offset}\n"
            )

            i += 2

        # ------------------------------
        # JNE
        # ------------------------------

        elif byte == 0x75:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JNE {offset}\n"
            )

            i += 2

        # ------------------------------
        # JG
        # ------------------------------

        elif byte == 0x7F:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JG {offset}\n"
            )

            i += 2

        # ------------------------------
        # JL
        # ------------------------------

        elif byte == 0x7C:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JL {offset}\n"
            )

            i += 2

        # ------------------------------
        # PUSHF
        # ------------------------------

        elif byte == 0x9C:

            resultado += (
                f"{i:08X}  PUSHF\n"
            )

            i += 1

        # ------------------------------
        # POPF
        # ------------------------------

        elif byte == 0x9D:

            resultado += (
                f"{i:08X}  POPF\n"
            )

            i += 1

        # ------------------------------
        # CLC
        # ------------------------------

        elif byte == 0xF8:

            resultado += (
                f"{i:08X}  CLC\n"
            )

            i += 1

        # ------------------------------
        # STC
        # ------------------------------

        elif byte == 0xF9:

            resultado += (
                f"{i:08X}  STC\n"
            )

            i += 1

        # ------------------------------
        # CLI
        # ------------------------------

        elif byte == 0xFA:

            resultado += (
                f"{i:08X}  CLI\n"
            )

            i += 1

        # ------------------------------
        # STI
        # ------------------------------

        elif byte == 0xFB:

            resultado += (
                f"{i:08X}  STI\n"
            )

            i += 1

        # ------------------------------
        # HLT
        # ------------------------------

        elif byte == 0xF4:

            resultado += (
                f"{i:08X}  HLT\n"
            )

            i += 1

                # ------------------------------
        # XCHG EAX, REG
        # 91-97
        # ------------------------------

        elif 0x91 <= byte <= 0x97:

            reg = registros[byte - 0x90]

            resultado += (
                f"{i:08X}  XCHG EAX, {reg}\n"
            )

            i += 1

        # ------------------------------
        # PUSH IMM8
        # ------------------------------

        elif byte == 0x6A:

            valor = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  PUSH BYTE {valor}\n"
            )

            i += 2

        # ------------------------------
        # LOOP
        # ------------------------------

        elif byte == 0xE2:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  LOOP {offset}\n"
            )

            i += 2

        # ------------------------------
        # JECXZ
        # ------------------------------

        elif byte == 0xE3:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JECXZ {offset}\n"
            )

            i += 2

        # ------------------------------
        # JB
        # ------------------------------

        elif byte == 0x72:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JB {offset}\n"
            )

            i += 2

        # ------------------------------
        # JAE
        # ------------------------------

        elif byte == 0x73:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JAE {offset}\n"
            )

            i += 2

        # ------------------------------
        # JBE
        # ------------------------------

        elif byte == 0x76:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JBE {offset}\n"
            )

            i += 2

        # ------------------------------
        # JA
        # ------------------------------

        elif byte == 0x77:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JA {offset}\n"
            )

            i += 2

        # ------------------------------
        # JS
        # ------------------------------

        elif byte == 0x78:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JS {offset}\n"
            )

            i += 2

        # ------------------------------
        # JNS
        # ------------------------------

        elif byte == 0x79:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JNS {offset}\n"
            )

            i += 2

        # ------------------------------
        # JP
        # ------------------------------

        elif byte == 0x7A:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JP {offset}\n"
            )

            i += 2

        # ------------------------------
        # JNP
        # ------------------------------

        elif byte == 0x7B:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JNP {offset}\n"
            )

            i += 2

        # ------------------------------
        # JGE
        # ------------------------------

        elif byte == 0x7D:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JGE {offset}\n"
            )

            i += 2

        # ------------------------------
        # JLE
        # ------------------------------

        elif byte == 0x7E:

            offset = int.from_bytes(
                data[i+1:i+2],
                "little",
                signed=True
            )

            resultado += (
                f"{i:08X}  JLE {offset}\n"
            )

            i += 2

        # ------------------------------
        # MOVSB
        # ------------------------------

        elif byte == 0xA4:

            resultado += f"{i:08X}  MOVSB\n"
            i += 1

        # ------------------------------
        # MOVSD
        # ------------------------------

        elif byte == 0xA5:

            resultado += f"{i:08X}  MOVSD\n"
            i += 1

        # ------------------------------
        # STOSB
        # ------------------------------

        elif byte == 0xAA:

            resultado += f"{i:08X}  STOSB\n"
            i += 1

        # ------------------------------
        # STOSD
        # ------------------------------

        elif byte == 0xAB:

            resultado += f"{i:08X}  STOSD\n"
            i += 1

        # ------------------------------
        # LODSB
        # ------------------------------

        elif byte == 0xAC:

            resultado += f"{i:08X}  LODSB\n"
            i += 1

        # ------------------------------
        # LODSD
        # ------------------------------

        elif byte == 0xAD:

            resultado += f"{i:08X}  LODSD\n"
            i += 1

        # ------------------------------
        # SCASB
        # ------------------------------

        elif byte == 0xAE:

            resultado += f"{i:08X}  SCASB\n"
            i += 1

        # ------------------------------
        # SCASD
        # ------------------------------

        elif byte == 0xAF:

            resultado += f"{i:08X}  SCASD\n"
            i += 1

        # ------------------------------
        # CLD
        # ------------------------------

        elif byte == 0xFC:

            resultado += f"{i:08X}  CLD\n"
            i += 1

        # ------------------------------
        # STD
        # ------------------------------

        elif byte == 0xFD:

            resultado += f"{i:08X}  STD\n"
            i += 1

        # ------------------------------
        # SAHF
        # ------------------------------

        elif byte == 0x9E:

            resultado += f"{i:08X}  SAHF\n"
            i += 1

        # ------------------------------
        # LAHF
        # ------------------------------

        elif byte == 0x9F:

            resultado += f"{i:08X}  LAHF\n"
            i += 1

        # ------------------------------
        # INT3
        # ------------------------------

        elif byte == 0xCC:

            resultado += f"{i:08X}  INT3\n"
            i += 1

        # ------------------------------
        # INTO
        # ------------------------------

        elif byte == 0xCE:

            resultado += f"{i:08X}  INTO\n"
            i += 1

        # ------------------------------
        # RET imm16
        # ------------------------------

        elif byte == 0xC2:

            valor = int.from_bytes(
                data[i+1:i+3],
                "little"
            )

            resultado += (
                f"{i:08X}  RET {valor}\n"
            )

            i += 3

        # ------------------------------
        # RETF
        # ------------------------------

        elif byte == 0xCB:

            resultado += (
                f"{i:08X}  RETF\n"
            )

            i += 1

        # ------------------------------
        # RETF imm16
        # ------------------------------

        elif byte == 0xCA:

            valor = int.from_bytes(
                data[i+1:i+3],
                "little"
            )

            resultado += (
                f"{i:08X}  RETF {valor}\n"
            )

            i += 3

        # ------------------------------
        # DESCONOCIDO
        # ------------------------------

        else:

            resultado += (
                f"{i:08X}  DB {byte:02X}\n"
            )

            i += 1

    return resultado