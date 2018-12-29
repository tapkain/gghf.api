from datetime import datetime
import re

def from_playstation(payload, region):
    payload = payload.get('default_sku', None)
    
    if payload is None or payload['price'] == 0:
        return None

    currency = re.sub('[0-9.,\s]', '', payload['display_price'])
    print(currency)

    if len(payload['rewards']) > 0:
        reward = payload['rewards'][0]
        final = reward['price']
        discount = reward['discount']
    else:
        final = payload['price']
        discount = 0

    return {
        'region': region,
        'store': 'playstation',
        'date': datetime.now(),
        'currency': currency,
        'initial': payload['price'],
        'final': final,
        'discount': discount
    }
