import json
import requests

PROPETIES = 'telegramkeys.txt'

class TelegramBot():
    print('inicio funcion')

    def __init__(self):
        self._token = None
        self._group = None
        self._chanel = None
        with open(PROPETIES,'r') as file_reader:
            params = json.load(file_reader)
            self._token = params['token']
            self._group = params['group']
            self._channel = params['channel']

    def get_me(self):
        url = f"https://api.telegram.org/bot{self._token}/getMe"
        response = requests.get(url)
        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        return None

    def get_updates(self):
        url = f"https://api.telegram.org/bot{self._token}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        return None

    def send_message_to_group(self,message):
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        data = {"chat_id" : self._group, "text":message}
        response = requests.post(url, data=data)
        if response.satus_code == 200:
            salida = json.loads(response.text)
            return salida
        return None

if __name__ =="__main__":
    tb = TelegramBot()
    print(tb.get_me())
    print(tb.get_updates())
    print(tb.send_message_to_group("Hola grupo se han ingresado 315 bolillos a las 13:01 hrs"))

    
#Token del bot de prueba : 5696573496:AAECNr27o0nvf0-NQDQqAt9X3n6enRo2_8s
##group:  -692188688
#Token del bot de MauPan : 5768298048:AAFyjsbxKprBNpSw_VldOM8BxOuEMzNMU0Q
##group: -866884165
