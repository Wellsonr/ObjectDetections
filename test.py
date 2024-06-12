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
    # print(sortedRanks, suits)
    handRanks = {10: "Royal Flush", 9: "Straight Flush", 8: "Four of a Kind", 7: "Full House", 6: "Flush",
                 5: "Straight", 4: "Three of a Kind", 3: "Two Pair", 2: "Pair", 1: "High Card"}
    # Royal Flush
    if suits.count(suits[0]) == 5:
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks and 10 in sortedRanks:
            possibleCard.append(10)
    # Straight Flush
        if all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range(1, len(sortedRanks))):
            possibleCard.append(9)
    # Flush
        else:
            possibleCard.append(6)
    #  Straight
    if all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range(1, len(sortedRanks))):
        possibleCard.append(5)
    # Four of a kind || Full House
    uniqueValue = list(set(sortedRanks))
    if len(uniqueValue) == 2:
        for val in uniqueValue:
            if sortedRanks.count(val) == 4:
                possibleCard.append(8)
            elif sortedRanks.count(val) == 3:
                possibleCard.append(7)
    # Three Of a kind || Two Pair
    if len(uniqueValue) == 3:
        for val in uniqueValue:
            if sortedRanks.count(val) == 3:
                possibleCard.append(4)
            if sortedRanks.count(val) == 2:
                possibleCard.append(3)
    if len(uniqueValue) == 4:
        possibleCard.append(2)

    # High Card
    if not possibleCard:
        possibleCard.append(1)
    output = handRanks[max(possibleCard)]
    print(hand, output)
    return 0


if __name__ == "__main__":
    findPokerHand(["KH", "AH", "QH", "JH", "10H"])  # Royal Flush # Done
    findPokerHand(["QC", "JC", "10C", "9C", "8C"])  # Straight Flush # Done
    findPokerHand(["5C", "5S", "5H", "5D", "QH"])  # Four of a Kind # Done
    findPokerHand(["2H", "2D", "2S", "10H", "10C"])  # Full House # Done
    findPokerHand(["2D", "KD", "7D", "6D", "5D"])  # Flush # Done
    findPokerHand(["JC", "10H", "9C", "8C", "7D"])  # Straight # Done
    findPokerHand(["10H", "10C", "10D", "2D", "5S"])  # Three of a Kind # Done
    findPokerHand(["KD", "KH", "5C", "5S", "6D"])  # Two Pair # Done
    findPokerHand(["2D", "2S", "9C", "KD", "10C"])  # Pair # Done
    findPokerHand(["KD", "5H", "2D", "10C", "JH"])  # High Card # Done
