from typing import List, Tuple


def program5(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 5
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)
    """
    # Dynamic programming O(n) solution:
    # dp[i] = best total using the first i vaults (1-indexed)
    # dp[i] = max(dp[i-1], values[i-1] + dp[i-k-1])
    if n <= 0:
        return 0, []

    dp: List[int] = [0] * (n + 1)
    choose: List[bool] = [False] * (n + 1)

    # Build a choice array to reconstruct solution
    for i in range(1, n + 1):
        include = values[i - 1]
        prev_index = i - k - 1
        if prev_index >= 0:
            include += dp[prev_index]

        if include > dp[i - 1]:
            dp[i] = include
            choose[i] = True
        else:
            dp[i] = dp[i - 1]
            choose[i] = False

    # Reconstruct chosen indices in 1-indexed format
    indices: List[int] = []
    i = n
    while i >= 1:
        if choose[i]:
            indices.append(i)
            i -= (k + 1)
        else:
            i -= 1

    indices.reverse()
    return dp[n], indices

if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program5(n, k, values)

    print(m)
    for i in indices:
        print(i)