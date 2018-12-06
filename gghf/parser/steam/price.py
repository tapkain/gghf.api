from datetime import datetime


def from_steam(payload, appid):
    region = payload['region']
    payload = payload.get(str(appid), None)
    if payload is None or not payload['success']:
        return None

    payload = payload['data']
    if payload is None or len(payload) == 0:
        return None

    payload = payload.get('price_overview', None)
    return {
        'region': region,
        'store': 'steam',
        'date': datetime.now(),
        'currency': payload['currency'],
        'initial': payload['initial'],
        'final': payload['final'],
        'discount': payload['discount_percent']
    }
