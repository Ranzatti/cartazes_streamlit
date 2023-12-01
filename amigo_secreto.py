import random
import openpyxl
import os
import time
import pywhatkit as kt
import pandas as pd
import pyautogui
import keyboard as k
from datetime import datetime
import urllib
import webbrowser as web
import schedule

def amigo_secreto(participantes):
    random.shuffle(participantes)
    amigo = participantes.copy()
    amigo.append(amigo.pop(0))
    combinacao = list(zip(participantes, amigo))
    return combinacao

def enviarZap():
    dados_excel = pd.read_excel('amigosecreto2023.xlsx')

    for i, nome in enumerate(dados_excel['Nome']):
        sorteado = dados_excel.loc[i, "Sorteado"]
        telefone = "+55" + str(dados_excel.loc[i, "Telefone"])

        # pyautogui.click(1200, 500)
        pyautogui.click(600, 500)
        time.sleep(300)

        mensagem = f"""
        Querido(a) _*{nome.upper()}*_,

        A época mais mágica do ano está chegando, e é hora de revelar quem terá a alegria de ser o seu Amigo Oculto! 🌟🎅
        Após um sorteio emocionante, 5 horas de processamento, computadores a mil... o nome que você deverá manter em segredo até a grande troca de presentes é...

        Que rufem os tambores....

        🎉🎁 _*{sorteado.upper()}*_ 🎉🎁

        Agora que o segredo foi revelado, é hora de começar a pensar no presente perfeito para surpreender o seu amigo. 
        Lembre-se de que o valor sugerido para o presente é de R$60,00, mas o mais importante é a criatividade e o carinho envolvidos no gesto.
        Prepare-se para uma noite cheia de risadas, alegria e, é claro, presentes incríveis!

        Mantenha o suspense até o dia da troca, e vamos fazer deste Amigo Oculto um momento inesquecível para todos.

        Desejamos a vocês um Natal cheio de amor, harmonia e ótimas lembranças!

        Abraço
        """

        # print(texto)
        # agora = datetime.now()
        # hora = agora.hour
        # min = agora.minute + 1

        texto = urllib.parse.quote(mensagem)

        web.open("https://web.whatsapp.com/send?phone="+telefone+"&text="+texto)

        # kt.sendwhatmsg(telefone, texto, hora, min, 15)
        # kt.sendwhatmsg_instantly(telefone, texto, 15)
        # pyautogui.click(1200, 980)
        time.sleep(20)
        pyautogui.click(600, 700)
        k.press_and_release('enter')

        print('Enviado com sucesso para ', nome)

def gerar_arquivo():
    print('Gerando Arquivo...')
    lista_participantes = {
                        'Fernanda' : '61992856117',
                        'Marlene' : '34988614573',
                        'Laura' : '34996690025',
                        'Mariana' : '67993244203',
                        'Milania' : '61996993610',
                        'Ricardo' : '34998100025',
                        'Joyce' : '62998651781',
                        'Ariane' : '67981584772',
                        'Eduardo' : '67993090917',
                        'Cirlene' : '34991141424',
                        'Cecilia' : '61992856117',
                        'Marlei' : '61991354006',
                        'Alba' : '34991733739',
                        'Maria Paula' : '61998410397',
                        'Joelma' : '62985889078',
                        'Marco Aurélio' : '61992164119',
                        'Galeno' : '34988680840',
                        'Umilda' : '34999796471',
                        'Victor' : '34988542881',
                        'Raquel' : '34999830025',
                        'Verê' : '34997293063',
                        'Alice' : '34988614573',
                        'Mário' : '34988614573',
                        'João Gabriel' : '61999198248',
                        'Frédérick' : '34996794554',
                        'Matheus' : '34998089988',
                        }
    # lista_participantes = {
    #                             'Ricardo': '34998100025'
    #                             }

    participantes = []
    telefone_participantes = []

    for key, value in lista_participantes.items():
        participantes.append(key)
        telefone_participantes.append(value)

    # Chamar a função amigo_secreto
    nomes = amigo_secreto(participantes)

    tudook = True
    #verificando se a pessoa saiu com ela mesmo
    for nome in nomes:
        if nome[0] == nome[1]:
            print('Sujeito Saiu com ele mesmo, faz de novo: ',nome[0]) 
            tudook = False

    #verificando se o numero de telefone é valido
    for telefone in telefone_participantes:
        if len(telefone) != 11:
            print('Telefone errado:',telefone, len(telefone)) 
            tudook = False

    if tudook:
        # Criar uma instância de Workbook (livro de trabalho)
        workbook = openpyxl.Workbook()

        # Selecionar a folha ativa (por padrão, há uma folha chamada 'Sheet')
        sheet = workbook.active

        # Adicionar dados à folha
        sheet['A1'] = 'Nome'
        sheet['B1'] = 'Telefone'
        sheet['C1'] = 'Sorteado'

        i = 2
        for nome in nomes:
            sheet[f'A{i}'] = nome[0]
            sheet[f'B{i}'] = lista_participantes.get(nome[0])
            sheet[f'C{i}'] = nome[1]
            i = i + 1

        # Salvar o arquivo Excel
        workbook.save('amigosecreto2023.xlsx')

        enviarZap()

        print('Parece que deu tudo certo!')
        return True
    else:
        print('Ops! deu ruim')


clear = lambda: os.system('cls')
clear()

schedule.every().friday.at("02:50").do(gerar_arquivo)

while 1:
    schedule.run_pending()

# if gerar_arquivo():
#     # enviarZap()
#     print('Parece que deu tudo certo!')
# else:
#     print('Ops! deu ruim')