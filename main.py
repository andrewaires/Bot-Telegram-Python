import telebot
import requests

with open('key.txt', 'r') as f:
    chave = f.read().strip()
bot = telebot.TeleBot(chave)

requisicao = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL')
requisicao_dic = requisicao.json()

dolar = requisicao_dic['USDBRL']['ask']
euro = requisicao_dic['EURBRL']['ask']
bitcoin = requisicao_dic['BTCBRL']['ask']

@bot.message_handler(commands = ['dolar'])
def handler_dolar(entrada):
    cotacao_dolar = float(dolar)
    bot.send_message(entrada.chat.id, f'O preço atual do Dólar é de R${cotacao_dolar:.2f}'.replace('.', ','))

@bot.message_handler(commands = ['btc'])
def handler_btc(entrada):
    cotacao_bitcoin = float(bitcoin)
    cotacao_bitcoin_formatada = format(cotacao_bitcoin, ",.1f").replace(".", ",")
    cotacao_bitcoin_formatada = cotacao_bitcoin_formatada.replace(",", ".", cotacao_bitcoin_formatada.count(',') - 1)
    bot.send_message(entrada.chat.id, f'O preço do Bitcoin é de R${cotacao_bitcoin_formatada}')

@bot.message_handler(commands = ['eur'])
def handler_eur(entrada):
    cotacao_euro = float(euro)
    bot.send_message(entrada.chat.id, f'O preço do Euro é de R${cotacao_euro:.2f}'.replace('.', ','))

def verificar(entrada):
    return True

@bot.message_handler(func=verificar)
def mensagem(entrada):
    texto = '''
    Clique em qual cotação você quer saber:
    /dolar - Cotação atual do Dólar
    /btc - Cotação atual do Bitcoin
    /eur - Cotação atual do Euro
    '''
    chat_id = entrada.chat.id
    bot.send_message(chat_id, texto)

bot.polling()