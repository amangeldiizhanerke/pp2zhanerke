#data types
n = int(input())
lst = []
lstnumbers=[]
lstothers=[]
for i in range(n):
    x = input()
    lst.append(x)
    if x.isdigit() or (x[0]=="-" and x[1:].isdigit()):
        x=int(x)
        lstnumbers.append(x)
    else:
        lstothers.append(x)
print ("general list:", lst)
print ("integer numbers' list:", lstnumbers)
print ("not integer list:", lstothers)