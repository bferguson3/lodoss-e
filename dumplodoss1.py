#!/usr/bin/python3

# warning - 9 lines do not dump correctly and need manual fixing

import os,sys,json

f = open("../lodoss1_scen_eng.fdi", "rb")
inby = f.read()
f.close()

ranges = [
#(0x10a100,0x10aab7),
#(0x114d00,0x1150ff),
#(0x115e00,0x11bc20),
#(0x11bd00,0x125fff),
#(0x127000,0x12bfff),
#(0x126900,0x126f2f),
(0x10b100, 0x10bab5),
(0x115d00, 0x1160ff),
(0x116e00, 0x1193f3),
(0x119400, 0x11cc20),
(0x11cd00, 0x123af0),
(0x123b00, 0x126ff1),
(0x127900, 0x127f2b),
(0x128000, 0x12cfff)
]

class TLWord():
    def __init__(self):
        self.address = 0x0
        self.text = ""
        self.translation = ""
        self.size = 0
    ###
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4,
            ensure_ascii=False)
    ###
###
word = TLWord()
outfiles = []
for r in ranges:
    file = []
    n = r[0]
    line = []
    while n < r[1]+1:
        if(inby[n] < 0x20):
            if(inby[n] == 0x0d):
                if(inby[n+1] == 0x0a):
                    word.text = line 
                    file.append(word)
                    word = TLWord()
                    line = []
                    n += 1
            else:
                line.append(ord('{'))
                line.append(ord(hex(inby[n])[2:][0]))
                if(inby[n] > 15):
                    line.append(ord(hex(inby[n])[2:][1]))
                line.append(ord('}'))
        else:
            if(inby[n] == 0x23):
                word.address = hex(n - len(line))
                word.size = len(line)
            else:
                line.append(inby[n])
        n += 1
    outfiles.append(file)

# write json blob 
outstr = "{\n\"words\":["
i = 0 
while i < len(outfiles):
    for k in outfiles[i]:
        try:
            k.text = bytes(k.text).decode("sjis")#.encode("sjis")
        except:
            #print(k.text, i)
            try:
                k.text = "" + bytes(k.text[2:]).decode("sjis")
            except:    
                try:
                    k.text = "{8x}" + bytes(k.text[1:]).decode("sjis")
                except:
                    k.text = "SJIS Decoding error!" + str(k.text)
        outstr += k.toJSON() + ",\n"
    i += 1
outstr = outstr[:len(outstr)-2]
outstr += "\n]\n}"
print(outstr)