from dateutil.parser import parse
import time


class GameParser:
    @staticmethod
    def from_steam(payload, appid):
        payload = payload[appid]

        if not payload['success']:
            return None

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
            'platforms': GameParser.platforms_from_steam(payload),
            'categories': GameParser.categories_from_steam(payload),
            'tags': GameParser.tags_from_steam(payload),
            'attachments': GameParser.attachments_from_steam(payload),
            'release_date': GameParser.release_date_from_steam(payload)
        }

    @staticmethod
    def categories_from_steam(payload):
        categories = payload.get('categories', None)
        if categories is not None:
            return list(map(lambda x: x['description'], categories))
        return []

    @staticmethod
    def release_date_from_steam(payload):
        payload = payload['release_date']

        return {
            'coming_soon': payload['coming_soon'],
            'date': GameParser._get_release_date(payload['date'])
        }

    @staticmethod
    def _get_release_date(date):
        try:
            date = parse(date)
        except:
            try:
                date = time.strptime(date, '   %Y')
            except:
                return None
        return date

    @staticmethod
    def tags_from_steam(payload):
        genres = payload.get('genres', None)
        if genres is not None:
            return list(map(lambda x: x['description'], genres))
        return []

    @staticmethod
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

    @staticmethod
    def platforms_from_steam(payload):
        result = []

        metadata = [
            ('linux', 'linux_requirements'),
            ('mac', 'mac_requirements'),
            ('windows', 'pc_requirements'),
        ]

        for meta in metadata:
            platform = GameParser._parse_platform(payload, meta[0], meta[1])
            if platform is not None:
                result.append(platform)

        return result

    @staticmethod
    def _parse_platform(data, name, req_name):
        if not data['platforms'][name]:
            return None

        if type(data[req_name]) is list:
            req = None
        else:
            req = data[req_name]['minimum']

        return {
            'name': name,
            'requirement_minimum': req
        }
