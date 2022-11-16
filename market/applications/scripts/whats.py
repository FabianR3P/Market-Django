import pywhatkit
from datetime import datetime
from datetime import timedelta

try:
    #eniando mensjae con pyehatkit
    now = datetime.now()
    hour = now.hour
    minute = now.minute + 1
    msg="Te estas quedando sin panecito, Alerta de Bot"
    pywhatkit.sendwhatmsg("+525570822021",msg,hour,minute)
    print("abriendo.... escaneee codigo QR")

except:
    print("No se pudo encontrar")
