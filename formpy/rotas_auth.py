from flask import render_template, request, redirect, url_for, flash, session
import mysql.connector

from database import conectar
from autenticacao import login_obrigatorio


def registrar_rotas_auth(app):

    @app.route('/')
    def inicio():
        if 'admin_id' in session:
            return redirect(url_for('menu'))

        return redirect(url_for('login'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            try:
                conexao = conectar()
                cursor = conexao.cursor(dictionary=True)

                comando = """
                SELECT * FROM admin
                WHERE EMAIL = %s AND SENHA = %s
                """

                cursor.execute(comando, (email, senha))
                admin = cursor.fetchone()

                cursor.close()
                conexao.close()

                if admin:
                    session['admin_id'] = admin['ID_ADMIN']
                    session['admin_email'] = admin['EMAIL']
                    return redirect(url_for('menu'))
                else:
                    flash('E-mail ou senha incorretos.')
                    return redirect(url_for('login'))

            except mysql.connector.Error as err:
                return f"Erro ao fazer login: {err}"

        return render_template('login.html')


    @app.route('/logout')
    def logout():
        session.clear()
        flash('Você saiu do sistema.')
        return redirect(url_for('login'))


    @app.route('/menu')
    @login_obrigatorio
    def menu():
        return render_template('menu.html')
