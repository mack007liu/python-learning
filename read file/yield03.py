def read_file(fpath):
    BLOCK_SIZE = 1024
    with open(fpath, 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return

c=read_file('D:\openSource\git\demo\data.txt')
m = c.next()
d = c.send('Fighting!')
print m