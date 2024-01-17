from flask import Flask, request, render_template, make_response, redirect, session
import recsys
import sys
from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv() 
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY

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

    if 'click_count' not in session:
        session['click_count'] = 0

    # me envían el formulario
    if request.method == 'POST' and 'mas_recomendaciones' in request.form:
        session['click_count'] += 1
        
        for id_juego in request.form.keys():
            rating_str = request.form[id_juego]
            if rating_str.strip():
                rating = int(rating_str)
                recsys.insertar_review(id_juego, id_usuario, rating)
            
    # recomendaciones
    juegos = recsys.recomendar(id_usuario, clicks=int(session['click_count']))

    # pongo juegos vistos con rating = 0
    for juego in juegos:
        recsys.insertar_review(juego["id_juego"], id_usuario, 0)

    cant_valorados = len(recsys.valorados(id_usuario))
    cant_ignorados = len(recsys.ignorados(id_usuario))
        
    
    return render_template("recomendaciones.html", juegos=juegos, id_usuario=id_usuario, cant_valorados=cant_valorados, cant_ignorados=cant_ignorados, click_count=session['click_count'])

@app.route('/reset')
def reset():
    id_usuario = request.cookies.get('id_usuario')
    recsys.reset_usuario(id_usuario)

    return make_response(redirect("/recomendaciones"))


if __name__ == "__main__":
    app.run(debug=True)