from typing import List, Tuple

def program4A(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4A
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)
    """

    DP = [-1]*n
    solution = [[] for i in range(n)]

    val, indices = chooseVault(n-1, k+1, values, DP, solution)
    indices.reverse()

    return val, indices # replace with your code

def chooseVault(i: int, k: int, vaults:List[int], DP:List[int], solution):
    # no elements left to evaluate
    if i < 0:
        return 0, []
    
    # only one element
    if i == 0:
        return vaults[0], [0]
    
    # something already cached there
    if DP[i] != -1:
        return DP[i], solution[i]
    
    # option 1: choose the current vault, move k vaults
    current, currentIndex = chooseVault(i-k, k, vaults, DP, solution)
    current += vaults[i]
    currentIndex = [i] + currentIndex

    # option 2: ignore this vault, move to the next one
    prev, prevIndex = chooseVault(i-1, k, vaults, DP, solution)

    # choose the max value between the two, return
    maximum = max(current, prev)
    if maximum == current:
        if DP[i] == -1:
            DP[i] = maximum
            solution[i] = currentIndex
        return DP[i], solution[i]
    else:
        if DP[i-1] == -1:
            DP[i-1] = maximum
            solution[i-1] = prevIndex
        return DP[i-1], solution[i-1]

if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program4A(n, k, values)

    print(m)
    for i in indices:
        print(i)