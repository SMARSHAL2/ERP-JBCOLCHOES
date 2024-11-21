from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__, template_folder="templates")

# Configurações do PostgreSQL
DB_HOST = "localhost"
DB_NAME = "erpdatabase"
DB_USER = "postgres"
DB_PASSWORD = "18122003"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/')
def cadastro():
    return render_template('cadastro.html')

@app.route('/estoque')
def estoque():
    # Captura os parâmetros de busca do formulário
    busca = request.args.get('busca', '')
    codigo_barras = request.args.get('codigo_barras', '')
    codigo_interno = request.args.get('codigo_interno', '')
    categoria = request.args.get('categoria', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Construção da query com condições opcionais
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []
    
    if busca:
        query += " AND descricao ILIKE %s"
        params.append(f'%{busca}%')
    
    if codigo_barras:
        query += " AND codigo_barras = %s"
        params.append(codigo_barras)
    
    if codigo_interno:
        query += " AND codigo_interno = %s"
        params.append(codigo_interno)
    
    if categoria:
        query += " AND categoria = %s"
        params.append(categoria)

    cursor.execute(query, params)
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('estoque.html', produtos=produtos, busca=busca, codigo_barras=codigo_barras, codigo_interno=codigo_interno, categoria=categoria)

@app.route('/add_produto', methods=['POST'])
def add_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    codigo_interno = request.form['codigo_interno']
    codigo_barras = request.form['codigo_barras']
    categoria = request.form['categoria']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    fornecedor = request.form['fornecedor']
    tipo_embalagem = request.form['tipo_embalagem']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, descricao, codigo_interno, codigo_barras, categoria, quantidade, preco, fornecedor, tipo_embalagem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, descricao, codigo_interno, codigo_barras, categoria, quantidade, preco, fornecedor, tipo_embalagem))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('estoque'))

if __name__ == "__main__":
    app.run(debug=True)
