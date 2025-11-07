def GenerateSyracuseSequence(n: int):
    liste = []
    liste.append(n)
    max = n
    count = 1
    while (n > 1):
        if (n % 2 == 0):
            n = n / 2
        else:
            n = 3 * n + 1
            count = count + 1
        if (n > max):
            max = n
        liste.append(int(n))
    return liste


if __name__ == "__main__":
    n = int(input("Saisir un nombre :"))
    max = n
    count = 1

    while (n > 1):
        if (n % 2 == 0):
            n = n / 2
        else:
            n = 3 * n + 1
            count = count + 1
        if (n > max):
            max = n

        print(n)
    print("nombre de termes dans la suite :" + str(count))
    print("valeur max de la suite :" + str(max))

    values=GenerateSyracuseSequence(5)
    print(values)