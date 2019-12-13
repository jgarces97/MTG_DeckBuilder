import pandas as pd
import sql_helpers
from junk import cluster_by_commander


freq = {}


def count_frequency(my_list):

    # Creating an empty dictionary
    for item in my_list:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1


if __name__ == '__main__':

    decks = sql_helpers.get_all_decks_of_commander('Scion of the Ur-Dragon').fetchall()
    cards = {}
    # LIST OF DECKS
    tmp = []
    for card in decks:
        if card[0] is not None:
            if card[0] in cards.keys():
                cards[card[0]].append(card[1].replace(' ', '').replace(',', '').replace('\'', '').replace('-', '')
                                      .replace('//', ''))
            else:
                cards[card[0]] = [card[1].replace(' ', '').replace(',', '').replace('\'', '').replace('-', '')
                                      .replace('//', '')]

    df = pd.DataFrame.from_dict(cards, orient='index')
    for index, row in df.iterrows():
        lst = row.tolist()
        tmp.append(str(list(filter(lambda a: a is not None, lst))))

    cluster_by_commander(tmp)
