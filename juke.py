import time
import RPi.GPIO as GPIO
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
from mpd import MPDClient
import json

class keypad():
 # CONSTANTS
    KEYPAD = [
    [6, 1, 5, 2],
    [9, 3, 9 ,7],
    [0, 0, 8,4],
#    [9, 3, "H" ,7],
#    ["R", 0, 8,4],
]
    COLUMN  = [12, 22, 16, 2]
    ROW = [24, 25, 3 ]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def getKey(self):

        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(len(self.ROW)):
#            print(self.ROW[i])
            GPIO.setup(self.ROW[i], GPIO.IN,pull_up_down=GPIO.PUD_UP)

        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                print("Row :"+str(i))

        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal < 0 or rowVal > 2:
            self.exit()
            return

        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN,pull_up_down=GPIO.PUD_UP)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.LOW)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 0:
                print("COL :"+ str(j))
                colVal=j

        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal > 3:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]

    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN)
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN)

#Init des Vars
credit = 25
playing = 0
selection = 0

#Numero de Digit
  #Credit 4,8
  #Playing 2,3,5
  #Selection 7,6,1

#Init Aff
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

#Fonction for Display
def display():
 StrCredit = f'{credit:02d}'
 StrPlaying = f'{playing:03d}'
 StrSelection = f'{selection:03d}'
 if selection < 10 :
   StrSelection = StrSelection.replace("0", " ")
 if (selection < 100) and (selection>9) :
   StrSelection = ' ' + str(selection)
 seg.text = StrSelection[2]+StrPlaying[0]+StrPlaying[1]+StrCredit[0]+StrPlaying[2]+StrSelection[1]+StrSelection[0]+StrCredit[1]  

def select():
  global selection
  song=client.search('file', selection)
  print(len(song))
  if len(song) > 0 :
    client.findadd('file',song[0]['file'])
  else :
    print('NO SONG')
  selection=0

def printKey(key):
  global selection
  if ( selection < 100 ) and ( selection > 0 ):
    selection=selection*10+int(key)
  if ( selection == 0 ):
    selection=int(key)
  display()
#    seg.text = str(key)
#  time.sleep(0.5)

display()
#time.sleep(3)
#seg.text = "12345678"
#time.sleep(3)
client = MPDClient()               # create client object
client.timeout = 10                # network timeout in seconds (floats allowed), default: None
client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
client.connect("localhost", 6600)  # connect to localhost:6600
print(client.mpd_version)          # print the MPD version

kp = keypad()
while True:
  digit = kp.getKey()
  if digit != None :
    print(digit)
    printKey(digit)
    time.sleep(0.2)

  if client.status()['state'] == 'stop' :
    print('stop')
    client.play()
  if len(client.currentsong()) > 0 :
    playing=int(client.currentsong()['file'].split("-")[0])
    if int(client.status()['song'])>0 :
      client.delete(0)
  else :
    playing=0
  credit=25-int(client.status()['playlistlength'])
  if selection > 99 :
    select();
  display()

  time.sleep(0.05)
client.close()                     # send the close command
client.disconnect()                # disconnect from the server

