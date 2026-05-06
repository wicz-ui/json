from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'troque_essa_chave_secreta'

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

        cursor.execute("SELECT * FROM produto")
        produtos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return render_template('index2.html', produtos=produtos)

    except mysql.connector.Error as err:
        return f"Erro ao buscar produtos: {err}"


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_produto = request.form.get('nome_produto')
    categoria = request.form.get('categoria')
    preco = request.form.get('preco')
    quantidade = request.form.get('quantidade')

    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        comando = """
        INSERT INTO produto
        (NOME_PRODUTO, CATEGORIA, PRECO, QUANTIDADE)
        VALUES (%s, %s, %s, %s)
        """

        valores = (nome_produto, categoria, preco, quantidade)

        cursor.execute(comando, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('index'))

    except mysql.connector.Error as err:
        return f"Erro ao cadastrar produto: {err}"


@app.route('/deletar/<int:id_produto>', methods=['POST'])
def deletar(id_produto):
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        comando = "DELETE FROM produto WHERE ID_PRODUTO = %s"
        valores = (id_produto,)

        cursor.execute(comando, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        flash('Produto excluído com sucesso!')
        return redirect(url_for('index'))

    except mysql.connector.Error as err:
        return f"Erro ao deletar produto: {err}"


if __name__ == '__main__':
    app.run(debug=True)
