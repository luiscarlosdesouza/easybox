from azure.iot.device import IoTHubDeviceClient, MethodResponse
import RPi.GPIO as GPIO  # Exemplo para Raspberry Pi
import time

# Configurações do GPIO (exemplo para Raspberry Pi)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # Pino para controlar a abertura do armário
GPIO.setup(23, GPIO.IN)   # Pino para detectar se o armário está aberto ou fechado

# String de conexão do dispositivo IoT
DEVICE_CONNECTION_STRING = "HHostName=easybox-iot-hub.azure-devices.net;DeviceId=armario-001;SharedAccessKey=5+IOxCcSeGYCIeekFQzLHT8rEJuPQDAJ/WFXqtXJMUY="

# Função para verificar o status do armário
def verificar_status():
    status = GPIO.input(23)  # Lê o estado do sensor
    return "Aberto" if status == GPIO.HIGH else "Fechado"

# Função para lidar com o Direct Method
def method_request_handler(method_request):
    print(f"Método direto recebido: {method_request.name}")

    if method_request.name == "GetStatus":
        # Obtém o status atual do armário
        status = verificar_status()
        payload = {"status": status}

        # Envia uma resposta ao método direto
        method_response = MethodResponse.create_from_method_request(
            method_request, 200, payload
        )
        device_client.send_method_response(method_response)
        print(f"Resposta enviada: {payload}")
    else:
        # Responde com um erro se o método não for reconhecido
        method_response = MethodResponse.create_from_method_request(
            method_request, 400, {"error": "Método não suportado"}
        )
        device_client.send_method_response(method_response)

# Função principal
def main():
    global device_client

    # Cria uma instância do cliente do dispositivo IoT
    device_client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)

    # Configura o handler para métodos diretos
    device_client.on_method_request_received = method_request_handler

    # Conecta ao IoT Hub
    device_client.connect()

    print("Dispositivo IoT conectado ao Azure IoT Hub. Aguardando métodos diretos...")

    # Mantém o dispositivo em execução
    while True:
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Encerrando o dispositivo IoT...")
    finally:
        GPIO.cleanup()  # Limpa os pinos GPIO ao encerrar