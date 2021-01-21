import requests
import sys
import getopt
import json

# arbir json de la tempetatura
f = open('.local/config/hackrf-sensors.json',) #ojo, revisar ruta

# obtencion de los valores del json
data = json.load(f) 

# Crear mensaje via api Slack #

# funcion hacer condicion de la temeptertaura
def main(argv):
    cpu = data['temp_cpu'] #temperatura de la cpu (viene del json)
    temp = data['lim_cpu'] #umbral o limite de la cpu (viene del json)
    if cpu > temp:
        send(argv,cpu)

#funcion para el envio del mensaje cuando la temperatura es alta
def send_slack_message(message):
    payload = '{"text":"%s"}' % message
    response = requests.post('https://hooks.slack.com/services/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', data=payload) #token para un bot de temperatura
    print(response.text)

#funcion para la creacion del mensaje 
def send(argv,cpu):

    message = ' '

    try: opts, args = getopt.getopt(argv, "hm:",["message="])

    except getopt.GetoptError:
        print('Alarma.py -m <message>')
        sys.exit(2)
    if len(opts) == 0:
        message = "Temperatura del umbral de la CPU excedida, " + "CPU a " + str(cpu) + (u'\u2103'.encode("utf-8").decode('latin-1')) # revisar ISO del sistema
    for opt, arg in opts:
        if opt == '-h':
            print('Alarma.py -m <message>')
            sys.exit()
        elif opt in ("-m", "--message"):
            message = arg   
    send_slack_message(message)

if __name__ == "__main__":
    main(sys.argv[1:])