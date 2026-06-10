f1 = open("scenario_orig.hdm", "rb")
f1by = f1.read()
f1.close()
f2 = open("scenario_orig_e.hdm", "rb")
f2by = f2.read()
f2.close()

fail = False
i = 0
while i < len(f1by):
    if f1by[i] == 0x23:
        #if f1by[i+1] == 0x0d:
        #    if f1by[i+2] == 0xa:
                    #print(hex(i))
        if f2by[i] != 0x23:# or f2by[i+1] != 0x0d or f2by[i+2] != 0x0a:
            print("FAILURE to confirm in new disk @", hex(i))
            fail = True
    i += 1
if not fail:
    print("0x23 check OK")