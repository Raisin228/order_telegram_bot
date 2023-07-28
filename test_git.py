print('hello world')

a = int(input())


def func(num):
    num += 1000
    print(num)


func(a)

def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)


print(fact(3))
