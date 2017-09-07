matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

[[row[i] for row in matrix] for i in range(4)]


transposed1 = []
for i in range(4):
    transposed1.append([row[i] for row in matrix])



transposed = []
for i in range(4):
    # the following 3 lines implement the nested listcomp
    transposed_row = []
    for row in matrix:
        transposed_row.append(row[i])
        #print(row)
    print(transposed_row)
    transposed.append(transposed_row)

print(transposed)

#print(matrix)
#print(list(zip(*matrix)))
print(dict([('sape', 4139), ('guido', 4127), ('jack', 4098)]))

print({x: x**2 for x in (2, 4, 6)})  # dict(sape=4139, guido=4127, jack=4098)


for i, v in enumerate(['tic', 'tac', 'toe']):
     print(i, v)