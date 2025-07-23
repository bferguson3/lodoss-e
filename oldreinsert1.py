# reinsert.py for lodoss 1

f = open("lodoss-ben.hdm", "rb")
inby = f.read()
f.close()

class TLWord():
    def __init__(self):
        self.txt = ""
        self.addr = 0
###

lines=[]
f = open("0.txt", "r", encoding="sjis") # tl complete 
#f = open("1.txt", "r", encoding="sjis")
#f = open("2.txt", "r", encoding="sjis")
#f = open("4.txt", "r", encoding="sjis")
#f = open("5.txt", "r", encoding="sjis")
tl = f.readline()
while tl != "":
    l = tl.split("#")
    t = TLWord()
    t.txt = l[0]
    new = []
    c = 0
    while c < len(t.txt):
        ch = ord(t.txt[c])
        if(ch > 0x40) and (ch < 0x5b): #A to Z
            new.append(0x82)
            new.append(ch + 0x1f)
        elif(ch > 0x60) and (ch < 0x7b): #a to z
            new.append(0x82)
            new.append(ch + 0x20)
        elif ch == 0x81: # 8140 = fw space 
            if(ord(t.txt[c+1]) == 0x40):
                new.append(0x81)
                new.append(0x40)
                c += 1
        else:
            if ch <= 0xff:
                new.append(ch)
        c += 1
    t.txt = new 
    t.addr = int(l[1],16)
    tl = f.readline()
    lines.append(t)
f.close()

lines3=[]
f = open("3e.txt", "rb")#, encoding="sjis")
tl = f.read()
f.close()
_tl3 = tl.split(b'\n')

# make words 
i = 0
while i < len(_tl3):
    w = TLWord()
    w.txt = _tl3[i].split(b'#')[0]
    w.addr = _tl3[i].split(b'#')[1]
    lines3.append(w)
    i += 1
    
ct = 0
for a in lines3:
    r = b'\xfa\x56' # fix apostraphes 
    if r in a.txt:
        a.txt = a.txt.replace(r, b'\x81\x65')
    n = 0
    while n < len(a.txt) - 3:
        if(a.txt[n] == ord('{')): # fix {xx} codes
            if(a.txt[n+1] >= ord('0'))and(a.txt[n+1] <= ord('f')):
                ct += 1
                if(a.txt[n+2] == ord('}')):
                    h = int(chr(a.txt[n+1]),16)
                    a.txt = a.txt[:n] + bytes([h]) + a.txt[n+3:]
                elif(a.txt[n+3] == ord('}')):
                    h = (int(chr(a.txt[n+1]),16) * 16) | int(chr(a.txt[n+2]),16)
                    a.txt = a.txt[:n] + bytes([h]) + a.txt[n+4:]
        n += 1
    new = []
    c = 0
    while c < len(t.txt):
        ch = ord(t.txt[c])
        if(ch > 0x40) and (ch < 0x5b): #A to Z
            new.append(0x82)
            new.append(ch + 0x1f)
        elif(ch > 0x60) and (ch < 0x7b): #a to z
            new.append(0x82)
            new.append(ch + 0x20)
        elif ch == 0x81:
            if(ord(t.txt[c+1]) == 0x40):
                new.append(0x81)
                new.append(0x40)
                c += 1
        else:
            if ch <= 0xff:
                new.append(ch)
        c += 1
    a.txt = new 
    print(a.txt)
print(ct, "script lines found")

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

print(ct,"yesno fixed")
f = open("lodoss-game_e.hdm", "wb")
f.write(game)
f.close()

k = 0
while k < len(lines):
    s = lines[k]
    bc = s.addr - len(bytes(s.txt))
    inby = inby[:bc] + bytes(s.txt) + bytes([ord('#'), 0x0d, 0x0a]) + inby[bc +3+ len(bytes(s.txt)):]
    k += 1

k = 0
while k < len(lines3):
    s = lines3[k]
    #print(int(s.addr,16))
    bc = int(s.addr,16) - len(bytes(s.txt))
    inby = inby[:bc] + bytes(s.txt) + bytes([ord('#'), 0x0d, 0x0a]) + inby[bc +3+ len(bytes(s.txt)):]
    k += 1

f = open ("lodoss-ben_e.hdm", "wb")
f.write(bytes(inby))
f.close()