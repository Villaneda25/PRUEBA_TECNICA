# Importamos las librerías necesarias de Flask
from flask import Flask, request, render_template, jsonify, redirect, url_for

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Lista para almacenar los libros (simulando una base de datos)
libros = []

# Función para validar los campos de un libro
def validar_campos_libro(libro):
    # Definimos los campos obligatorios
    campos_obligatorios = ['titulo', 'autor', 'anio_publicacion', 'genero']
    # Verificamos si todos los campos obligatorios están presentes y no son vacíos
    for campo in campos_obligatorios:
        if campo not in libro or not libro[campo]:
            return False
    return True

# Endpoint para agregar un libro
@app.route('/libros', methods=['POST'])
def agregar_libro():
    # Obtenemos los datos del libro del cuerpo de la solicitud en formato JSON
    datos = request.get_json()
    # Verificamos si los campos del libro son válidos
    if validar_campos_libro(datos):
        # Agregamos el libro a la lista de libros
        libros.append(datos)
        # Retornamos un mensaje de éxito con el código de estado 201 (CREADO)
        return jsonify({'mensaje': 'Libro agregado correctamente'}), 201
    else:
        # Retornamos un mensaje de error con el código de estado 400 (BAD REQUEST)
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

# Endpoint para obtener todos los libros
@app.route('/libros', methods=['GET'])
def obtener_libros():
    # Retornamos la lista de libros en formato JSON
    return jsonify(libros)

# Endpoint para eliminar un libro
@app.route('/eliminar-libro', methods=['POST'])
def eliminar_libro():
    # Obtenemos el título del libro a eliminar del formulario
    titulo = request.form['titulo']
    # Iteramos sobre la lista de libros
    for libro in libros:
        # Si encontramos el libro con el título proporcionado, lo eliminamos
        if libro['titulo'] == titulo:
            libros.remove(libro)
            # Redireccionamos al formulario principal después de eliminar el libro
            return redirect(url_for('formulario'))
    # Si el libro no se encuentra, retornamos un mensaje de error con el código de estado 404 (NOT FOUND)
    return jsonify({'error': 'Libro no encontrado'}), 404

# Endpoint para editar un libro
@app.route('/editar-libro', methods=['GET', 'POST'])
def editar_libro():
    # Obtenemos el título del libro a editar de los parámetros de la URL
    titulo = request.args.get('titulo')
    # Iteramos sobre la lista de libros
    for libro in libros:
        # Si encontramos el libro con el título proporcionado
        if libro['titulo'] == titulo:
            # Si la solicitud es POST, actualizamos los datos del libro
            if request.method == 'POST':
                libro['titulo'] = request.form['titulo']
                libro['autor'] = request.form['autor']
                libro['anio_publicacion'] = request.form['anio_publicacion']
                libro['genero'] = request.form['genero']
                # Redireccionamos al formulario principal después de editar el libro
                return redirect(url_for('formulario'))
            else:
                # Si la solicitud es GET, mostramos el formulario de edición del libro
                return render_template('editar.html', libro=libro)
    # Si el libro no se encuentra, retornamos un mensaje de error con el código de estado 404 (NOT FOUND)
    return jsonify({'error': 'Libro no encontrado'}), 404

# Formulario para agregar o editar un libro
@app.route('/', methods=['GET', 'POST'])
def formulario():
    # Si la solicitud es POST, agregamos un nuevo libro
    if request.method == 'POST':
        nuevo_libro = {
            'titulo': request.form['titulo'],
            'autor': request.form['autor'],
            'anio_publicacion': request.form['anio_publicacion'],
            'genero': request.form['genero']
        }
        # Verificamos si los campos del nuevo libro son válidos
        if validar_campos_libro(nuevo_libro):
            # Agregamos el nuevo libro a la lista de libros
            libros.append(nuevo_libro)
            mensaje = 'Libro agregado correctamente'
        else:
            mensaje = 'Todos los campos son obligatorios'
        # Retornamos la plantilla del formulario con el mensaje y la lista de libros actualizada
        return render_template('index.html', mensaje=mensaje, libros=libros)
    # Si la solicitud es GET, mostramos el formulario vacío
    return render_template('index.html', mensaje='', libros=libros)

# Punto de entrada para la aplicación Flask
if __name__ == '__main__':
    # Ejecutamos la aplicación en modo debug
    app.run(debug=True, port=5869)
