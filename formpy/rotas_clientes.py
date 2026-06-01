from flask import render_template, request, redirect, url_for, flash
import mysql.connector

from database import conectar
from autenticacao import login_obrigatorio


def registrar_rotas_clientes(app):

    @app.route('/clientes')
    @login_obrigatorio
    def clientes():
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute("SELECT * FROM cliente")
            clientes = cursor.fetchall()

            cursor.close()
            conexao.close()

            return render_template('index.html', clientes=clientes)

        except mysql.connector.Error as err:
            return f"Erro ao buscar clientes: {err}"


    @app.route('/clientes/cadastrar', methods=['POST'])
    @login_obrigatorio
    def cadastrar_cliente():
        cpfs = request.form.getlist('cpf')
        nomes = request.form.getlist('primeiro_nome')
        sobrenomes = request.form.getlist('sobrenome')
        idades = request.form.getlist('idade')

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            comando = """
            INSERT INTO cliente
            (CPF, PRIMEIRO_NOME, SOBRENOME, IDADE)
            VALUES (%s, %s, %s, %s)
            """

            valores = []

            for cpf, nome, sobrenome, idade in zip(cpfs, nomes, sobrenomes, idades):
                if cpf and nome and sobrenome and idade:
                    valores.append((cpf, nome, sobrenome, idade))

            cursor.executemany(comando, valores)
            conexao.commit()

            cursor.close()
            conexao.close()

            flash('Cliente(s) cadastrado(s) com sucesso!')
            return redirect(url_for('clientes'))

        except mysql.connector.Error as err:
            return f"Erro ao cadastrar cliente: {err}"


    @app.route('/clientes/deletar/<cpf>', methods=['POST'])
    @login_obrigatorio
    def deletar_cliente(cpf):
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            comando = "DELETE FROM cliente WHERE CPF = %s"
            valores = (cpf,)

            cursor.execute(comando, valores)
            conexao.commit()

            cursor.close()
            conexao.close()

            flash('Cliente excluído com sucesso!')
            return redirect(url_for('clientes'))

        except mysql.connector.Error as err:
            return f"Erro ao deletar cliente: {err}"
