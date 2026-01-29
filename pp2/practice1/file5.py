#string
password=input()
c=len(password)
cnta=0
cntb=0
for i in range(c):
    if password[i].isdigit():
        cnta+=1
    if password[i]==password[i].lower():
        cntb+=1
if len(password)>=8 and len(password)<=20:
    if password[0].isupper():
        if cnta > 0 and cntb > 0:
            print("valid")
        else:
            print("invalid")
    else:
        print("invalid")
else:
    print("invalid")
