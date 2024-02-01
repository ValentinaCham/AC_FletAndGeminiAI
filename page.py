import flet as ft
from function_propose import *
from pruebaExtraccion import *
from configparser import ConfigParser
import json
import time
import threading
from chatbot import ChatBot
import os

with open('basedatos.json', 'r') as archivo:
    datos = json.load(archivo)

respuesta = ""
nombre = ""
initFlag = False

def ingresar_usuario(vista, page):
    txt_result = ft.TextField()
    dato = ""

    def on_send_click(_):
        nonlocal dato
        dato = txt_result.value
        page.update()

    button_audio = ft.ElevatedButton(icon="mic_sharp", on_click=lambda _: texto_a_audio("Hola"))
    button_send = ft.ElevatedButton("Send", on_click=on_send_click)

    (((vista.controls[1]).content).content).controls.append(
        ft.ListTile(
            leading=button_send,
            title=txt_result,
            trailing=ft.Icon(ft.icons.ANDROID),
        )
    )

    page.update()

    # Espera hasta que el usuario haga clic en el botón "Send"
    while not dato:
        pass

    # Retorna el dato ingresado por el usuario
    return dato

def asistente_habla(vista, page, mensaje):
    (((vista.controls[1]).content).content).controls.append(
        ft.ListTile(
            leading=ft.Icon(ft.icons.FACE),
            title=ft.Text(mensaje),
            selected=True,
        )
    )
    page.update()

def asistente_imagen(vista, page, linkImagen):
    (((vista.controls[1]).content).content).controls.append(
        ft.ListTile(
            leading=ft.Icon(ft.icons.FACE),
            title=ft.Image(
                src=linkImagen,
                fit=ft.ImageFit.FIT_WIDTH,
                repeat=ft.ImageRepeat.NO_REPEAT,
            ),
            selected=True,
        )
    )
    page.update()

def almacenarNombre(nombre):
    cadena = nombre
    # Abre el archivo en modo append
    with open('dataUser.txt', 'a') as archivo:
        # Agrega la cadena al final del archivo
        archivo.write(cadena + "\n")
    pass

def ingresoDatos1(vista, page):
    global initFlag
    if (os.path.getsize('dataUser.txt') <= 0):
        texto_a_audio(datos['bienvenida'])
        nombre = ingresar_usuario(vista, page)
        almacenarNombre(nombre)
        asistente_habla(vista, page, "Hola {}. Mucho gusto.".format(nombre))
        texto_a_audio("Hola {}. Mucho gusto.".format(nombre))
        resume = chatbot.send_prompt("Por favor si esto pero resumido, no repitas algo que ya hayas dicho: " +nombre + "Ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger.")
        asistente_habla(vista, page, resume)
        texto_a_audio(resume)
        asistente_habla(vista, page, "Aprendizaje. Tests. Juegos.")
        texto_a_audio("Aprendizaje. Tests. Juegos.")
        resume = chatbot.send_prompt("Por favor resume lo siguiente, no repitas algo que ya hayas dicho: La opción Aprendizaje es donde podrás aprender todo con respecto a la Estructura de un computador. La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes. Y por último, la tercer opción, es Juegos, donde tambien podrás demostrar lo que aprendiste jugando.")
        asistente_habla(vista, page, resume)
        texto_a_audio(resume)
        asistente_habla(vista, page, "¿Qué opción eliges?")
        texto_a_audio("¿Qué opción eliges?")
    elif initFlag == False:
        with open('dataUser.txt', 'r') as archivo_lectura:
            nombre = archivo_lectura.readline().strip()
        respuesta = chatbot.send_prompt("Por favor, dale un saludo a " + nombre + ". Es una app sobre Arquitectura de Computadoras. No te extiendas mucho, algo corto, pero que sea natural.")
        initFlag = True
        asistente_habla(vista, page, respuesta)
        texto_a_audio(respuesta)

def seguir(vista, page):
    asistente_habla(vista, page, "¿Quieres seguir aprendiendo?")
    texto_a_audio("¿Quieres seguir aprendiendo?")
    time.sleep(0.5)
    texto_a_audio("Responde con:\n1) Está bien\n2) No gracias")
    asistente_habla(vista, page, "Responde con:\n1) Está bien\n2) No gracias")
    respuesta = ingresar_usuario(vista, page)
    return respuesta

