from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições de diferentes origens

# Configuração da conexão com o Azure SQL Database
#def get_db_connection():
#    server = 'seu_servidor.database.windows.net'
#    database = 'easybox-db'
#    username = 'seu_usuario'
#    password = 'sua_senha'
#    driver = '{ODBC Driver 17 for SQL Server}'
#    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
#    return pyodbc.connect(connection_string)


# Função para conectar ao banco de dados
def get_db_connection():
    server = os.getenv('SQL_SERVER')  # Nome do servidor
    database = os.getenv('SQL_DATABASE')  # Nome do banco de dados
    username = os.getenv('SQL_USERNAME')  # Nome de usuário
    password = os.getenv('SQL_PASSWORD')  # Senha
    driver = '{ODBC Driver 17 for SQL Server}'  # Driver do SQL Server

    # String de conexão
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(connection_string)

# Exemplo de rota para testar a conexão
@app.route('/teste')
def teste_conexao():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    resultado = cursor.fetchone()
    conn.close()
    return f'Conexão bem-sucedida! Resultado: {resultado[0]}'

if __name__ == '__main__':
    app.run(debug=True)





# Rota para listar todos os pedidos
@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pedidos')
    pedidos = cursor.fetchall()
    conn.close()
    return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in pedidos])

# Rota para criar um novo pedido
@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Pedidos (cliente, item, status) VALUES (?, ?, ?)',
                  (dados['cliente'], dados['item'], 'Pendente'))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Pedido criado com sucesso!'}), 201

# Rota para atualizar o status de um pedido
@app.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    dados = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Pedidos SET status = ? WHERE id = ?', (dados['status'], id))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Pedido atualizado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)