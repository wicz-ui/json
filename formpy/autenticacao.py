from flask import session, flash, redirect, url_for
from functools import wraps


def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Faça login para acessar o sistema.')
            return redirect(url_for('login'))

        return funcao(*args, **kwargs)

    return verificar