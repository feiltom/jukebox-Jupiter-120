from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
import keypad16 as matrix
import keypad26 as matrix2
import time
import os
from pygame import mixer

#Instantiate mixer
mixer.init()
mixer.music.set_volume(1)

songPath="/home/tfeillant/song/"
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)
#seg.text = "1d.Ec5678"
seg.text = "------"

kb = matrix.keypad_module(0x20,0,0)
kb2 = matrix2.keypad_module(0x22,0,0)
entryLetter=""
entryNumber = 0
songArray=[];
songInPlay="";

def addSong(song):
  global songPath
  if os.path.isfile(songPath+song.lower()+".mp3"):
      seg.text = "-----"
      time.sleep(0.2)
      seg.text[1]=song[0]
      seg.text[2]=song[1]
      seg.text[4]=song[2]
      time.sleep(0.2)
      seg.text = "-----"
      time.sleep(0.2)
      seg.text[1]=song[0]
      seg.text[2]=song[1]
      seg.text[4]=song[2]
      time.sleep(0.2)
      seg.text = "-----"
      time.sleep(0.2)
      seg.text[1]=song[0]
      seg.text[2]=song[1]
      seg.text[4]=song[2]
      time.sleep(0.2)
      seg.text = "-----"
      songArray.append(song)
      print(songArray)
  else:
      seg.text[1]="-"
      seg.text[2]="n"
      seg.text[4]="o"
      time.sleep(1)
      seg.text = "-----"


def readKey():
  global entryLetter 
  global entryNumber 
  global songInPlay
  ch = kb.getch()
  if ch != None:
#    print(ord(ch))
    time.sleep(0.1)
  if ch == None:
    ch = kb2.getch()
  if ch != None:
#    print(ch)
    time.sleep(0.1)
  if ch != None:
    if ch=="R":
      if (entryLetter == ""):
        songInPlay=""
      seg.text = "-----"
      entryLetter = ""
      entryNumber = 0
    if (entryLetter == "") and 64<ord(ch) and ord(ch)<70:
      entryLetter=ch
      if 65<ord(entryLetter) and ord(entryLetter)<69:
        entryLetter=entryLetter.lower()
      seg.text = "-----"
      seg.text[1] = entryLetter
    if (entryLetter != "") and 48<ord(ch) and ord(ch)<58:
#      print(ord(ch)-48)
      if entryNumber <1:
        entryNumber+=ord(ch)-48
        seg.text[2]=ch
      else:
        entryNumber=entryNumber*10+(ord(ch)-48)
        seg.text[4]=ch
  if entryNumber > 9:
    addSong(entryLetter+str(entryNumber))
    entryLetter=""
    entryNumber = 0

def playSong():
  global songInPlay
  global songArray
  global entryLetter
  if entryLetter == "" and songInPlay != "":
      seg.text[1]=songInPlay[0]
      seg.text[2]=songInPlay[1]
      seg.text[4]=songInPlay[2]
  if songInPlay == "" and len(songArray) >0:
    songInPlay=songArray.pop(0)
    mixer.music.load(songPath+songInPlay.lower()+".mp3")
    mixer.music.play()
  if mixer.music.get_busy() == False:
    songInPlay = ""
  if entryLetter == "" and songInPlay == "":
    seg.text = "-----"
while 1:
  readKey()
  playSong()
