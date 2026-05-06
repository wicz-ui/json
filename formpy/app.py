from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'h56j5dr6rh6d8tj357'

# Configuração do Banco de Dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'escola',
    'database': 'cadastro'
}


@app.route('/')
def index():
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()

        cursor.close()
        conexao.close()

        return render_template('index.html', clientes=clientes)

    except mysql.connector.Error as err:
        return f"Erro ao buscar clientes: {err}"


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    cpf = request.form.get('cpf')
    nome = request.form.get('primeiro_nome')
    sobrenome = request.form.get('sobrenome')
    idade = request.form.get('idade')

    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        comando = """
        INSERT INTO cliente 
        (CPF, PRIMEIRO_NOME, SOBRENOME, IDADE) 
        VALUES (%s, %s, %s, %s)
        """

        valores = (cpf, nome, sobrenome, idade)

        cursor.execute(comando, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('index'))

    except mysql.connector.Error as err:
        return f"Erro ao cadastrar: {err}"


@app.route('/deletar/<cpf>', methods=['POST'])
def deletar(cpf):
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        comando = "DELETE FROM cliente WHERE CPF = %s"
        valores = (cpf,)

        cursor.execute(comando, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect(url_for('index'))

    except mysql.connector.Error as err:
        return f"Erro ao deletar cliente: {err}"


if __name__ == '__main__':
    app.run(debug=True)