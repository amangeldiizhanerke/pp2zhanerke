#numbers
n=int(input())
cnt=0
for i in range (1,n+1):
    if n%i==0:
        cnt+=1
if cnt!=2:
    #nuzhno delitsya krome 1 i na sebya,1 ne mozhet byt prime
    print("not prime")
else:
    print("prime number")