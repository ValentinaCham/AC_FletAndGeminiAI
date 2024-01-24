import flet as ft
from function_propose import *
import json

with open('basedatos.json', 'r') as archivo:
    datos = json.load(archivo)

def main(page: ft.Page):

    txt_result = ft.Text(value="Resultado")

    texto_a_audio(datos['bienvenida'])

    def on_button_click(e):
        audio_data = enviar_voz()
        #result = recognize_voice(audio_data)
        txt_result.value = audio_data
        page.update()

    page.add(
        ft.ElevatedButton(text="Habla", on_click=on_button_click),
        txt_result,
    )

ft.app(target=main)