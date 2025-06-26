# fibonacci series
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return []
    elif n == 2:
        return [0, 1]

    fib_series = [0, 1]
    for i in range(1, n):
        next_value = fib_series[i - 1] + fib_series[i - 2]
        fib_series.append(next_value)

    return fib_series


# Example usage
if __name__ == "__main__":
    n = int(input("Enter the number of terms in the Fibonacci series: "))
    result = fibonacci(n)
    print(f"Fibonacci series up to {n} terms: {result}")
