import json,jaconv,os,sys

f = open("lodoss1_dump.json", "r")
j = f.read()
f.close()
data = json.loads(j)

class TLWord():
    def __init__(self):
        self.txt = ""
        self.addr = 0
###

jlines=[]
tct = 0
nct = 0
for w in data["words"]:
    nct += 1
    if w["translation"] != "":
        tct += 1
        a = TLWord()
        try:
            _d = w["translation"].encode("sjis")
            if(len(_d) > w["size"]):
                print("size mismatch error", len(_d), w["size"],":",w["translation"])
                sys.exit()
            else:
                # size ok
                ovr = 0
                while len(_d) < w["size"]:
                    _d += b'\x20'
                    ovr += 1
                print(_d.decode("sjis"), "unused", ovr)
                a.txt = _d 
                a.addr = int(w["address"],16)
                jlines.append(a)
        except Exception as e:
            print(e)
print(tct,"translated of",nct, "{:01}".format(tct/nct*100)[:5]+"%")

# fix all yes/no
yn = bytes([0x82, 0xCD, 0x82, 0xA2, 0x23, 0x82, 0xA2, 0x82, 0xA2, 0x82, 0xA6, 0x23])
#newyn = bytes([0x82, 0x78, 0x81, 0x40, 0x23, 0x82, 0x6D, 0x81, 0x40, 0x81, 0x40, 0x23])
newyn = bytes([0x82, 0x78, 0x82, 0x85, 0x82, 0x93, 0x23, 0x82, 0x6D, 0x82, 0x8F, 0x23])
f = open("lodoss-game.hdm", "rb")
game = f.read()
f.close()
i = 0
ct = 0
while i < len(game):
    n = 0
    match = False
    b = 0
    if(game[i] == yn[n]):
        match = True
        while n < len(yn):
            if(game[i+b] != yn[n]):
                match = False
                break
            n += 1
            b += 1
    if(match == True):
        ct += 1
        game = game[:i] + newyn + game[i+len(newyn):]
        i += b
    i += 1
print(ct,"yesno fixed in game disk")
f = open("lodoss-game_e.hdm", "wb")
f.write(game)
f.close()

f = open("lodoss-ben.hdm", "rb")
inby = f.read()
f.close()

## old insertion for block 0
lines=[]
f = open("0.txt", "r", encoding="sjis") # tl complete 
tl = f.readline()
while tl != "":
    l = tl.split("#")
    t = TLWord()
    t.txt = l[0]
    new = []
    c = 0
    #print(t.txt, len(bytes(t.txt, encoding="sjis")))
    t.txt = bytes(t.txt, encoding="sjis")

    while c < len(t.txt):
        ch = t.txt[c]
        if(ch > 0x40) and (ch < 0x5b): #A to Z
            new.append(0x82)
            new.append(ch + 0x1f)
        elif(ch > 0x60) and (ch < 0x7b): #a to z
            new.append(0x82)
            new.append(ch + 0x20)
        elif ch == 0x81: # 8140 = fw space 
            if(t.txt[c+1] == 0x40):
                new.append(0x81)
                new.append(0x40)
                c += 1
        else:
            if ch <= 0xff:
                new.append(ch)
        c += 1
    t.txt = new 
    t.addr = int(l[1],16) #- len(bytes(t.txt))
    #print(bytes(t.txt), len(t.txt), hex(t.addr))
    tl = f.readline()
    lines.append(t)
f.close()


k = 0
while k < len(lines):
    s = lines[k]
    bc = s.addr - len(bytes(s.txt))
    inby = inby[:bc] + bytes(s.txt) + bytes([ord('#'), 0x0d, 0x0a]) + inby[bc +3+ len(bytes(s.txt)):]
    k += 1

k = 0
while k < len(jlines):
    s = jlines[k]
    bc = s.addr 
    inby = inby[:bc] + bytes(s.txt) + bytes([ord('#'), 0x0d, 0x0a]) + inby[bc + 3 + len(bytes(s.txt)):]
    k += 1

f = open ("lodoss-ben_e.hdm", "wb")
f.write(bytes(inby))
f.close()