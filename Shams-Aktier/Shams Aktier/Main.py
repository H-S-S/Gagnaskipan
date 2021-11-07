#apple_USD.csv
import os

def all_posetive(seq):
    isIt = True
    if len(seq)==0:

        print(seq)
        return 1

    elif seq[0] >= 0:
        print(seq)
        all_posetive(seq[1:])
else:
        print(seq)
        isIt = False
        return isIt





nums = [1, 5, 65, 1]

shams= all_posetive(nums)

print(shams)

def File_Def(val):
    file = open(val, "r")
    date = []
    price = []
    for line in file:
        for i in range(len(line)):
            if line[i] == ";":
                iafter = i + 1
                nonewline = len(line) - 2
                date.append(line[0:i])
                price.append(float(line[iafter:nonewline]))
    PriceDateDic = {"Date": date,
                    "Price": price}
    return PriceDateDic

def High(PriceDateDic):
    high_price_index = 0
    for i in range(len(PriceDateDic["Price"])):
        if max(PriceDateDic["Price"]) == PriceDateDic["Price"][i]:
            high_price_index = i
    return high_price_index


def Low(PriceDateDic):
    low_price_index = 0
    for i in range(len(PriceDateDic["Price"])):
        if min(PriceDateDic["Price"]) == PriceDateDic["Price"][i]:
            low_price_index = i
    return low_price_index


def Worst_Buy(PriceDateDic):
    biggest_drop = 1
    then_price_index = 0
    now_price_index = 0
    for i in range(len(PriceDateDic["Price"])):
        for k in range(len(PriceDateDic["Price"])):
            if k > i:
                then_price = PriceDateDic["Price"][i]
                now_price = PriceDateDic["Price"][k]
                if biggest_drop >= (now_price - then_price):
                    biggest_drop = (now_price - then_price)
                    then_price_index = i
                    now_price_index = k
    return then_price_index, now_price_index


valName = str(input("Vilken fil vill du öppna? "))
val = "Aktiekurser_2/" + valName

nameIndex = 0
for i in range(len(valName)):
    if valName[i] == "_":
        nameIndex = i
nameOfFile = valName[0:nameIndex] + "_stoks.txt"

if not os.path.isfile(nameOfFile):
    PriceDateDic = File_Def(val)

    then_price_index, now_price_index = Worst_Buy(PriceDateDic)
    high_price_index = High(PriceDateDic)
    low_price_index = Low(PriceDateDic)

    price_difference = PriceDateDic["Price"][then_price_index] - PriceDateDic["Price"][now_price_index]


    # skriver in allt i text document
    file = open(nameOfFile, "w")
    file.write("Report on {} shares\n".format(valName[0:nameIndex]))
    file.write("-----------------------------------------------\n\n")
    file.write("Highest price\n-----------------------------------------------\n")
    file.write("Date: {}\nPrice: {}\n \n".format(PriceDateDic["Date"][high_price_index], max(PriceDateDic["Price"])))
    file.write("Lowest price\n-----------------------------------------------\n")
    file.write("Date: {}\nPrice: {}\n \n".format(PriceDateDic["Date"][low_price_index], min(PriceDateDic["Price"])))
    profit = PriceDateDic["Price"][high_price_index] - PriceDateDic["Price"][low_price_index]
    file.write("Best buy-date: {}\nBest sell-date:{}\nProfit: {}\n".format(PriceDateDic["Date"][low_price_index],
                                                                           PriceDateDic["Date"][high_price_index],
                                                                           profit))
    file.write(
        "\nWorst buy-date: {}\nWorst sell-date:{}\nLoss per share(not in percent like a real investor you idiot): {}\n".format(
            PriceDateDic["Date"][then_price_index], PriceDateDic["Date"][now_price_index], price_difference))
    file.close()
else:
    print("File Alredy exists")