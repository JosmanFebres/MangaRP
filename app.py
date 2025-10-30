from flask import Flask, render_template, abort
import os
import re

app = Flask(__name__)

# Carpeta de capítulos para la parte escrita del manga
CAPITULOS_DIR = "capitulos"

# Definición de los arcos argumentales y sus capítulos
arcos_literarios = {
    'tripulacion_pijama': {
        'titulo': 'Arco 1: Tripulación Pijama',
        'capitulos': [
            {'nombre_archivo': 'capitulo1.txt', 'nombre_mostrar': 'Capítulo 1: Navegando...'},
            {'nombre_archivo': 'capitulo2.txt', 'nombre_mostrar': 'Capítulo 2: El cuerpo de mi amigo...'},
            {'nombre_archivo': 'capitulo3.txt', 'nombre_mostrar': 'Capítulo 3: ¡El Capitán de la Marian, Logan!'},
            {'nombre_archivo': 'capitulo4.txt', 'nombre_mostrar': 'Capítulo 4: La batalla contra Logan'},
            {'nombre_archivo': 'capitulo5.txt', 'nombre_mostrar': 'Capítulo 5: El Reino Orange'},
            {'nombre_archivo': 'capitulo6.txt', 'nombre_mostrar': 'Capítulo 6: Las sombras del Reino Orange'},
        ]
    },
    'primer_mar': {
        'titulo': 'Arco 2: Primer Mar',
        'capitulos': [
            {'nombre_archivo': 'capitulo7.txt', 'nombre_mostrar': 'Capítulo 7: ¿¡Nuevos Rostros?!'},
            {'nombre_archivo': 'capitulo8.txt', 'nombre_mostrar': 'Capítulo 8: Arlong Park'},
            # Aquí irán los demás capítulos del Arco 2 cuando los crees
        ]
    }
}

# Lista plana de todos los capítulos para una fácil navegación
all_capitulos = [cap for arco in arcos_literarios.values() for cap in arco['capitulos']]

def obtener_siguiente_anterior(nombre_archivo_actual):
    """Obtiene los nombres de los archivos del capítulo anterior y siguiente."""
    try:
        index_actual = next(i for i, c in enumerate(all_capitulos) if c['nombre_archivo'] == nombre_archivo_actual)
        capitulo_anterior = all_capitulos[index_actual - 1]['nombre_archivo'] if index_actual > 0 else None
        capitulo_siguiente = all_capitulos[index_actual + 1]['nombre_archivo'] if index_actual < len(all_capitulos) - 1 else None
        return capitulo_anterior, capitulo_siguiente
    except (StopIteration, IndexError):
        return None, None

@app.route("/")
def portada():
    return render_template("cover.html")

@app.route("/literario")
def literario():
    return render_template("literario.html", arcos=arcos_literarios)

@app.route("/literario/arco/<nombre_arco>")
def mostrar_arco(nombre_arco):
    arco = arcos_literarios.get(nombre_arco)
    if not arco:
        abort(404)
    return render_template("capitulos_por_arco.html", arco=arco, nombre_arco=nombre_arco)

@app.route("/capitulo/<nombre>")
def mostrar_capitulo(nombre):
    ruta = os.path.join(CAPITULOS_DIR, nombre)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()

        titulo_capitulo = next((c['nombre_mostrar'] for c in all_capitulos if c['nombre_archivo'] == nombre), "Título Desconocido")
        capitulo_anterior, capitulo_siguiente = obtener_siguiente_anterior(nombre)

        # Renderiza el nuevo HTML para formato de libro
        return render_template(
            "capitulo_literario.html",
            titulo=titulo_capitulo,
            contenido=contenido,
            anterior=capitulo_anterior,
            siguiente=capitulo_siguiente
        )
    else:
        abort(404)

@app.route("/manga/<int:capitulo_id>")
def manga(capitulo_id):
    capitulos_paneles = {
        1: 14,
    }
    num_paneles = capitulos_paneles.get(capitulo_id, 0)
    if num_paneles == 0:
        return render_template("proximamente.html", capitulo_id=capitulo_id)
    paneles = [f"P{i}.png" for i in range(1, num_paneles + 1)]
    return render_template("manga.html", capitulo_id=capitulo_id, paneles=paneles)

if __name__ == "__main__":
    app.run(debug=True)
