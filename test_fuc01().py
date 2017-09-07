def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n.斐波那契数列"""
    a, b = 0, 1
    result = []
    while a < n:
        #print(a, end=' ')
        result.append(a)
        a, b = b, a+b
    #print()
    return result

fib(100)
f = fib
f(333)
print(fib(333))


def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise OSError('uncooperative user')
        print(complaint)

print(ask_ok('Do you really want to quit?'))
#print(ask_ok('OK to overwrite the file?', 2))
#print(ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!'))

def ff(a, L=[]):
    L.append(a)
    return L

print(ff(1))
print(ff(2))
print(ff(3))

def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L

print(f(1))
print(f(2))
print(f(3))