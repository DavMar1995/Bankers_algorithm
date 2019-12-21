from collections import namedtuple
NUM_PROCESS = 5
NUM_RESOURCE = 3
Available = [10, 5, 7]
ProcessList = []


    def __init__(self, A, M):
        ResAlloc = namedtuple('ResAlloc', ['allocation', 'max'])
        self.resource = []
        for i in range(0, NUM_RESOURCE):
            self.resource.append(ResAlloc(A[i], M[i]))

# safty algorithm
def safty():
    print("=== Safty algorithm starts!")
    
    # 1. Work =Available, Finish[i] = false for i = 0,1,...,n-1
    tempAvail = Available
    done = [False, False, False, False, False]
    sequence = []
    
    # 2. Find an i such that both
    #                 a. Finish[i] = false
    #                 b. Need i => Work
    #       If no such i exists, goto Step 4
    qualifed = False
    while qualifed is True:
        pid = 0
        qualifed = False
        # search in processes
        for process in ProcessList:
            # haven't been finished yet
            if done[pid] is False:
                counter = 0
                availID = 0
                for resource in process:
                    # b. Need i => Work
                    if resource.max - resource.allocation >= tempAvail[availID]:
                        counter += 1
                    availID += 1
                if counter is NUM_RESOURCE:
                    qualifed = True
                    break
            pid += 1
        # 3. Work = Work + Allocation i
        #    Finish[i] = true
        #    goto Step 2
        if qualifed is True:
            for i in range(0, NUM_RESOURCE):
                tempAvail[i] +=  ProcessList[pid][i].allocation
            done[pid] is True
            sequence.append(pid)
    # 4. If Finish[i] == true for all i => Safe state.
    for i in done:
        if done[i] is False:
            return False
    return sequence
            
    



# print system status
def printStatus():
    print("Available status: ({}, {}, {})".format(
        Available[0], Available[1], Available[2]))
    print("     Resource Allocation | Max Request | Remaining Needs:")
    counter = 0
    for i in ProcessList:
        print("Process #{}: ".format(counter), end="")
        counter = counter + 1

        # Allocation
        for j in i.resource:
            print(f"  {j.allocation}", end="")
        print("    | ", end="")

        # Max
        for j in i.resource:
            print(f"  {j.max}", end="")
        print("   | ", end="")

        # Needs
        for j in i.resource:
            print(f"  {j.max- j.allocation}", end="")

        print()


# main

print("=== Banker's algorithm starts!\n")
print("Initial System states: ")

#* append the data into `ProcessList`
p0 = Process([0, 1, 0], [7, 5, 3])
ProcessList.append(p0)

p1 = Process([2, 0, 0], [3, 2, 2])
ProcessList.append(p1)

p2 = Process([3, 0, 2], [9, 0, 2])
ProcessList.append(p2)

p3 = Process([2, 1, 1], [2, 2, 2])
ProcessList.append(p3)

p4 = Process([0, 0, 2], [4, 3, 3])
ProcessList.append(p4)

#* print the status
printStatus()

result = safty()
if result is True:
    print(f'Safe! Find the sequence: <', end="")
    for i in result:
        print(f'  {i}', end='')
    print(">")
else: 
    print('Unsafe!')