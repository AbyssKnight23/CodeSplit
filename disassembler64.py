# ---------- DESENSAMBLADOR 64 BITS ----------

def desensamblar64(data, limite=200):

    resultado = ""  # Aqui guardamos el resultado final
    i = 0  # Puntero que recorre los bytes

    registros = ["RAX", "RCX", "RDX", "RBX", "RSP", "RBP", "RSI", "RDI"]

    # Recorremos los bytes hasta el limite
    while i < min(len(data), limite):

        byte = data[i]  # Leemos 1 byte

        # ---------- PREFIJO REX ----------

        if byte == 0x48:
            rex = byte
            i += 1
            byte = data[i]

        else:
            rex = None

        # ---------- INSTRUCCIONES SIMPLES ----------

        # NOP (No hace nada)
        if byte == 0x90:
            resultado += f"{i:08X}  NOP\n"
            i += 1

        # RET (retorna de una funcion)
        elif byte == 0xC3:
            resultado += f"{i:08X}  RET\n"
            i += 1

        # ---------- INSTRUCCIONES CON DATOS ----------

        # MOV RAX, valor (48 B8 + 8 bytes)
        elif rex == 0x48 and 0xB8 <= byte <= 0xBF:

            reg = registros[byte - 0xB8]
            valor = int.from_bytes(data[i+1:i+9], "little")

            resultado += f"{i:08X}  MOV {reg}, {valor}\n"
            i += 9

        # PUSH valor
        elif byte == 0x68:

            valor = int.from_bytes(data[i+1:i+5], "little")

            resultado += f"{i:08X}  PUSH {valor}\n"
            i += 5

        # PUSH registro
        elif 0x50 <= byte <= 0x57:

            reg = registros[byte - 0x50]

            resultado += f"{i:08X}  PUSH {reg}\n"
            i += 1

        # POP registro
        elif 0x58 <= byte <= 0x5F:

            reg = registros[byte - 0x58]

            resultado += f"{i:08X}  POP {reg}\n"
            i += 1

        # ---------- OPERACIONES ----------

        # ADD RAX, valor
        elif rex == 0x48 and byte == 0x05:

            valor = int.from_bytes(data[i+1:i+5], "little")

            resultado += f"{i:08X}  ADD RAX, {valor}\n"
            i += 5

        # SUB RAX, valor
        elif rex == 0x48 and byte == 0x2D:

            valor = int.from_bytes(data[i+1:i+5], "little")

            resultado += f"{i:08X}  SUB RAX, {valor}\n"
            i += 5

        # CMP RAX, valor
        elif rex == 0x48 and byte == 0x3D:

            valor = int.from_bytes(data[i+1:i+5], "little")

            resultado += f"{i:08X}  CMP RAX, {valor}\n"
            i += 5

        # XOR RAX, RAX
        elif rex == 0x48 and byte == 0x31 and data[i+1] == 0xC0:

            resultado += f"{i:08X}  XOR RAX, RAX\n"
            i += 2

        # ---------- INCREMENTO / DECREMENTO ----------

        # INC registro
        elif 0x40 <= byte <= 0x47:

            reg = registros[byte - 0x40]

            resultado += f"{i:08X}  INC {reg}\n"
            i += 1

        # DEC registro
        elif 0x48 <= byte <= 0x4F:

            reg = registros[byte - 0x48]

            resultado += f"{i:08X}  DEC {reg}\n"
            i += 1

        # ---------- SALTOS Y LLAMADAS ----------

        # CALL direccion
        elif byte == 0xE8:

            offset = int.from_bytes(data[i+1:i+5], "little", signed=True)

            resultado += f"{i:08X}  CALL {offset}\n"
            i += 5

        # JMP direccion
        elif byte == 0xE9:

            offset = int.from_bytes(data[i+1:i+5], "little", signed=True)

            resultado += f"{i:08X}  JMP {offset}\n"
            i += 5

        # JMP corto
        elif byte == 0xEB:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JMP SHORT {offset}\n"
            i += 2

        # JE
        elif byte == 0x74:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JE {offset}\n"
            i += 2

        # JNE
        elif byte == 0x75:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JNE {offset}\n"
            i += 2

                # ---------- OPERACIONES LOGICAS ----------

        # AND RAX, RAX
        elif rex == 0x48 and byte == 0x21 and data[i+1] == 0xC0:

            resultado += f"{i:08X}  AND RAX, RAX\n"
            i += 2

        # OR RAX, RAX
        elif rex == 0x48 and byte == 0x09 and data[i+1] == 0xC0:

            resultado += f"{i:08X}  OR RAX, RAX\n"
            i += 2

        # TEST RAX, RAX
        elif rex == 0x48 and byte == 0x85 and data[i+1] == 0xC0:

            resultado += f"{i:08X}  TEST RAX, RAX\n"
            i += 2

        # NOT RAX
        elif rex == 0x48 and byte == 0xF7 and data[i+1] == 0xD0:

            resultado += f"{i:08X}  NOT RAX\n"
            i += 2

        # NEG RAX
        elif rex == 0x48 and byte == 0xF7 and data[i+1] == 0xD8:

            resultado += f"{i:08X}  NEG RAX\n"
            i += 2

        # XCHG RAX, RBX
        elif rex == 0x48 and byte == 0x87 and data[i+1] == 0xD8:

            resultado += f"{i:08X}  XCHG RAX, RBX\n"
            i += 2

        # ---------- DESPLAZAMIENTOS ----------

        # SHL RAX, 1
        elif rex == 0x48 and byte == 0xD1 and data[i+1] == 0xE0:

            resultado += f"{i:08X}  SHL RAX, 1\n"
            i += 2

        # SHR RAX, 1
        elif rex == 0x48 and byte == 0xD1 and data[i+1] == 0xE8:

            resultado += f"{i:08X}  SHR RAX, 1\n"
            i += 2

        # SAR RAX, 1
        elif rex == 0x48 and byte == 0xD1 and data[i+1] == 0xF8:

            resultado += f"{i:08X}  SAR RAX, 1\n"
            i += 2

        # ROL RAX, 1
        elif rex == 0x48 and byte == 0xD1 and data[i+1] == 0xC0:

            resultado += f"{i:08X}  ROL RAX, 1\n"
            i += 2

        # ROR RAX, 1
        elif rex == 0x48 and byte == 0xD1 and data[i+1] == 0xC8:

            resultado += f"{i:08X}  ROR RAX, 1\n"
            i += 2

        # ---------- BANDERAS ----------

        # PUSHFQ
        elif byte == 0x9C:

            resultado += f"{i:08X}  PUSHFQ\n"
            i += 1

        # POPFQ
        elif byte == 0x9D:

            resultado += f"{i:08X}  POPFQ\n"
            i += 1

        # CLC
        elif byte == 0xF8:

            resultado += f"{i:08X}  CLC\n"
            i += 1

        # STC
        elif byte == 0xF9:

            resultado += f"{i:08X}  STC\n"
            i += 1

        # CLI
        elif byte == 0xFA:

            resultado += f"{i:08X}  CLI\n"
            i += 1

        # STI
        elif byte == 0xFB:

            resultado += f"{i:08X}  STI\n"
            i += 1

        # ---------- SISTEMA ----------

        # HLT
        elif byte == 0xF4:

            resultado += f"{i:08X}  HLT\n"
            i += 1

        # INT 3
        elif byte == 0xCC:

            resultado += f"{i:08X}  INT 3\n"
            i += 1

        # INT n
        elif byte == 0xCD:

            valor = data[i+1]

            resultado += f"{i:08X}  INT {valor}\n"
            i += 2

        # ---------- LEA ----------

        # LEA RAX, [RAX]
        elif rex == 0x48 and byte == 0x8D and data[i+1] == 0x00:

            resultado += f"{i:08X}  LEA RAX, [RAX]\n"
            i += 2

        # ---------- SALTOS CONDICIONALES ----------

        elif byte == 0x70:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JO {offset}\n"
            i += 2

        elif byte == 0x71:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JNO {offset}\n"
            i += 2

        elif byte == 0x72:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JB {offset}\n"
            i += 2

        elif byte == 0x73:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JAE {offset}\n"
            i += 2

        elif byte == 0x76:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JBE {offset}\n"
            i += 2

        elif byte == 0x77:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JA {offset}\n"
            i += 2

        elif byte == 0x78:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JS {offset}\n"
            i += 2

        elif byte == 0x79:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JNS {offset}\n"
            i += 2

        elif byte == 0x7A:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JP {offset}\n"
            i += 2

        elif byte == 0x7B:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JNP {offset}\n"
            i += 2

        elif byte == 0x7C:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JL {offset}\n"
            i += 2

        elif byte == 0x7D:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JGE {offset}\n"
            i += 2

        elif byte == 0x7E:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JLE {offset}\n"
            i += 2

        elif byte == 0x7F:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  JG {offset}\n"
            i += 2

        # LOOP
        elif byte == 0xE2:

            offset = int.from_bytes(data[i+1:i+2], "little", signed=True)

            resultado += f"{i:08X}  LOOP {offset}\n"
            i += 2

        # ---------- SI NO CONOCEMOS EL BYTE ----------

        else:
            resultado += f"{i:08X}  DB {byte:02X}\n"
            i += 1

    return resultado