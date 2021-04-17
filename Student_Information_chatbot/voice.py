import os

f = open("voice.txt", 'r+')
text = f.read()
os.system("echo \""+text+"\" | festival --tts")


