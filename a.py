napis = input()
if len(napis)==0:
    print("PUSTY")
else:
    zero = napis.find('0')
    napis=napis[zero+1:]
    napis=napis[::-1]
    jeden = napis.find('1')
    napis = napis[jeden+1:]
    napis = napis[::-1]
    print(napis)