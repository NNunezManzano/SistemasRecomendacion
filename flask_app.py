from flask import Flask, request, render_template, make_response, redirect
import recsys
import sys

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def login():
    # si me mandaron el formulario y tiene id_usuario... 
    if request.method == 'POST' and 'id_usuario' in request.form:
        id_usuario = request.form['id_usuario']

        # creo el usuario al insertar el id_lector en la tabla "lectores"
        recsys.crear_usuario(id_usuario)

        # mando al usuario a la página de recomendaciones
        res = make_response(redirect("/recomendaciones"))

        # pongo el id_lector en una cookie para recordarlo
        res.set_cookie('id_usuario', id_usuario)
        return res

    # si alguien entra a la página principal y conozco el usuario
    if request.method == 'GET' and 'id_usuario' in request.cookies:
        return make_response(redirect("/recomendaciones"))

    # sino, le muestro el formulario de login
    return render_template('login.html')

@app.route('/recomendaciones', methods=('GET', 'POST'))
def recomendaciones():
    id_usuario = request.cookies.get('id_usuario')

    # me envían el formulario
    if request.method == 'POST':
        for id_juego in request.form.keys():
            rating = int(request.form[id_juego])
            recsys.insertar_review(id_juego, id_usuario, rating)

    # recomendaciones
    juegos = recsys.recomendar(id_usuario)

    # pongo juegos vistos con rating = 0
    for juego in juegos:
        recsys.insertar_review(juego["id_juego"], id_usuario, 0)

    cant_valorados = len(recsys.valorados(id_usuario))
    cant_ignorados = len(recsys.ignorados(id_usuario))
    
    return render_template("recomendaciones.html", juegos=juegos, id_usuario=id_usuario, cant_valorados=cant_valorados, cant_ignorados=cant_ignorados)

@app.route('/reset')
def reset():
    id_usuario = request.cookies.get('id_usuario')
    recsys.reset_usuario(id_usuario)

    return make_response(redirect("/recomendaciones"))


if __name__ == "__main__":
    app.run(debug=True)