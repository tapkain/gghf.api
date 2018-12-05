class PriceParser:
    @staticmethod
    def from_steam(payload):
        region = payload['region']
        payload = payload.get('price_overview', None)
        if payload is None:
            return None

        return {
            'region': region,
            'store': 'steam',
            'date': datetime.now(),
            'currency': payload['currency'],
            'initial': payload['initial'],
            'final': payload['final'],
            'discount': payload['discount_percent']
        }
