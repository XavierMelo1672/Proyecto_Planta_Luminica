import sys
import smbus
import time
from firebase import firebase
 
# Define some constants from the datasheet
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
ONE_TIME_HIGH_RES_MODE = 0x20
 
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

firebase = firebase.FirebaseApplication('https://ciberluz1raspberrypi.firebaseio.com/', None)
key = "AIzaSyD2VN-FqNG1muprYxh43Y207UwXOvm85P0"

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
  return ((data[1] + (256 * data[0])) / 1.2)
 
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE)
  return convertToNumber(data)
 
def main():

  cardinalmuestra = firebase.get('/cardinal/2/muestra',None)
  j=cardinalmuestra+1
  firebase.put('/cardinal/2','muestra',j)
  muestras=str(j)
  firebase.put('/cardinal/1','contador',0)
  estado=firebase.get('/estado/estado',None)
  while (estado==1):
    estadosensor=firebase.get('/estado/estadosensor',None)
    if(estadosensor==1):
      print ('Nivel de luz: ' + str(readLight()) + ' lux')
      hora = time.strftime("%H:%M:%S")
      fecha = time.strftime("%d/%m/%y")
      horastring = str(hora)
      fechastring = str(fecha)
      horafechastring=fechastring+"-"+horastring
      luz= readLight()
      cardinal = firebase.get('/cardinal/1/contador',None)
      i=cardinal+1
      uid= str(i)
      data = {"fechayhora":horafechastring, "fecha": fechastring, "hora": horastring, "luz": luz}
      firebase.post('/muestras/sensorluzmuestra'+muestras+'/'+uid, data)
      firebase.put('/cardinal/1','contador',i)
      #firebase.put('/luz/'+uid,'fechayhora',horafechastring)
      #firebase.put('/luz/'+uid,'fecha',fechastring)
      #firebase.put('/luz/'+uid,'hora',horastring)
      #firebase.put('/luz/'+uid,'lux',luz)
      #time.sleep(0.5)
      
    else:
      print('Sensor apagado')
      
   
 
if __name__=="__main__":
   main()
