import sys

#0 is strong not taken 1 is weak not taken 2 is weak taken 3 is strongly taken.
misprediction_count = count = 0
PHT_Entries = 1024
PHT = []
for index in range(PHT_Entries):
    PHT.append(0)

# print "The counter bits are: " , str(sys.argv[1])
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
            if PHT[pc_pht] < statemid:                        #if branch is 'Taken' but we had predicted 'Not Taken'
                if PHT[pc_pht] < statemin:
                    PHT[pc_pht] = statemin
                misprediction_count += 1                      #increment misprediction count
            else:
                if PHT[pc_pht] > statemax:
                    PHT[pc_pht] = statemax
            PHT[pc_pht] += 1             

        if 'N' in status:
            if PHT[pc_pht] < statemid:                        #if branch is 'Not Taken' and we correctly predicted 'Not Taken'
                if PHT[pc_pht] < statemin:
                    PHT[pc_pht] = statemin
            else:
                if PHT[pc_pht] > statemax:
                    PHT[pc_pht] = statemax
                misprediction_count += 1            
            PHT[pc_pht] -= 1             


print (100 - (float(misprediction_count)*100/float(count)))