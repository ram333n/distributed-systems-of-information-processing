def generate_fibonacci_upto(n):
    fib = [1, 2]
    while fib[-1] + fib[-2] <= n:
        fib.append(fib[-1] + fib[-2])

    return fib


def fibonacci_encode(number):
    fib = generate_fibonacci_upto(number)
    codeword = []
    largest_fib_found = False

    for i in range(len(fib) - 1, -1, -1):
        if number == 0:
            break

        if fib[i] <= number:
            if not largest_fib_found:
                largest_fib_found = True
                codeword = ['0'] * (i + 1)

            codeword[i] = '1'
            number -= fib[i]

    codeword.append('1')

    return ''.join(codeword)


def main():
    for i in range(17):
        print(f'Number: {i} - code: {fibonacci_encode(i)}')

if __name__ == '__main__':
    main()