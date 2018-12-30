from datetime import datetime, timedelta, timezone
import dateutil.parser

def from_playstation(payload):
    # TODO Figure out how to get developers and website
    return {
        'appid': payload.get('id', ''),
        'name': payload.get('name', ''),
        'type': payload.get('game_contentType', ''),
        'long_desc': payload.get('long_desc', None),
        'header_image': payload['images'][0]['url'],
        'website': None,
        'developers': None,
        'publishers': [payload.get('provider_name', None)],
        'platforms': platforms_from_playstation(payload),
        'tags': tags_from_playstation(payload),
        'attachments': attachments_from_playstaion(payload),
        'release_date': release_date_from_playstation(payload)
    }

def release_date_from_playstation(payload):
    release = dateutil.parser.parse(payload['release_date'])

    return {
        'coming_soon': datetime.now(timezone.utc) < release,
        'date': payload['release_date']
    }

def platforms_from_playstation(payload):
    result = []

    for meta in payload['playable_platform']:
        result.append({'name': meta})

    return result

def attachments_from_playstaion(payload):
    attachments = []
    if payload.get('mediaList', None) is not None:
        movies = payload['mediaList'].get('previews', None)
        if movies is not None:
            movies = list(movies)
            for movie in movies:
                attachments.append({
                    'type': 'video',
                    'content': movie['url'],
                })

        screenshots = payload['mediaList'].get('screenshots', None)
        if screenshots is not None:
            screenshots = list(screenshots)
            for screenshot in screenshots:
                attachments.append({
                    'type': 'screenshot',
                    'content': screenshot['url']
                })

    return attachments

def tags_from_playstation(payload):
    genres = payload['metadata'].get('genre', None)
    if genres is not None:
        return list(genres.get('values', None))
    return []
