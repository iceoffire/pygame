import serial

porta = "/dev/ttyUSB0"

conexao = serial.Serial(porta, 9600)

opcao = 0

while opcao != '2':
    opcao = input('coloque a opcao: ')
    if opcao != '2':
        conexao.write(opcao);
        