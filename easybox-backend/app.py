from flask import Flask, jsonify, request
import pyodbc
import uuid
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

app = Flask(__name__)

# Configurações de conexão com o Azure SQL Database
server = 'easybox-sql-server.database.windows.net'
database = 'easybox-db'
username = 'CloudSA537d8b38'
password = '**********'
driver = '{ODBC Driver 17 for SQL Server}'

# String de conexão do banco de dados
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# String de conexão do IoT Hub
IOT_HUB_CONNECTION_STRING = "HostName=easybox-iot-hub.azure-devices.net;DeviceId=armario-001;SharedAccessKey=5+IOxCcSeGYCIeekFQzLHT8rEJuPQDAJ/WFXqtXJMUY="

# Endpoint para receber pedidos de aplicativos de entrega
@app.route('/api/pedidos', methods=['POST'])
def receber_pedido():
    try:
        # Recebe os dados do pedido no formato JSON
        dados_pedido = request.json

        # Valida os dados do pedido
        if not dados_pedido or 'cliente' not in dados_pedido or 'itens' not in dados_pedido:
            return jsonify({"error": "Dados do pedido inválidos"}), 400

        # Gera um ID único para o pedido
        id_pedido = str(uuid.uuid4())

        # Conecta ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insere o pedido no banco de dados
        cursor.execute("""
            INSERT INTO Pedidos (id, cliente, itens, status)
            VALUES (?, ?, ?, ?)
        """, id_pedido, dados_pedido['cliente'], str(dados_pedido['itens']), 'Recebido')

        conn.commit()

        # Atribui um armário ao pedido (simulação)
        armario = atribuir_armario(id_pedido)

        # Envia um comando para abrir o armário
        abrir_armario(armario)

        # Envia uma notificação ao cliente (simulação)
        enviar_notificacao(dados_pedido['cliente'], id_pedido, armario)

        return jsonify({
            "message": "Pedido recebido com sucesso!",
            "id_pedido": id_pedido,
            "armario": armario
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Função para atribuir um armário ao pedido (simulação)
def atribuir_armario(id_pedido):
    # Aqui você pode implementar a lógica para atribuir um armário disponível
    # Por enquanto, vamos simular a atribuição de um armário fixo
    return "armario-001"

# Função para enviar comando de abrir o armário
def abrir_armario(armario):
    try:
        # Cria uma instância do IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)

        # Define o método direto para abrir o armário
        method_name = "abrir_armario"
        payload = {"armario": armario}

        # Envia o comando para o dispositivo
        device_method = CloudToDeviceMethod(method_name=method_name, payload=payload)
        registry_manager.invoke_device_method(armario, device_method)

        print(f"Comando enviado para abrir o armário {armario}")

    except Exception as e:
        print(f"Erro ao enviar comando para o armário: {e}")

# Função para enviar notificação ao cliente (simulação)
def enviar_notificacao(cliente, id_pedido, armario):
    # Aqui você pode integrar com um serviço de notificação (e-mail, SMS, etc.)
    print(f"Notificação enviada para {cliente}: Pedido {id_pedido} está no armário {armario}.")

if __name__ == '__main__':
    app.run(debug=True)