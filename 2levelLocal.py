import sys
#0 is strong not taken 1 is weak not taken 2 is weak taken 3 is strongly taken.
misprediction_count = count = 0
PHT_Entries = 1024
LHT_Entries = 1024
PHT = []
LHT = []

statemax = sys.argv[1]
statemax = 2 ** int(statemax)
statemid = statemax/2
statemax -= 1
statemin = 0

for index in range(PHT_Entries):
    PHT.append(0)
for index in range(LHT_Entries):
    LHT.append(0)

with open("branch-trace-gcc.trace", 'rb') as tracefile:
    for line in tracefile:
        if line.strip() == '':
            continue
        pc, status = line.split()
        pc_lht = int(pc) % LHT_Entries
        # pc_pht = LHT[pc_lht]

        count += 1
        if 'T' in status:
            if PHT[LHT[pc_lht]] < statemid:                        #if branch is 'Taken' but we had predicted 'Not Taken'
                if PHT[LHT[pc_lht]] < statemin:
                    PHT[LHT[pc_lht]] = statemin
                misprediction_count += 1               #increment misprediction count
            else:
                if PHT[LHT[pc_lht]] > statemax:
                    PHT[LHT[pc_lht]] = statemax
            PHT[LHT[pc_lht]] += 1
            LHT[pc_lht] = (((LHT[pc_lht] << 1) | 0x01) & 0x000003ff)


        if 'N' in status:
            if PHT[LHT[pc_lht]] < statemid:                        #if branch is 'Not Taken' and we correctly predicted 'Not Taken'
                if PHT[LHT[pc_lht]] < statemin:
                    PHT[LHT[pc_lht]] = statemin
            else:
                if PHT[LHT[pc_lht]] > statemax:
                    PHT[LHT[pc_lht]] = statemax
                misprediction_count += 1            
            PHT[LHT[pc_lht]] -= 1           
            LHT[pc_lht] = ((LHT[pc_lht] << 1) & 0x000003fe)

print (100 - (float(misprediction_count)*100/float(count)))