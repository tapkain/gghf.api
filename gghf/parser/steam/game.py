from dateutil.parser import parse
import time


def from_steam(payload, appid):
    payload = payload[str(appid)]

    if not payload['success']:
        return False

    payload = payload['data']
    return {
        'appid': int(appid),
        'name': payload.get('name', ''),
        'type': payload.get('type', ''),
        'description': payload.get('detailed_description', None),
        'header_image': payload.get('header_image', None),
        'website': payload.get('website', None),
        'developers': payload.get('developers', None),
        'publishers': payload.get('publishers', None),
        'platforms': platforms_from_steam(payload),
        'categories': categories_from_steam(payload),
        'tags': tags_from_steam(payload),
        'attachments': attachments_from_steam(payload),
        'release_date': release_date_from_steam(payload)
    }


def categories_from_steam(payload):
    categories = payload.get('categories', None)
    if categories is not None:
        return list(map(lambda x: x['description'], categories))
    return []


def release_date_from_steam(payload):
    payload = payload['release_date']

    return {
        'coming_soon': payload['coming_soon'],
        'date': _get_release_date(payload['date'])
    }


def _get_release_date(date):
    try:
        date = parse(date)
    except:
        try:
            date = time.strptime(date, '   %Y')
        except:
            return None
    return date


def tags_from_steam(payload):
    genres = payload.get('genres', None)
    if genres is not None:
        return list(map(lambda x: x['description'], genres))
    return []


def attachments_from_steam(payload):
    attachments = []

    movies = payload.get('movies', None)
    if movies is not None:
        for movie in movies:
            attachments.append({
                'type': 'video',
                'thumbnail': movie['thumbnail'],
                'content': movie['webm']['max'],
                'name': movie['name']
            })

    screenshots = payload.get('screenshots', None)
    if screenshots is not None:
        for screenshot in screenshots:
            attachments.append({
                'type': 'screenshot',
                'thumbnail': screenshot['path_thumbnail'],
                'content': screenshot['path_full']
            })

    return attachments


def platforms_from_steam(payload):
    result = []

    metadata = [
        ('linux', 'linux_requirements'),
        ('mac', 'mac_requirements'),
        ('windows', 'pc_requirements'),
    ]

    for meta in metadata:
        platform = _parse_platform(payload, meta[0], meta[1])
        if platform is not None:
            result.append(platform)

    return result


def _parse_platform(data, name, req_name):
    if not data['platforms'][name]:
        return None

    minimum = None
    recommended = None
    if type(data[req_name]) is not list:
        minimum = data[req_name].get('minimum', None)
        recommended = data[req_name].get('recommended', None)

    return {
        'name': name,
        'requirement_minimum': minimum,
        'requirement_recommended': recommended
    }
