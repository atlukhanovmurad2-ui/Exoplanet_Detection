n = 10

for row in range(n):
    for col in range(2 * n + 1):
        if ((row < n // 2 and
             ((col >= n - row - 1 and col <= n - 1) or
              (col >= n + 1 and col <= n + row + 1))) or \
           (row >= n // 2 and
             abs(col - n) <= n - row - 1)):
            print("* ", end="")
        else:
            print("  ", end="")
    print()