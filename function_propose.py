import pyaudio
import speech_recognition as sr
import pyttsx3

p = pyaudio.PyAudio()
r = sr.Recognizer()
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def texto_a_audio(comando):
    palabra = pyttsx3.init()
    palabra.say(comando)
    palabra.runAndWait()

def capturar_voz(reconocer, microfono, tiempo_ruido=1.0):
    if not isinstance(reconocer, sr.Recognizer):
        raise TypeError("'reconocer' no es de la instacia 'Recognizer'")

    if not isinstance(microfono, sr.Microphone):
        raise TypeError("'microfono' no es de la instacia 'Microphone'")

    with microfono as fuente:
        reconocer.adjust_for_ambient_noise(fuente, duration=tiempo_ruido)
        audio = reconocer.listen(fuente)

    respuesta = {
        "suceso": True,
        "error": None,
        "mensaje": None,
    }
    try:
        respuesta["mensaje"] = reconocer.recognize_google(
            audio, language="es-PE")
    except sr.RequestError:
        respuesta["suceso"] = False
        respuesta["error"] = "API no disponible"
    except sr.UnknownValueError:
        respuesta["error"] = "Habla inteligible"
    return respuesta

def enviar_voz():
    while (1):
        palabra = capturar_voz(recognizer, microphone)
        if palabra["mensaje"]:
            break
        if not palabra["suceso"]:
            print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado. <>")
            texto_a_audio(
                "Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado.")
            exit(1)
        print("No pude escucharte, ¿podrias repetirlo?\n")
        texto_a_audio("No pude escucharte, ¿podrias repetirlo?")
    return palabra["mensaje"].lower()

def capture_audio():
    # Configurar el microfono
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    # Capturar audio
    frames = []
    for i in range(0, 10000):
        data = stream.read(1024)
        frames.append(data)

    # Cerrar el microfono
    stream.close()

    # Convertir los datos de audio a un formato que pueda ser utilizado por SpeechRecognition
    audio_data = sr.AudioData(bytes(frames), sample_rate=16000, duration=len(frames) / 16000)

    return audio_data

def recognize_voice(audio_data):
    # Reconocer la voz
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(audio_data)
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "No se pudo reconocer la voz"
    except sr.RequestError as e:
        return f"Error de reconocimiento de voz: {e}"
    
