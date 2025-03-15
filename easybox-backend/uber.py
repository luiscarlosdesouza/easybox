import requests

# URL da API do Uber Eats 
UBER_EATS_API_URL = "https://api.uber.com/v1/eats/orders"

# Função para buscar pedidos do Uber Eats
def buscar_pedidos_uber_eats():
    try:
        # Autenticação (simulação)
        headers = {
            "Authorization": "TOKEN"
        }

        # Faz a requisição à API do Uber Eats
        response = requests.get(UBER_EATS_API_URL, headers=headers)
        response.raise_for_status()

        # Processa os pedidos recebidos
        pedidos = response.json()
        for pedido in pedidos:
            print(f"Pedido recebido: {pedido['id']}")

    except Exception as e:
        print(f"Erro ao buscar pedidos: {e}")