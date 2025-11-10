from typing import List, Tuple


def program3(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 3
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)
    """
    # Naive brute-force Θ(2^n) algorithm:
    # Calculate the sum for each subset of vaults
    subset_sums = [0] * (1 << n)
    for mask in range(1 << n):
        if mask == 0:
            subset_sums[mask] = 0
        else:
            lsb = mask & -mask
            i = (lsb.bit_length() - 1)
            subset_sums[mask] = subset_sums[mask ^ lsb] + values[i]

    best_value = 0
    best_mask = 0

    # Validate each subset within distance constraint, choose maximum value
    for mask in range(1 << n):
        valid = True
        shifted = mask
        for _ in range(k):
            shifted = shifted >> 1
            if mask & shifted:
                valid = False
                break
        if valid and subset_sums[mask] > best_value:
            best_value = subset_sums[mask]
            best_mask = mask

    # Extract chosen indices in 1-indexed format
    chosen = [i + 1 for i in range(n) if (best_mask >> i) & 1]
    return best_value, chosen


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program3(n, k, values)

    print(m)
    for i in indices:
        print(i)