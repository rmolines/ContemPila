perg = input("vai la fera: ").replace(' ', '')
resp = 0
op = 1
p = 0


for n in range(len(perg)):
    i = perg[n]
    if not i.isdigit():
        if i == '+':
            resp += int(perg[p:n])*op
            op = 1
            p = n+1
        elif i == '-':
            resp += int(perg[p:n]) * op
            op = -1
            p = n+1

resp += int(perg[p:]) * op

print (resp)
