'''
Tema: Aplicación de estructuras de Python: archivos, JSON, cifrado de contraseñas
Fecha: 07 de septiembre del 2022
Autor: Francisco Javier Magallon Romero
Continuación de la práctica 6
'''
import json
import random

import bcrypt

'''
Crear un programa que utilice los archivos Estudiantes.prn y kardex.txt:

1. Crear un método que regrese un conjunto de tuplas de estudiantes. (5) 10 min.
2. Crear un método que regrese un conjunto de tuplas de materias.
3. Crear un método que dado un número de control regrese el siguiente formato JSON:
   {
        "Nombre": "Manzo Avalos Diego",
        "Materias":[
            {
                "Nombre":"Base de Datos",
                "Promedio":85
            },
            {
                "Nombre":"Inteligencia Artificial",
                "Promedio":100
            },
            . . . 
        ],
        "Promedio general": 98.4
   }

4. Regresar una lista de JSON con las materias de un estudiante, el formato es el siguiente:
[
    {"Nombre": "Contabilidad Financiera"},
    {"Nombre": "Dise\u00f1o UX y UI"}, 
    {"Nombre": "Base de datos distribuidas"}, 
    {"Nombre": "Finanzas internacionales IV"}, 
    {"Nombre": "Analisis y dise\u00f1o de sistemas de informacion"}, 
    {"Nombre": "Microservicios"},
    {"Nombre": "Algoritmos inteligentes"}
]
'''
# def regresa_conjunto_promedios():
#     arch = open('Kardex.txt', 'r')
#     cad = arch.read()
#     lista = cad.split("\n")
#     contupla = set()
#     arch.close()
#     for x in lista:
#         mnpaux = x.split("|")
#         tupla = (mnpaux[0], mnpaux[1],mnpaux[2])
#         contupla.add(tupla)
#     return contupla
#
# print(regresa_conjunto_promedios())
#
# def regresa_materias_por_estudiante(ctrl):
#     promedios = regresa_conjunto_promedios() # Funcion de la segunda practica6
#     lista_materias = []
#     for mat in promedios:
#         c,m,p = mat # Destructurar la variable mat
#         if ctrl == c:
#             lista_materias.append({"Nombre":m})
#         return json.dumps(lista_materias)
#
# print(regresa_materias_por_estudiante('18420778'))



'''
5. Generar un archivo de usuarios que contenga el numero de control, éste será el usuario
   y se generará una contraseña de tamaño 10 la cual debe tener:
   A. Al menos una letra mayúscula 
   B. Al menos una letra minúscula
   C. Numeros
   D. Al menos UN carácter especial, considere ( @, #, $,%,&,_,?,! )

   Considere:
    - Crear un método para generar cada caracter
    - El codigo ascii: https://elcodigoascii.com.ar/
    - Encriptar la contraseña con bcrypt, se utiliza con node.js, react, etc. Para ello:
        * Descargue la libreria bcrypt con el comando: "pip install bcrypt" desde la terminal o desde PyCharm
        * Página: https://pypi.org/project/bcrypt/
        * Video:Como Cifrar Contraseñas en Python     https://www.youtube.com/watch?v=9tEovDYSPK4

   El formato del archivo usuarios.txt será:
   control contrasena contraseña_cifrada
   
'''
def generar_letra_mayuscula():
    return chr(random.randint(65,90))

def generar_letra_minuscula():
    return chr(random.randint(97,122))

def generar_numeros(): # numeros del 0 al 9
    return chr(random.randint(48,57))

def generar_caracter(): # genera un caracter especial
    lista_caracteres = ['@', '#', '$','%','&','_','?','!']
    return lista_caracteres[random.randint(0,7)]

def generar_contrasena():
    clave = ""
    for i in range(0,10):
        numero = random.randint(1, 5)
        if numero == 1:
            clave = clave + generar_letra_mayuscula()
        elif numero == 2:
            clave = clave + generar_letra_minuscula()
        elif numero == 3:
            clave = clave + generar_numeros()
        elif numero >= 4 and numero <= 5:
            clave = clave + generar_caracter()
    return clave

# print(generar_contrasena())

# cifrar las contrasenas con bcrypt
def cifrar_contrasena(contrasena):
    sal = bcrypt.gensalt()
    contrasena_cifrada = bcrypt.hashpw(contrasena.encode("utf-8"),sal) # deves convertirla a bits con el encode para que jale
    return contrasena_cifrada

# clave = generar_contrasena()
# print(clave,cifrar_contrasena(clave))


# generar el archivo de usuarios

def regresa_conjunto_estudiantes():
    arch = open('Estudiantes.prn', 'r')
    cad = arch.read()
    lista = cad.split("\n")
    arch.close()
    contupla = set()

    for x in lista:
        tupla = (x[:8], x[8:])
        contupla.add(tupla)
    return contupla

def generar_contrasena_usuarios():
    archivo = open('usuarios.txt', 'r')
    cadena = archivo.read()
    listaarchivo = cadena.split("\n")
    archivo.close()
    arch = set()
    for x in listaarchivo:
        regis = x.split(" ")
        tupla=(regis[0], regis[1], regis[2])
        arch.add(tupla)
    return arch

# print(regresa_conjunto_estudiantes())

def generar_usuarios():
    # obtener lista de estudiantes
    estudiantes = regresa_conjunto_estudiantes()
    ususario = open("usuarios.txt","w")
    contador = 1
    for est in estudiantes:
        c,n = est # dividir una tupla
        clave = generar_contrasena()
        clave_cifrada = cifrar_contrasena(clave)
        registro = c + " " + clave + " " + str(clave_cifrada, "utf-8") + "\n"
        ususario.write(registro)
        contador +=1
        print(contador)
    print("archivo generado")

# print(generar_usuarios())
# generar_usuarios()

# print(bcrypt.checkpw("0#&#Z1B4FF".encode("utf-8"),"$2b$12$uNMjXylIhIMkMR0KvFhOpetO6.jzNrfQ8yBrFtYMOm4jCk2JtntNW".encode("utf-8")))

'''

6. Crear un método "autenticar_usuario(usuario,contrasena)" que regrese una bandera que 
   indica si se pudo AUTENTICAR, el nombre del estudiante y un mensaje, regresar el JSON:
   {
        "Bandera": True,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Bienvenido al Sistema de Autenticación de usuarios"
   }

   ó

   {
        "Bandera": False,
        "Usuario": "",
        "Mensaje": "No existe el Usuario"
   }

   ó

    {
        "Bandera": False,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Contraseña incorrecta"
   }


'''



def autenticar_usuario(usuario, contrasena):
    registro = generar_contrasena_usuarios()
    estudiante = regresa_conjunto_estudiantes()
    validar = {}
    for x in registro:
        if x[0] == usuario:
            for x2 in estudiante:
                if x2[0]==usuario:
                    ban = bcrypt.checkpw(contrasena.encode('utf-8'), x[2].encode('utf-8'))
                    validar["Bandera"] = ban
                    validar["Usuario"] = x2[1]
                    if ban:
                        validar["Mensaje"] = "****Bienvenido al Sistema de Autenticación de usuarios****"
                    else:
                        validar["Mensaje"] = "Contraseña incorrecta***"
                    return validar
    validar["Bandera"] = False
    validar["Usuario"] = ""
    validar["Mensaje"] = "********No existe el Usuario**********"
    return validar

print(autenticar_usuario("18420458","SaFi%%$pnD"))
