def findPokerHand(hand):
    ranks = []
    suits = []
    possibleCard = []
    for card in hand:
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]
        if rank == "A":
            rank = 14
        elif rank == "K":
            rank = 13
        elif rank == "Q":
            rank = 12
        elif rank == "J":
            rank = 11
        ranks.append(int(rank))
        suits.append(suit)

    sortedRanks = sorted(ranks)

    # print(sortedRanks)
    # Royal Flush    == AH,KH,QH,JH,10H -- Jika semua suits didalam tangan sama semua
    # Straight Flush == 10H,9H,8H,7H,6H -- Jika semua berurutan dan suits nya sama
    # Flush          == 5H,7H,1H,3H,4H  -- Jika semua Suits sama
    if suits.count(suits[0]) == 5:
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks and 10 in sortedRanks:  # Royal Flush
            possibleCard.append(10)
        # Straight Flush
        elif all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range(1, len(sortedRanks))):
            possibleCard.append(9)
        else:
            possibleCard.append(6)  # Flush
    # Straight
    if all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range(1, len(sortedRanks))):  # Straight
        possibleCard.append(5)
    # Four Of a Kind || Full House
    # the list used so that we can modify easily
    handUniqueValue = list(set(sortedRanks))
    if len(handUniqueValue) == 2:
        for val in handUniqueValue:
            if sortedRanks.count(val) == 3:  # Full House
                possibleCard.append(7)
            elif sortedRanks.count(val) == 4:  # Four Of a Kind
                possibleCard.append(8)
    # Three of a Kind || Two Pair
    if len(handUniqueValue) == 3:
        for val in handUniqueValue:
            if sortedRanks.count(val) == 3:
                possibleCard.append(4)
            elif sortedRanks.count(val) == 2:
                possibleCard.append(3)
    # Pair
    if len(handUniqueValue) == 4:
        possibleCard.append(2)
    # Jika Tidak ada didalam list maka :
    if not possibleCard:
        possibleCard.append(1)

    print(possibleCard)

    pokerHandRanks = {10: "Royal Flush", 9: "Straight Flush", 8: "Four of a Kind", 7: "Full House", 6: "Flush",
                      5: "Straight", 4: "Three of a Kind", 3: "Two Pair", 2: "Pair", 1: "High Card"}

    output = pokerHandRanks[max(possibleCard)]  # type: ignore
    print(hand, output)

    return output


if __name__ == "__main__":  # jika ini file ini yang berjalan, maka akan menjalankan code ini. Jika file lain calling function ini maka code ini tidak akan berjalan
    findPokerHand(["KH", "AH", "QH", "JH", "10H"])  # Royal Flush
    findPokerHand(["QC", "JC", "10C", "9C", "8C"])  # Straight Flush
    findPokerHand(["5C", "5S", "5H", "5D", "QH"])  # Four of a Kind
    findPokerHand(["2H", "2D", "2S", "10H", "10C"])  # Full House
    findPokerHand(["2D", "KD", "7D", "6D", "5D"])  # Flush
    findPokerHand(["JC", "10H", "9C", "8C", "7D"])  # Straight
    findPokerHand(["10H", "10C", "10D", "2D", "5S"])  # Three of a Kind
    findPokerHand(["KD", "KH", "5C", "5S", "6D"])  # Two Pair
    findPokerHand(["2D", "2S", "9C", "KD", "10C"])  # Pair
    findPokerHand(["KD", "5H", "2D", "10C", "JH"])  # High Card
