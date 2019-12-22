from collections import namedtuple


class Process:
    def __init__(self, A, M):
        ResAlloc = namedtuple('ResAlloc', ['allocation', 'max'])
        self.resourceList = []
        for i in range(0, NUM_RESOURCE):
            self.resourceList.append(ResAlloc(A[i], M[i]))

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
    running = True
    while running is True:
        pid = 0
        running = False
        # * search in processes
        for process in ProcessList:
            # * haven't been finished yet
            if done[pid] is False:
                counter = 0
                availID = 0
                print(f'process #{pid}: {process}, {type(process)}')
                for resource in process.resourceList:
                    # b. Need i => Work
                    print(f'c: {counter}, aID: {availID} ')
                    print(
                        f'   a: {resource.allocation}, m: {resource.max}, ', end='')
                    print(
                        f'n: {resource.max - resource.allocation}, avail: {tempAvail[availID]} ', end='')
                    print(
                        f'=> {resource.max - resource.allocation <= tempAvail[availID]}')
                    if resource.max - resource.allocation <= tempAvail[availID]:
                        counter += 1
                    availID += 1
                    print(f' => c: {counter}, aID: {availID}\n')
                # * 3. Work = Work + Allocation i
                if counter is NUM_RESOURCE:

                    availID = 0
                    # * Finish[i] = true
                    for resource in process.resourceList:
                        # @debug
                        # print(
                        #     f'Before => availID: {availID}, tempAllocation: {tempAvail[availID]}, allocation: {ProcessList[pid].resourceList[availID].allocation}')

                        tempAvail[availID] += resource.allocation
                        # @debug
                        # print(
                        #     f'After: availID: {availID}, tempAllocation: {tempAvail[availID]}\n')
                        availID += 1

                    # * goto Step 2
                    running = True
                    # * set this process is done
                    done[pid] = True
                    # * add this process to sequence
                    sequence.append(pid)

                    # @debug: print(f'done: {done}, sequence: {sequence}\n')
                    break
            pid += 1
        # 3. Work = Work + Allocation i
        #    Finish[i] = true
        #    goto Step 2
    # 4. If Finish[i] == true for all i => Safe state.
    printDone = False
    for i in done:
        if i is False:
            printDone = True
    if printDone is True:
        for i in range(0, len(done)):
            if done[i] is True:
                print(f'process #{i} is done!')
            else:
                print(f'process #{i} isn\'t done!')
        return False
    return sequence


def resourceRequest():
    # ? availID = 0
    # availValue = [3, 3, 2]
    # for i in Available:
    #     i = availValue[availID]
    #     availID += 1
    global Available, InitAvail
    Available = InitAvail

    print(f'A: {Available}\nI: {InitAvail}')

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

    # todo: 1. if `request` < `Available` => wait
    # todo: 2. let user consider to continue or not
    requestTooBig = False
    for i in range(0, NUM_RESOURCE):
        if request[i] > Available[i]:
            requestTooBig = True
            break
    if requestTooBig is True:
        print('Request > Available! Process must wait!')
        print(f'continue: {countineProgram()}')
        if(countineProgram() is False):
            exit

            # @debug
            # print(request, pid)
    print(f'before: {ProcessList[pid].resourceList[0].allocation}')

    for i in range(0, NUM_RESOURCE):
        # print(f'a: {Available[i]}, i: {input[i]}')
        Available[i] -= request[i]
        ProcessList[pid].resourceList[i] = ProcessList[pid].resourceList[i]._replace(
            allocation=ProcessList[pid].resourceList[i].allocation + request[i])
    # @debug
    print(f'after: {ProcessList[pid].resourceList[0].allocation}')

    print('Pretend to grant the requet')

    printStatus(Available)

    result = safty()
    if result is False:
        print('Unsafe!')
    else:
        print(f'Safe! Find the sequence: <', end="")
        # print(f'{result}')
        for i in result:
            print(f' {i},', end='')
        print(">")
        print('Safe! Grant the request!')
        countineProgram()
        
def countineProgram():
    print('Continue the Banker\'s algorithm? (Yes = y or Y) ', end='')
    key = input()
    resume = False
    if key is 'y' or key is 'Y':
        resume = True
    # else: key is 'n' or 'N':
    # else:
    #     resume = False
        # print('Please enter `y` or `n`')
        # resume = countineProgram()
    return resume

# print system status
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
            print(f"  {j.max- j.allocation}", end="")

        print()


# * main

print("=== Banker's algorithm starts!\n")
print("Initial System states: ")

NUM_PROCESS = 5
NUM_RESOURCE = 3
# Available = [10, 5, 7]
InitAvail = [3, 3, 2]
Available = []

# ? counter = 0
for i in InitAvail:
    Available.append(i)
    # ? counter +=1

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
if result is False:
    print('Unsafe!')
else:
    print(f'Safe! Find the sequence: <', end="")
    # print(f'{result}')
    for i in result:
        print(f' {i},', end='')
    print(">")

    # ? Available = InitAvail
    resourceRequest()
