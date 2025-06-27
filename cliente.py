
import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(2.0)

def listen_server():
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            message = data.decode()
            if message.startswith("CARTA:"):
                valor = message.split(":")[1]
                print(f"[Servidor] Você recebeu a carta: {valor}")
            elif message.startswith("RESULTADO:"):
                resultado = message.split(":")[1]
                print(f"[Servidor] Resultado final: Você {resultado} a partida!")
            elif message.startswith("MENSAGEM:"):
                texto = message.split(":", 1)[1]
                print(f"[Servidor] {texto}")
        except socket.timeout:
            continue

def send_message(msg):
    client_socket.sendto(msg.encode(), (SERVER_HOST, SERVER_PORT))

nome = input("Digite seu nome: ")
send_message(f"ENTRAR:{nome}")

listener_thread = threading.Thread(target=listen_server, daemon=True)
listener_thread.start()

while True:
    try:
        comando = input("Digite comando (PEDIR_CARTA / PARAR): ").strip().upper()
        if comando in ["PEDIR_CARTA", "PARAR"]:
            send_message(comando)
        else:
            print("Comando inválido.")
    except KeyboardInterrupt:
        print("\nEncerrando cliente...")
        break

client_socket.close()
