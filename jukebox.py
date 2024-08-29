import keypad16 as matrix
import keypad26 as matrix2
import time
import os
from pygame import mixer
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
PANELCODE  = [['6','4','c'], # KEYCOL0
            ['8','2','b'], # KEYCOL1
            ['7','9','0'], # KEYCOL2
            ['5','e','1'], # KEYCOL2
            ['3','d','a']] # KEYCOL3
#Instantiate mixer
mixer.init()
mixer.music.set_volume(1)

songPath="/home/jukebox/song/"
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1,contrast=255)
print("Created device")
LedCanvas = canvas(device)
seg = ["-","-","-","-"]

kb = matrix.keypad_module(0x20,0,0)
kb2 = matrix2.keypad_module(0x20,1,0)
entryLetter=""
entryNumber = 0
songArray=[];
songInPlay="";
ledinitial="---"

def printseg(leddisplay):
  global ledinitial
  if leddisplay!=ledinitial:
    with LedCanvas as draw:
      for y in range(2,7):
        for x in range(0,3):
          draw.point((x,y), fill="black")
          if PANELCODE[y-2][x]==leddisplay[0].lower() or PANELCODE[y-2][x]==leddisplay[1] or PANELCODE[y-2][x]==leddisplay[2]:
              draw.point((x,y), fill="white")
              time.sleep(0.1)
#              print(str(x)+","+str(y))
#              print(PANELCODE[y-2][x])
#              print(seg[1]+seg[2]+seg[3])
          ledinitial=leddisplay

def addSong(song):
  global songPath
  if os.path.isfile(songPath+song.lower()+".mp3"):
      printseg("---")
      time.sleep(0.2)
      printseg(song[0]+song[1]+song[2])
      time.sleep(0.2)
      printseg("---")
      time.sleep(0.2)
      printseg(song[0]+song[1]+song[2])
      time.sleep(0.2)
      printseg("---")
      time.sleep(0.2)
      printseg(song[0]+song[1]+song[2])
      time.sleep(0.2)
      songArray.append(song)
      print(songArray)
  else:
      printseg("357")
      time.sleep(0.2)
      printseg("bcd")
      time.sleep(0.2)
      printseg("357")
      time.sleep(0.2)
      printseg("bcd")
      time.sleep(0.2)
      printseg("357")
      time.sleep(0.2)


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
#    print(ord(ch))
    time.sleep(0.1)
  if ch != None:
    if ch=="R":
      if (entryLetter == ""):
        songInPlay=""
      seg[1] = "-"
      entryLetter = ""
      entryNumber = 0
    if (entryLetter == "") and 64<ord(ch) and ord(ch)<70:
      entryLetter=ch
      if 65<ord(entryLetter) and ord(entryLetter)<69:
        entryLetter=entryLetter.lower()
      seg[1] = seg[2] = seg[3] ="-"
      seg[1] = entryLetter
      printseg(seg[1] + seg[2] + seg[3])
    if (entryLetter != "") and 47<ord(ch) and ord(ch)<58:
#      print(ord(ch)-48)
      if entryNumber <0:
        entryNumber+=ord(ch)-48
        seg[2]=ch
        printseg(seg[1] + seg[2] + seg[3])
      else:
        entryNumber=entryNumber*10+(ord(ch)-48)
        seg[3]=ch
        printseg(seg[1] + seg[2] + seg[3])
  if entryNumber > 9:
    addSong(entryLetter+str(entryNumber))
    entryLetter=""
    entryNumber = 0

def playSong():
  global songInPlay
  global songArray
  global entryLetter
  if entryLetter == "" and songInPlay != "":
      seg[1]=songInPlay[0]
      seg[2]=songInPlay[1]
      seg[3]=songInPlay[2]
      printseg(seg[1] + seg[2] + seg[3])
  if songInPlay == "" and len(songArray) >0:
    songInPlay=songArray.pop(0)
    mixer.music.load(songPath+songInPlay.lower()+".mp3")
    mixer.music.play()
  if mixer.music.get_busy() == False:
    songInPlay = ""
  if entryLetter == "" and songInPlay == "":
    seg[1] = seg[2] =seg[3] = "-"
    printseg(seg[1] + seg[2] + seg[3])

printseg("a10")
time.sleep(0.2)
printseg("b32")
time.sleep(0.2)
printseg("c54")
time.sleep(0.2)
printseg("d76")
time.sleep(0.2)
printseg("e98")
time.sleep(0.2)

while 1:
  readKey()
  playSong()