
# Jogo de Cartas "21" com Sockets UDP

Este projeto implementa o jogo de cartas "21" (Blackjack simplificado) utilizando a comunicação cliente-servidor via sockets UDP em Python.

## 🎮 Como funciona

- O servidor gerencia o jogo, sorteia cartas e controla os turnos.
- Os jogadores se conectam como clientes via terminal e jogam em sequência.
- Ganha quem chegar mais próximo de 21 sem ultrapassar.

## 🚀 Execução

### Requisitos
- Python 3.x

### Instruções

1. Abra dois terminais ou mais (para vários jogadores).
2. Em um terminal, inicie o servidor:
   ```bash
   python servidor.py
   ```
3. Em cada outro terminal, inicie um cliente:
   ```bash
   python cliente.py
   ```
   Digite seu nome quando solicitado.

4. O jogo começará automaticamente quando pelo menos 2 jogadores estiverem conectados.

## 📜 Comandos do Cliente

- `PEDIR_CARTA`: Solicita nova carta.
- `PARAR`: Para de receber cartas.

## 📦 Estrutura de Arquivos

- `servidor.py`: Código do servidor.
- `cliente.py`: Código do cliente.
- `README.md`: Este arquivo de instruções.

## 🧑‍💻 Desenvolvido para fins acadêmicos
