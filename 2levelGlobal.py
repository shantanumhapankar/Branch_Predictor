from time import sleep
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

with open("branch-trace-gcc.trace", 'rb') as tracefile:
    for line in tracefile:
        if line.strip() == '':
            continue
        pc, status = line.split()
        pc_pht = int(pc) % 1024
        count += 1
        if 'T' in status:
            if PHT[GHR] < statemid:                        #if branch is 'Taken' but we had predicted 'Not Taken'
                if PHT[GHR] < statemin:
                    PHT[GHR] = statemin
                misprediction_count += 1            #increment misprediction count
            else:
                if PHT[GHR] > statemax:
                    PHT[GHR] = statemax
            PHT[GHR] += 1                       #increment status counter
            GHR = (((GHR << 1) | 0x01) & 0x000003ff)


        if 'N' in status:
            if PHT[GHR] < statemid:                        #if branch is 'Not Taken' and we correctly predicted 'Not Taken'
                if PHT[GHR] < statemin:
                    PHT[GHR] = statemin
            else:
                if PHT[GHR] > statemax:
                    PHT[GHR] = statemax
                misprediction_count += 1
            PHT[GHR] -= 1             
            GHR = ((GHR << 1) & 0x000003fe)

print (100 - (float(misprediction_count)*100/float(count)))