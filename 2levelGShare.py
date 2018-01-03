import sys

#0 is strong not taken 1 is weak not taken 2 is weak taken 3 is strongly taken.
misprediction_count = count = 0
PHT_Entries = 1024
PHT = []
GHR = 0x000000000
for index in range(PHT_Entries):
    PHT.append(0)

statemax = sys.argv[1]
statemax = 2 ** int(statemax)
statemid = statemax/2
statemax -= 1
statemin = 0

# for i in range(8):
#     GHR = ((GHR << 1) or 0x01)
#     print GHR

with open("branch-trace-gcc.trace", 'rb') as tracefile:
    for line in tracefile:
        if line.strip() == '':
            continue
        pc, status = line.split()
        pc_pht = int(pc) % 1024
        gshare = (pc_pht ^ GHR)
        count += 1
        if 'T' in status:
            if PHT[gshare] < statemid:                        #if branch is 'Taken' but we had predicted 'Not Taken'
                if PHT[gshare] < statemin:
                    PHT[gshare] = statemin
                misprediction_count += 1            #increment misprediction count
            else:
                if PHT[gshare] > statemax:
                    PHT[gshare] = statemax
            PHT[gshare] += 1                       #increment status counter
            GHR = (((GHR << 1) | 0x01) & 0x000003ff)


        if 'N' in status:
            # print GHR, PHT[GHR], status
            if PHT[gshare] < statemid:                        #if branch is 'Not Taken' and we correctly predicted 'Not Taken'
                if PHT[gshare] < statemin:
                    PHT[gshare] = statemin
            else:
                if PHT[gshare] > statemax:
                    PHT[gshare] = statemax
                misprediction_count += 1
            PHT[gshare] -= 1             
            GHR = ((GHR << 1) & 0x000003fe)

print (100 - (float(misprediction_count)*100/float(count)))