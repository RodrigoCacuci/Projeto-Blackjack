
import socket
import random
import threading

HOST = 'localhost'
PORT = 12345

players = {}
addresses = []
turn_index = 0
game_running = False

def send_message(message, addr):
    server_socket.sendto(message.encode(), addr)

def draw_card():
    return random.randint(1, 11)

def handle_message(message, addr):
    global turn_index, game_running

    if addr not in addresses and message.startswith("ENTRAR:"):
        nome = message.split(":")[1]
        players[addr] = {'nome': nome, 'cartas': [], 'parou': False}
        addresses.append(addr)
        send_message(f"MENSAGEM:Bem-vindo, {nome}! Aguardando outros jogadores...", addr)

        if len(players) >= 2 and not game_running:
            game_running = True
            start_game()
    elif addr == addresses[turn_index]:
        if message == "PEDIR_CARTA":
            carta = draw_card()
            players[addr]['cartas'].append(carta)
            total = sum(players[addr]['cartas'])
            send_message(f"CARTA:{carta}", addr)
            send_message(f"MENSAGEM:Total atual: {total}", addr)
            if total > 21:
                send_message("RESULTADO:perdeu", addr)
                players[addr]['parou'] = True
                next_turn()
        elif message == "PARAR":
            players[addr]['parou'] = True
            send_message("MENSAGEM:Você parou. Aguardando os outros jogadores...", addr)
            next_turn()

def next_turn():
    global turn_index, game_running

    if all(p['parou'] for p in players.values()):
        end_game()
        return

    for _ in players:
        turn_index = (turn_index + 1) % len(addresses)
        next_player = players[addresses[turn_index]]
        if not next_player['parou']:
            send_message("MENSAGEM:Sua vez!", addresses[turn_index])
            break

def start_game():
    for addr in addresses:
        carta1 = draw_card()
        carta2 = draw_card()
        players[addr]['cartas'] = [carta1, carta2]
        send_message(f"CARTA:{carta1}", addr)
        send_message(f"CARTA:{carta2}", addr)
        send_message(f"MENSAGEM:Soma atual: {carta1 + carta2}", addr)

    send_message("MENSAGEM:Sua vez!", addresses[turn_index])

def end_game():
    global game_running

    pontuacoes = {
        addr: sum(data['cartas']) if sum(data['cartas']) <= 21 else 0
        for addr, data in players.items()
    }
    vencedor = max(pontuacoes, key=pontuacoes.get)
    nome_vencedor = players[vencedor]['nome']
    for addr in addresses:
        if addr == vencedor:
            send_message("RESULTADO:ganhou", addr)
        else:
            send_message("RESULTADO:perdeu", addr)
        send_message(f"MENSAGEM:O vencedor foi {nome_vencedor}", addr)

    game_running = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"Servidor iniciado em {HOST}:{PORT}")

while True:
    try:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        threading.Thread(target=handle_message, args=(message, addr)).start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        break

server_socket.close()
