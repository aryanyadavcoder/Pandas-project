import sharefunctions1 as sf


while True:

    print("<--- MENU --->")
    print("0 Exit")
    print("1 Download Share Data")
    print("2 View Share Price")
    print("3 Read CSV")

    option = int(input("Enter option: "))

    if option == 0:
        print("Exit")
        break

    elif option == 1:
        stock = input("Enter share name: ")
        start = input("Enter start date (YYYY-MM-DD): ")
        end = input("Enter end date (YYYY-MM-DD): ")

        sf.downloadShareData(stock, start, end)

    elif option == 2:
        stock = input("Enter share name: ")
        sf.getSharePrice(stock)

    elif option == 3:
        stock = input("Enter share name: ")
        df = sf.readCSV(stock)
        print(df)