def comprobar_respuesta(vista, page, respuesta, nombre):
    if respuesta == "está bien":
        texto_a_audio("Elige la opción que desees aprender:")
        asistente_habla(vista, page,"Elige la opción que desees aprender:")
        asistente_habla("\n1) Unidad central de proceso CPU\n2) Memoria\n3) Entrada / Salida\n4) Sistemas de interconexión: Buses\n5) Periféricos\n")    
    elif respuesta == "no gracias":
        texto_a_audio(
            "Oh, es una lástima. En ese caso nos veremos en otra ocasión")
        asistente_habla("Oh, es una lástima. En ese caso nos veremos en otra ocasión.")
        time.sleep(0.5)
        texto_a_audio(
            "Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
        asistente_habla("Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
        exit(0)
    else:
        asistente_habla(vista, page,nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
        texto_a_audio(
            nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
        asistente_habla(vista, page,"Responde con:\n1) Está bien.\n2) No gracias")

def menu(page):
    viewMenu = ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Asistente: Arquitectura de Computadoras"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Card(
                        content=ft.Container(
                            width=500,
                            content=ft.Column(
                                [
                                    ft.ListTile(title=ft.Text("Bienvenida")),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.FACE),
                                        title=ft.Text(datos['bienvenida'][0]),
                                        selected=True,
                                    ),
                                ],
                                spacing=0,
                            ),
                            padding=ft.padding.symmetric(vertical=10),
                        )
                    ),
                    ft.ElevatedButton("Aprendizaje", on_click=lambda _: page.go("/learn")),
                    ft.ElevatedButton("Test", on_click=lambda _: page.go("/test")),
                    ft.ElevatedButton("Juegos", on_click=lambda _: page.go("/game")),
                    ft.ElevatedButton("Asistente", on_click=lambda _: page.go("/chatbot")),
                ],
            )
    viewMenu.scroll = 'AUTO'
    hilo = threading.Thread(target=ingresoDatos1, args=(viewMenu, page))
    hilo.daemon = True
    hilo.start()
    return viewMenu

