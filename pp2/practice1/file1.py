items = []
summ = []

command = input("choose one add/sell/count/exit ")

while True:
    if command == "add" or command.lower() == "add":
        item = input("write item name")
        for i in range(len(items)):
            if items[i] == item:
                summ[i] += 1
                print(f"we added {item}")
                break
        else:
            items.append(item)
            summ.append(1)
            print(f"we added {item}")

    if command == "sell" or command.lower() == "sell":
        item = input("what to sell")
        for i in range(len(items)):
            if items[i] == item:
                if summ[i] <= 0:
                    print("we dont have it, choose another item")
                else:
                    summ[i] -= 1
                    print(f"{item} was sold, count is {summ[i]}")
                break

    if command == "count" or command.lower() == "count":
        for i in range(len(items)):
            print(items[i], summ[i])

    elif command == "exit":
        break
