import flet as ft
from function_propose import *
import json
import time
import threading
from chatbot import ChatBot

with open('basedatos.json', 'r') as archivo:
    datos = json.load(archivo)

def ingresar_usuario(vista, page):
    txt_result = ft.TextField()
    dato = ""

    def on_send_click(_):
        nonlocal dato
        dato = txt_result.value
        page.update()

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

def ingresoDatos1(vista, page):
    texto_a_audio(datos['bienvenida'])
    nombre = ingresar_usuario(vista, page)
    asistente_habla(vista, page, "Hola {}. Mucho gusto.".format(nombre))
    texto_a_audio("Hola {}. Mucho gusto.".format(nombre))
    resume = chatbot.send_prompt("Por favor si esto pero resumido: " +nombre + "Ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger.")
    asistente_habla(vista, page, resume)
    texto_a_audio(resume)
    asistente_habla(vista, page, "Aprendizaje. Tests. Juegos.")
    texto_a_audio("Aprendizaje. Tests. Juegos.")
    resume = chatbot.send_prompt("Por favor resume lo siguiente: La opción Aprendizaje es donde podrás aprender todo con respecto a la Estructura de un computador. La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes. Y por último, la tercer opción, es Juegos, donde tambien podrás demostrar lo que aprendiste jugando.")
    asistente_habla(vista, page, resume)
    texto_a_audio(resume)
    asistente_habla(vista, page, "¿Qué opción eliges?")
    texto_a_audio("¿Qué opción eliges?")
    time.sleep(0.3)
    asistente_habla(vista, page, "¿uno? ¿dos? ¿tres?")
    texto_a_audio("¿uno? ¿dos? ¿tres?")


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
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
    viewMenu.scroll = 'AUTO'
    threading.Thread(target=ingresoDatos1, args=(viewMenu, page)).start()
    return viewMenu
            
def Aprendizaje(page):
    return ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )

def main(page: ft.Page):
    page.title = "Routes Example"
    chatbot.start_conversation()

    def route_change(route):
        page.views.clear()
        page.views.append(
            #The second is controls, add with append
            menu(page)
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

api_key = 'AIzaSyCkNOaAFzGuPw3Gdjn4cBvgrM4_ZR3aqHU'
chatbot = ChatBot(api_key = api_key)
ft.app(target=main)