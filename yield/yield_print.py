def h():
    print 'Wen Chuan',
    m = yield 5
    print m
    d = yield 12
    print 'We are together!'
c = h()
m = c.next()
d = c.send('Fighting!')
print 'We will never forget the date', m, '.', d