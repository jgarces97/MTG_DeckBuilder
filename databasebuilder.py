import sql_helpers
import requests
import pandas as pd
from time import sleep

if __name__ == '__main__':

    #sql_helpers.create_cards()
    resp = requests.get('https://archive.scryfall.com/json/scryfall-oracle-cards.json')
    if resp.status_code != 200:
    # This means something went wrong.
        print('Uh oh')
    cards = {'name': [], 'mana_cost': [], 'type_line': [], 'color_identity': [], 'commander': []}
    for card in resp.json():
        if card['layout'] not in ['vanguard', 'token', 'scheme', 'double_faced_token', 'emblem', 'augment', 'planar',
                                  'host', 'art_series'] and card['legalities']['commander'] == 'legal':
            cards['name'].append(card['name'])
            cards['type_line'].append(card['type_line'])

            if card['layout'] in ['transform']:
                cards['mana_cost'].append(card['card_faces'][0]['mana_cost'])
            else:
                cards['mana_cost'].append(card['mana_cost'])

            identity = ""
            for color in card['color_identity']:
                identity = identity + color
            cards['color_identity'].append(identity)

            can_commnader = False
            if 'oracle_text' in card:
                if 'can be your commander' in card['oracle_text']:
                    can_commnader = True

            if can_commnader or ('Legendary Creature' in card['type_line'] and '//' not in card['type_line']):
                cards['commander'].append(True)
            else:
                cards['commander'].append(False)

            # Uncomment to get the prices for the cards
            '''
            cards['price'].append(requests.get('https://api.scryfall.com/cards/%s' % card['id']).json()['prices']['usd'])
            sleep(.06)
            '''

    df = pd.DataFrame().from_dict(cards)
    con = sql_helpers.sql_connection()
    df.to_sql('cards', con, if_exists='replace', index=False)
