# self.best_candidate = max(self.candidates, key=attrgetter('score'))
# # print(f'best: : {max_candidate.score}', file=sys.stderr, flush=True)

""""
def fib(n):
    result = [0, 1]
    for n in range(2, n + 1):
        a = result[n - 1]
        b = result[n - 2]
        result.append(a + b)

    return result[n]


for j in range(30):
    print(str(fib(j)))
"""

my_list = [0, 1, 2, 1, 2]


my_list.append(0)
my_list.remove(2)
my_list.append(1)
my_list.remove(0)
print(my_list)















