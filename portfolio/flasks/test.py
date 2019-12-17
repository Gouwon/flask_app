ii = [1,2,3,4,5]
# r = []
# r = [i for i in ii if i % 2 == 0]
# r = map(2 % i == 0 , ii)
r = filter(lambda a: a % 2 == 0, ii)

print(type(r))
for rr in r:
    print(rr)