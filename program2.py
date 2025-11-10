from typing import List, Tuple
import timeit
import random
#import matplotlib.pyplot as plt


def program2(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:  
    """
    ###
    Solution to Program 2
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)
    ###
    """

    minPos = 0
    currentPos = len(values) - 1
    totalValue = 0

    vaultsChosen = []

    # the last vault in the list will always be a max
    vaultsChosen.append(currentPos + 1)
    totalValue += values[currentPos]

    # subtract k to start the actual max finding process
    currentPos -= (k+1)

    # since the second part of the list is ordered ascendingly, we know the next value will be a max
    while currentPos > 0:
        # check for the minimum 
        if values[currentPos] < values[currentPos - 1]:
            # we have either crossed or found the minimum if ^^ is true
            minPos = currentPos
            # try to find the minimum (if this is not it)
            while values[minPos] > values[minPos + 1]:
                minPos += 1
            # and if its valid to add, then add to the total
            if minPos == currentPos:
                vaultsChosen.append(currentPos + 1)
                totalValue += values[currentPos]
            break   # then move on to the forward search
        # ok, not the minimum, add and continue
        vaultsChosen.append(currentPos + 1)
        totalValue += values[currentPos]
        currentPos -= (k+1)

    # minimum should be found atp, so begin the forward search
    # we know the first vault should be a max
    vaultsChosen.append(1)
    totalValue += values[0]
    currentPos = k+1

    # now add until hitting the minimum
    while currentPos < minPos:
        vaultsChosen.append(currentPos + 1)
        totalValue += values[currentPos]
        currentPos += (k+1)
    
    vaultsChosen.sort()

    return totalValue, vaultsChosen


"""
if __name__ == "__main__":
    input_sizes = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    repetitions = 500

    results = []

    print(f"{'n':>6} | {'avg time (s)':>15}")
    print("-" * 25)

    for n in input_sizes:
        avg_time = measure_time(n, repetitions)
        results.append(avg_time)
        print(f"{n:6d} | {avg_time:15.8e}")

    # Plot results
    # plt.figure(figsize=(8, 5))
    # plt.plot(input_sizes, results, marker='o', linestyle='-', linewidth=2)
    # plt.title("Runtime Scaling of program2")
    # plt.xlabel("Input size n")
    # plt.ylabel("Average execution time (seconds)")
    # plt.grid(True, linestyle='--', alpha=0.6)
    # plt.tight_layout()
    # plt.show()
"""


def generate_input(n: int) -> Tuple[int, int, List[int]]:
    k = random.randint(1, max(1, n-1))
    temp = []
    #generate random values
    for i in range(n):
        temp.append(i+1)

    mid = (n//2)
    ascVal = sorted(temp[:mid])
    dscVal = sorted(temp[mid:], reverse=True)

    values = dscVal + ascVal
    #print(values)
    return n, k, values

#measure the time it takes for the algorithm to run, run multiple times and get the average
def measure_time(n: int, repetitions: int = 500) -> float:
    n, k, values = generate_input(n)
    program2(n, k, values)

    t = timeit.timeit(
        stmt=f"program2({n}, {k}, {values})",
        setup="from __main__ import program2",
        number=repetitions
    )
    return t / repetitions

if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program2(n, k, values)

    print(m)
    for i in indices:
        print(i)