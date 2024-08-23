import requests
import random
import json

PROXY_API_URL = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&country=br&protocol=http&proxy_format=protocolipport&format=json&timeout=20000"

def get_proxies():
    """Obter a lista de proxies da API"""
    try:
        response = requests.get(PROXY_API_URL)
        proxies = response.text.splitlines()
        return proxies
    except Exception as e:
        print(f"Erro ao obter proxies: {e}")
        return []

def save_proxies_to_file(proxies, filename="proxies.json"):
    """Salvar proxies em um arquivo JSON"""
    with open(filename, 'w') as f:
        json.dump(proxies, f)

def load_proxies_from_file(filename="proxies.json"):
    """Carregar proxies do arquivo JSON"""
    try:
        with open(filename, 'r') as f:
            proxies = json.load(f)
        return proxies
    except FileNotFoundError:
        print("Arquivo de proxies não encontrado.")
        return []

def get_random_proxy(proxies):
    """Selecionar um proxy aleatório"""
    return random.choice(proxies)

def create_proxy_session(proxy):
    """Criar uma sessão de requests com proxy"""
    session = requests.Session()
    session.proxies = {
        "http": proxy,
        "https": proxy,
    }
    return session

def test_proxy(proxy):
    """Testar o proxy com uma requisição simples"""
    session = create_proxy_session(proxy)
    try:
        response = session.get("http://httpbin.org/ip", timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} está funcionando.")
            return True
    except:
        pass
    print(f"Proxy {proxy} falhou.")
    return False

if __name__ == "__main__":
    proxies = get_proxies()
    save_proxies_to_file(proxies)
    
    # Teste de proxy
    loaded_proxies = load_proxies_from_file()
    if loaded_proxies:
        proxy = get_random_proxy(loaded_proxies)
        test_proxy(proxy)
