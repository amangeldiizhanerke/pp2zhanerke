#variables
temp=int(input("temperature "))
press=int(input("pressure "))
power= input("is power on or off(write on or off only) ")

if temp>=20 and temp<=80:
    if press>=30 and press<=120:
        if power=="on":
            print("conditions are convenient")
        elif power=="off":
            print("change power")
    else:
        print("change preessure")
else:
    print("change temperature")
