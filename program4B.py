from typing import List, Tuple


def program4B(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4B
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)
    """

    # ref: https://www.geeksforgeeks.org/dsa/maximum-sum-subsequence-least-k-distant-elements
    
    # DP = array of sums
    DP = [0] * n
    # solution = list of indices in a sublist
    solution = [[] for i in range(n)]
    print(solution)
    
    # base case for the upcoming loop
    DP[n-1] = values[n-1]


    # for every value in Values (excluding the last one), R->L
    for pos in range(n-2, -1, -1):
        print()
            #print("position:", pos)
        # if this is a starting element (elements from n to n-k)
        if (pos+(k+1) >= n):
            # used to determine where to start the sum
            DP[pos] = max(values[pos], DP[pos+1])
                # print("+Comparing:", values[pos], "to", DP[pos+1])
            # choose indices
            if DP[pos] == values[pos]:
                solution[pos] = [pos]
            else:
                solution[pos] = [pos+1]
        else:
            # compare a possible sum to the current sum
            # would start a new sum or continue
            DP[pos] = max(values[pos] + DP[pos+(k+1)], DP[pos+1])
                # print("-Comparing:", values[pos], "+", DP[pos+(k+1)], "to", DP[pos+1])
            # choose indices
            if DP[pos] == DP[pos+1]:
                solution[pos] = [pos+1]
            else:
                solution[pos] = [pos] + solution[pos+(k+1)]
    return DP[0], solution[0] # replace with your code


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program4B(n, k, values)

    print(m)
    for i in indices:
        print(i)