from functools import wraps

from flask import session, redirect, url_for, flash


def login_obrigatorio(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "usuario" not in session:

            flash("Faça login primeiro")

            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function


def requer_permissao(*permissoes):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            if "usuario" not in session:

                return redirect(url_for("auth.login"))

            if session.get("permissao") not in permissoes:

                flash("Você não tem permissão")

                return redirect(url_for("auth.dashboard"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator