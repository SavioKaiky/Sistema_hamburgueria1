from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.models.usuario import Usuario
from app import db

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and user.verificar_senha(senha):
            session["usuario"] = user.usuario
            session["permissao"] = user.permissao

            return redirect(url_for("auth.dashboard"))
        else:
            flash("Usuário ou senha inválidos!", "danger")

    return render_template("login.html")


@auth.route("/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    return render_template("index.html")

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))