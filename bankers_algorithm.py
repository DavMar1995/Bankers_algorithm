from collections import namedtuple
import sys

class Process:
    def __init__(self, A, M):
        ResAlloc = namedtuple('ResAlloc', ['allocation', 'max'])
        self.resourceList = []
        for i in range(0, NUM_RESOURCE):
            self.resourceList.append(ResAlloc(A[i], M[i]))

# safty algorithm


def safty():
    print("=== Safty algorithm starts!\n")

    # 1. Work =Available, Finish[i] = false for i = 0,1,...,n-1
    tempAvail = []
    for i in Available:
        tempAvail.append(i)
    done = [False, False, False, False, False]
    sequence = []

    # 2. Find an i such that both
    #                 a. Finish[i] = false
    #                 b. Need i => Work
    #       If no such i exists, goto Step 4
    running = True
    while running == True:
        pid = 0
        running = False
        # * search in processes
        for process in ProcessList:
            # * haven't been finished yet
            if done[pid] == False:
                counter = 0
                availID = 0
                for resource in process.resourceList:
                    # b. Need i => Work
                    if resource.max - resource.allocation <= tempAvail[availID]:
                        counter += 1
                    availID += 1
                # * 3. Work = Work + Allocation i
                if counter == NUM_RESOURCE:

                    availID = 0
                    # * Finish[i] = true
                    for resource in process.resourceList:
                        tempAvail[availID] += resource.allocation
                        availID += 1

                    # * goto Step 2
                    running = True
                    # * set this process == done
                    done[pid] = True
                    # * add this process to sequence
                    sequence.append(pid)
                    break
            pid += 1
        # 3. Work = Work + Allocation i
        #    Finish[i] = true
        #    goto Step 2
    # 4. If Finish[i] == true for all i => Safe state.
    printDone = False
    for i in done:
        if not i:
            printDone = True
    if printDone == True:
        for i in range(0, len(done)):
            if done[i] == True:
                print(f'process #{i} == done!')
            else:
                print(f'process #{i} isn\'t done!')
        return False
    return sequence


def resourceRequest(first=True):
    global Available, InitAvail

    if first:
        Available = InitAvail

    print("Resource-Request algorithm starts!\n")

    # * print the init `Available`
    printStatus(Available)

    print("Request! Enter Procss No: ", end='')

    # * scan the request
    pid = int(input())
    request = []
    for i in range(0, NUM_RESOURCE):
        print(f'Enter request resource #{i} = ', end='')
        request.append(int(input()))

    requestRes = 0
    for i in range(0, NUM_RESOURCE):
        if request[i] > Available[i]:
            # * bigger than `Available`
            requestRes = 1
            break
        if request[i] > (ProcessList[pid].resourceList[i].max - ProcessList[pid].resourceList[i].allocation):
            # * bigger than `Need`
            requestRes = 2
            break
    if requestRes == 1:
        print('Request > Available! Process must wait!')
        if(not continueProgram()):
            sys.exit()
        else:
            resourceRequest(False)
    elif requestRes == 2:
        print('Request > Need! Reject!')
        if(not continueProgram()):
            sys.exit()
        else:
            resourceRequest(False)

    for i in range(0, NUM_RESOURCE):
        Available[i] -= request[i]
        ProcessList[pid].resourceList[i] = ProcessList[pid].resourceList[i]._replace(
            allocation=ProcessList[pid].resourceList[i].allocation + request[i])

    print('Pretend to grant the requet')

    printStatus(Available)

    result = safty()
    if not result:
        print('Unsafe!')
        print('Unsafe, Do not grant! Restore the allocation state!')
        if continueProgram():
            resourceRequest(False)
        else:
            sys.exit()
    else:
        print(f'Safe! Find the sequence: <', end="")
        for i in result:
            print(f' {i},', end='')
        print(">\n")
        print('Safe! Grant the request!')
        if not continueProgram():
            sys.exit()
        else:
            resourceRequest(False)

def continueProgram():
    print('Continue the Banker\'s algorithm? (Yes = y or Y) ', end='')
    key = input()
    if key == 'y' or key == 'Y':
        return True
    print('Bye! End of Banker\'s algorithm!')
    sys.exit()

# * print system status
def printStatus(avail):
    print(f'Available status: ({avail[0]}, {avail[1]}, {avail[2]})')
    print("     Resource Allocation | Max Request | Remaining Needs:")
    counter = 0
    for i in ProcessList:
        print("Process #{}: ".format(counter), end="")
        counter = counter + 1

        # Allocation
        for j in i.resourceList:
            print(f"  {j.allocation}", end="")
        print("    | ", end="")

        # Max
        for j in i.resourceList:
            print(f"  {j.max}", end="")
        print("   | ", end="")

        # Needs
        for j in i.resourceList:
            print(f"  {j.max - j.allocation}", end="")

        print()


# * main
print("=== Banker's algorithm starts!\n")
print("Initial System states: ")

NUM_PROCESS = 5
NUM_RESOURCE = 3
# Available = [10, 5, 7]
InitAvail = [3, 3, 2]
Available = []

for i in InitAvail:
    Available.append(i)

ProcessList = []

# * append the data into `ProcessList`
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

# * print the status
printStatus(Available)

result = safty()
if not result:
    print('Unsafe!')
else:
    print(f'Safe! Find the sequence: <', end="")
    for i in result:
        print(f' {i},', end='')
    print(">\n")

    resourceRequest()

