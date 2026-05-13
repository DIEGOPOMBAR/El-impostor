from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

salas = {}

palabras = [
    "Pizza",
    "Hospital",
    "Avion",
    "Netflix",
    "Futbol",
    "Helado"
]

# PAGINA PRINCIPAL
@app.get("/", response_class=HTMLResponse)
def home():

    html = """

    <!DOCTYPE html>

    <html>

    <head>
        <title>El Impostor</title>

        <style>

            body {
                background-color: #111;
                color: white;
                font-family: Arial;
                text-align: center;
                margin-top: 50px;
            }

            input {
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
                border: none;
            }

            button {
                padding: 10px 20px;
                margin: 5px;
                border: none;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
            }

            button:hover {
                background-color: #45a049;
            }

        </style>

    </head>

    <body>

        <h1>EL IMPOSTOR</h1>

        <button onclick="crearSala()">
            Crear Sala
        </button>

        <br><br>

        <input
            type="text"
            id="codigo"
            placeholder="Codigo Sala"
        >

        <input
            type="text"
            id="nombre"
            placeholder="Tu Nombre"
        >

        <br><br>

        <button onclick="unirseSala()">
            Unirse
        </button>

        <button onclick="iniciarPartida()">
            Iniciar
        </button>

        <button onclick="verRol()">
            Ver Rol
        </button>

        <script>

        async function crearSala() {

            let respuesta = await fetch('/crear_sala')

            let datos = await respuesta.json()

            alert("Codigo Sala: " + datos.codigo)
        }

        async function unirseSala() {

            let codigo =
                document.getElementById("codigo").value

            let nombre =
                document.getElementById("nombre").value

            let url =
                "/unirse?codigo=" +
                codigo +
                "&nombre=" +
                nombre

            let respuesta = await fetch(url)

            let datos = await respuesta.json()

            alert(JSON.stringify(datos))
        }

        async function iniciarPartida() {

            let codigo =
                document.getElementById("codigo").value

            let url =
                "/iniciar?codigo=" + codigo

            let respuesta = await fetch(url)

            let datos = await respuesta.json()

            alert(JSON.stringify(datos))
        }

        async function verRol() {

            let codigo =
                document.getElementById("codigo").value

            let nombre =
                document.getElementById("nombre").value

            let url =
                "/ver_rol?codigo=" +
                codigo +
                "&nombre=" +
                nombre

            let respuesta = await fetch(url)

            let datos = await respuesta.json()

            if (datos.rol == "IMPOSTOR") {

                alert("SOS EL IMPOSTOR")

            } else {

                alert(
                    "Palabra: " +
                    datos.palabra
                )
            }
        }

        </script>

    </body>

    </html>
    """

    return html


# CREAR SALA
@app.get("/crear_sala")
def crear_sala():

    codigo = str(random.randint(1000, 9999))

    salas[codigo] = {
        "jugadores": [],
        "impostor": None,
        "palabra": None
    }

    return {
        "codigo": codigo
    }


# UNIRSE A SALA
@app.get("/unirse")
def unirse(codigo: str, nombre: str):

    if codigo not in salas:

        return {
            "error": "Sala no existe"
        }

    salas[codigo]["jugadores"].append(nombre)

    return {
        "mensaje": "Jugador agregado",
        "jugadores": salas[codigo]["jugadores"]
    }


# INICIAR PARTIDA
@app.get("/iniciar")
def iniciar(codigo: str):

    if codigo not in salas:

        return {
            "error": "Sala no existe"
        }

    jugadores = salas[codigo]["jugadores"]

    if len(jugadores) < 3:

        return {
            "error": "Minimo 3 jugadores"
        }

    impostor = random.choice(jugadores)

    palabra = random.choice(palabras)

    salas[codigo]["impostor"] = impostor

    salas[codigo]["palabra"] = palabra

    return {
        "mensaje": "Partida iniciada"
    }


# VER ROL
@app.get("/ver_rol")
def ver_rol(codigo: str, nombre: str):

    if codigo not in salas:

        return {
            "error": "Sala no existe"
        }

    sala = salas[codigo]

    if nombre not in sala["jugadores"]:

        return {
            "error": "Jugador no encontrado"
        }

    if nombre == sala["impostor"]:

        return {
            "rol": "IMPOSTOR"
        }

    return {
        "rol": "JUGADOR",
        "palabra": sala["palabra"]
    }