def moduloAprender(vista, page):
    texto_a_audio("Elegiste la opcion APRENDIZAJE.")
    asistente_habla(vista, page, "Antes de empezar quisiera hacer una introduccion a la estructura de computadores.")
    texto_a_audio("Antes de empezar quisiera hacer una introduccion a la estructura de computadores.")
    asistente_imagen(vista, page, "./img/intro/computador.jpg")
    text = ""
    for i in datos['aprendizaje']:
        text = text + i
    resume = chatbot.send_prompt("Por favor si esto pero resumido y con otras palabras, no lo estiendas, que sea preciso, pero también que sea natural, no menciones el nombre del usuario:" + text)
    asistente_habla(vista, page, resume)
    texto_a_audio(resume)
    asistente_imagen(vista, page, "./img/aprendizaje/arquitectura.png")
    texto_a_audio(
        "Como se puede apreciar en la imagen, la estructura de un computador está dado por:")
    asistente_habla(vista, page,
        "Como se puede apreciar en la imagen, la estructura de un computador está dado por:")
    texto_a_audio(
        "Unidad central de proceso CPU. Memoria. Entrada / Salida. Sistemas de interconexion: Buses. Periféricos.")
    asistente_habla(vista, page,"\n1) Unidad central de proceso (CPU)\n 2) Memoria\n 3) Entrada / Salida\n 4) Sistemas de interconexion (Buses)\n 5) Periféricos\n")
    asistente_habla(vista, page,"¿Por cual deseas empezar?")
    texto_a_audio("¿Por cual deseas empezar?")
    time.sleep(0.5)
    asistente_habla(vista, page,"¿uno? ¿dos? ¿tres? ¿cuatro? ¿cinco? o  salir")

    while (1):
        respuesta = ingresar_usuario(vista, page)
        asistente_habla(vista, page,"Tu respuesta " + respuesta)

        if respuesta == "cpu":
            ruta_imagen = "./img/aprendizaje/CPU.png"
            asistente_imagen(vista, page,ruta_imagen)
            texto_a_audio(datos['unidad central de proceso'])
            seguir(vista, page)
            comprobar_respuesta(vista, page, respuesta, nombre)

        elif respuesta == "memoria":
            ruta_imagen = "./img/aprendizaje/memoria.png"
            asistente_imagen(vista, page, ruta_imagen)
            text = ""
            for i in datos['memoria']:
                text = text + i
            for i in datos['circuitos de memoria']:
                text = text + i
            for i in datos['ram']:
                text = text + i
            for i in datos['rom']:
                text = text + i
            for i in datos['flash']:
                text = text + i
            resume = chatbot.send_prompt("Por favor si esto pero resumido y con otras palabras, no lo estiendas, que sea preciso, pero también que sea natural, no menciones el nombre del usuario:" + text + "Si ya antes te pedi lo mismo, por favor responde con otras palabras")
            asistente_habla(vista, page, resume)
            texto_a_audio(resume)
            seguir(vista, page)
            comprobar_respuesta(vista, page, respuesta, nombre)

        elif respuesta == "entrada salida":
            ruta_imagen = "./img/aprendizaje/entrada salida.png"
            asistente_imagen(vista, page,ruta_imagen)
            text = ""
            for i in datos['entrada salida']:
                text = text + i
            resume = chatbot.send_prompt("Por favor si esto pero resumido y con otras palabras, no lo estiendas, que sea preciso, pero también que sea natural, no menciones el nombre del usuario:" + text + "Si ya antes te pedi lo mismo, por favor responde con otras palabras")
            asistente_habla(vista, page, resume)
            texto_a_audio(resume)
            seguir(vista, page)
            comprobar_respuesta(vista, page, respuesta, nombre)

        elif respuesta == "buses":
            ruta_imagen = "./img/aprendizaje/buses.png"
            asistente_imagen(vista, page,ruta_imagen)
            text = ""
            for i in datos['sistemas de interconexión buses']:
                text = text + i
            resume = chatbot.send_prompt("Por favor si esto pero resumido y con otras palabras, no lo estiendas, que sea preciso, pero también que sea natural, no menciones el nombre del usuario:" + text + "Si ya antes te pedi lo mismo, por favor responde con otras palabras")
            asistente_habla(vista, page, resume)
            texto_a_audio(resume)
            seguir(vista, page)
            comprobar_respuesta(vista, page, respuesta, nombre)

        elif respuesta == "periféricos":
            ruta_imagen = "./img/aprendizaje/perifericos.jpg"
            asistente_imagen(vista, page,ruta_imagen)
            text = ""
            for i in datos['perifericos']:
                text = text + i
            resume = chatbot.send_prompt("Por favor si esto pero resumido y con otras palabras, no lo estiendas, que sea preciso, pero también que sea natural, no menciones el nombre del usuario:" + text + "Si ya antes te pedi lo mismo, por favor responde con otras palabras")
            asistente_habla(vista, page, resume)
            texto_a_audio(resume)
            seguir(vista, page)
            comprobar_respuesta(vista, page, respuesta, nombre)
        
        elif respuesta == "salir":
            page.go("/")

        elif respuesta != "unidad central de proceso" or respuesta != "memoria" or respuesta != "entrada salida" or respuesta != "sistemas de interconexion buses" or respuesta != "perifericos":
            texto_a_audio(
                "Perdona, pero por el momento no tengo informacion sobre {}. Prueba con otra OPCION".format(respuesta))
            asistente_habla(vista, page,"Perdona, pero por el momento no tengo informacion sobre {}. Prueba con otra OPCION".format(
                respuesta))
            asistente_habla(vista, page,
                "\n1) Unidad central de proceso CPU\n2) Memoria\n3) Entrada / Salida\n4) Sistemas de interconexion: Buses\n5) Periféricos\n")
        # SI EL MENSAJE ENVIADO NO ES ERRONEO LE PIDE AL USUARIO SELECCIONAR UNA OPCION VALIDA
        else:
            texto_a_audio(
                nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
            asistente_habla(vista, page,
                nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
            asistente_habla(vista, page,
                "\n1) Unidad central de proceso CPU\n 2) Memoria\n 3) Entrada / Salida\n 4) Sistemas de interconexion: Buses\n 5) Periféricos\n")

def Aprendizaje(page):
    viewLearn = ft.View(
                    "/learn",
                    [
                        ft.AppBar(title=ft.Text("APRENDIZAJE"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Card(
                            content=ft.Container(
                                width=500,
                                content=ft.Column(
                                    [
                                        ft.ListTile(
                                            leading=ft.Icon(ft.icons.FACE),
                                            title=ft.Text("Elegiste la opcion APRENDIZAJE."),
                                            selected=True,
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                padding=ft.padding.symmetric(vertical=10),
                            )
                        ),
                    ],
                )
    viewLearn.scroll = 'AUTO'
    threading.Thread(target=moduloAprender, args=(viewLearn, page)).start()
    return viewLearn

def moduloTest(vista, page):
    texto_a_audio("Escogiste: Test")
    asistente_habla(vista, page, "En esta opción tienes para elegir en dar una prueba de entrada sobre PENSAMIENTO COMPUTACIONAL, o dar un examen sobre Estructura de Computadores.")
    texto_a_audio("En esta opción tienes para elegir en dar una prueba de entrada sobre PENSAMIENTO COMPUTACIONAL, o dar un examen sobre Estructura de Computadores.")
    asistente_habla(vista, page, "¿Cuál eliges?")
    texto_a_audio("¿Cuál eliges?")
    asistente_habla(vista, page, "1) Prueba de entrada - Pensamiento Computacional\n 2) Examen - Estructura de computadores")
    texto_a_audio(
                "¿Prueba de entrada - Pensamiento Computacional? o ¿Examen - Estructura de computadores?")
    respuesta = ingresar_usuario(vista, page)
    if respuesta == "1":
        moduloPruebaEntrada(vista, page)
    elif respuesta == "2":
        moduloExamen(vista, page)

def almacenarAvance(avance):
    # Abre el archivo en modo append
    with open('dataUser.txt', 'a') as archivo:
        # Agrega la cadena al final del archivo
        archivo.write(avance + "\n")
    pass

def escribir_respuesta(vista, page, pregunta, opciones, respuesta_correcta):
    global puntaje

    texto_a_audio(pregunta)
    asistente_habla(vista, page, pregunta)
    for i, alternativa in enumerate(opciones, start=1):
        asistente_habla(vista, page, f"{i}. {alternativa}")
        texto_a_audio(f"Opción {i}: {alternativa}")

    respuesta_usuario = ingresar_usuario(vista, page)
    if len(respuesta_usuario) == 1:
        if respuesta_usuario == respuesta_correcta:
            asistente_habla(vista, page,"Respuesta correcta.")
            texto_a_audio("Respuesta correcta.")
            asistente_habla(vista, page,"Ganaste 1 PUNTO.")
            texto_a_audio("Ganaste 1 PUNTO.")
            puntaje += 1
            almacenarAvance(fechaHora() + "El usuario respondio de forma correcta a la pregunta: " + pregunta)
        else:
            asistente_habla(vista, page,"Respuesta incorrecta.")
            texto_a_audio("Respuesta incorrecta.")
            almacenarAvance(fechaHora() + "El usuario respondio de forma incorrecta a la pregunta: " + pregunta)
    else:
        print("Entrada inválida.")
        texto_a_audio("Entrada inválida.")

def moduloPruebaEntrada(vista, page):
    global puntaje
    puntaje = 0
    texto_a_audio("Escogiste: Prueba de entrada de Pensamiento Computacional")
    pregunta_actual = datos['PE PREGUNTA 01']['pregunta']
    opciones_actual = datos['PE PREGUNTA 01']['opciones']
    respuesta_correcta_actual = datos['PE PREGUNTA 01']['respuesta_correcta']
    escribir_respuesta(vista, page, pregunta_actual, opciones_actual, respuesta_correcta_actual)
    asistente_habla(vista, page,"Siguiente pregunta.")
    texto_a_audio("Siguiente pregunta.")
    pregunta_actual = datos['PE PREGUNTA 02']['pregunta']
    opciones_actual = datos['PE PREGUNTA 02']['opciones']
    respuesta_correcta_actual = datos['PE PREGUNTA 02']['respuesta_correcta']
    escribir_respuesta(vista, page, pregunta_actual, opciones_actual, respuesta_correcta_actual)
    asistente_habla(vista, page,"Siguiente pregunta.")
    texto_a_audio("Siguiente pregunta.")
    pregunta_actual = datos['PE PREGUNTA 03']['pregunta']
    opciones_actual = datos['PE PREGUNTA 03']['opciones']
    respuesta_correcta_actual = datos['PE PREGUNTA 03']['respuesta_correcta']
    escribir_respuesta(vista, page, pregunta_actual, opciones_actual, respuesta_correcta_actual)

def moduloExamen(vista, page):
    texto_a_audio("Escogiste: Examen - Estructura de computadores")



def Test(page):
    viewLearn = ft.View(
                    "/test",
                    [
                        ft.AppBar(title=ft.Text("EXAMEN"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Card(
                            content=ft.Container(
                                width=500,
                                content=ft.Column(
                                    [
                                        ft.ListTile(
                                            leading=ft.Icon(ft.icons.FACE),
                                            title=ft.Text("Elegiste la opcion TEST."),
                                            selected=True,
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                padding=ft.padding.symmetric(vertical=10),
                            )
                        ),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
    viewLearn.scroll = 'AUTO'
    threading.Thread(target=moduloTest, args=(viewLearn, page)).start()
    return viewLearn
                

def Game(page):
    return ft.View(
                    "/game",
                    [
                        ft.AppBar(title=ft.Text("JUEGO"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )

def avanceUsuario():
    nombre_archivo = 'dataUser.txt'

    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()
    return contenido

def moduloChatbot(vista, page):
    texto_a_audio("Bienvenido al ChatBot")
    respuesta = chatbot.send_prompt("Dale una Binevenida al Usuario al modulo de chat, algo corto. Al final consultale ¿Que consulta desearias realizar?")
    asistente_habla(vista, page, respuesta)
    texto_a_audio(respuesta)
    while True:
        user_input = ingresar_usuario(vista, page)
        if(user_input == "Almacenar concepto"):
            pasarData(chatbot.send_prompt("Almacenar concepto. Quisiera que me des lo que te pedi pero en el formato JSON con los objectos de 'concepto' 'respuesta'. Dalo de forma directa, sin el ```json del inicio ni el ``` del final"))
        elif(user_input == "Repaso"):
            #El asistente tiene el avance
            respuesta = chatbot.send_prompt("El avance del usuario es el siguiente: " + avanceUsuario() + ". QUisiera que primero lo felicites por las respuestas correctas y que luego hagas un resapso de las respueats incorrectas. En caso haya realiado antes un repaso entonces hacer un repaso general pero pequeño")
            asistente_habla(vista, page, respuesta)
            texto_a_audio(respuesta)
            almacenarAvance(fechaHora() + "El usuario realizo un repaso")
        else: 
            try:
                respuesta = chatbot.send_prompt(user_input)
                asistente_habla(vista, page, respuesta)
                texto_a_audio(respuesta)
            except Exception as e:
                print(f"Error: {e}")

def Chatbot(page):
    viewChat = ft.View(
                    "/chatbot",
                    [
                        ft.AppBar(title=ft.Text("CHATBOT"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Card(
                            content=ft.Container(
                                width=500,
                                content=ft.Column(
                                    [
                                        ft.ListTile(
                                            leading=ft.Icon(ft.icons.FACE),
                                            title=ft.Text("Elegiste la opcion CHATBOT."),
                                            selected=True,
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                padding=ft.padding.symmetric(vertical=10),
                            )
                        ),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
    viewChat.scroll = 'AUTO'
    threading.Thread(target=moduloChatbot, args=(viewChat, page)).start()
    return viewChat


def main(page: ft.Page):
    flagInit = False
    page.title = "Routes Example"
    chatbot.start_conversation()

    def route_change(route):
        page.views.clear()
        page.views.append(
            menu(page)
        )
        if page.route == "/learn":
            page.views.append(
                Aprendizaje(page)
            )
        elif page.route == "/test":
            page.views.append(
                Test(page)
            )
        elif page.route == "/game":
            page.views.append(
                Game(page)
            )
        elif page.route == "/chatbot":
            page.views.append(
                Chatbot(page)
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

config = ConfigParser()
config.read('credential.ini')
api_key = config['gemini_ai']['API_KEY']
chatbot = ChatBot(api_key = api_key)
ft.app(target=main)