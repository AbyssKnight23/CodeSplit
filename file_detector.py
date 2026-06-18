def file_detector(data):

    #Verificamos si el programa tiene mas de 4 bytes
    if(len(data) < 4):
        return "El archivo es demasiado pequeño"

    #Verificamos si el archivo es un Windows EXE (PE)
    if data[0:2] == b'MZ':
        return "Este archivo es un ejecutable de Windows"

    #Verificamos si el archivos es un Linux ELF
    elif data[0:4] == b'\x7fELF':
        return "Este archivo es un ejecutable de Linux"

    else:
        return "Archivo con formato incorrecto (EXE o ELF)"                                                                                                                                                                             