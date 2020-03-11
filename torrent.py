#!/usr/bin/env python3

import os
import sys

from tpblite import TPB
from tpblite.models.constants import CATEGORIES, ORDERS

orders = {
    ('leechers', 'asc'): ORDERS.LEECHERS.ASC,
    ('leechers', 'desc'): ORDERS.LEECHERS.DES,
    ('name', 'asc'): ORDERS.NAME.ASC,
    ('name', 'desc'): ORDERS.NAME.DES,
    ('seeders', 'asc'): ORDERS.SEEDERS.ASC,
    ('seeders', 'desc'): ORDERS.SEEDERS.DES,
    ('size', 'asc'): ORDERS.SIZE.ASC,
    ('size', 'desc'): ORDERS.SIZE.DES,
    ('type', 'asc'): ORDERS.TYPE.ASC,
    ('type', 'desc'): ORDERS.TYPE.DES,
    ('uploaded', 'asc'): ORDERS.UPLOADED.ASC,
    ('uploaded', 'desc'): ORDERS.UPLOADED.DES,
    ('uploader', 'asc'): ORDERS.UPLOADER.ASC,
    ('uploader', 'desc'): ORDERS.UPLOADER.DES,
}

categories = {
    'all': CATEGORIES.ALL,
    'applications': CATEGORIES.APPLICATIONS.ALL,
    'audio': CATEGORIES.AUDIO.ALL,
    'games': CATEGORIES.GAMES.ALL,
    'porn': CATEGORIES.PORN.ALL,
    'video': CATEGORIES.VIDEO,
    'hdtv': CATEGORIES.VIDEO.HD_TV_SHOWS,
    'tv': CATEGORIES.VIDEO.TV_SHOWS,
    'hdmovies': CATEGORIES.VIDEO.HD_MOVIES,
    'movies': CATEGORIES.VIDEO.MOVIES,
    'ebooks': CATEGORIES.OTHER.EBOOKS,
    'comics': CATEGORIES.OTHER.COMICS,
}

def show(page, pages):
    torrents = pages.get(page, [])
    print(f'Page: {page} ({len(torrents)} torrents)')
    print(
        *(f'{i: >2}: {t}, {t.upload_date}' for i, t in enumerate(torrents)),
        sep='\n'
    )
    if not any(torrents):
        print('\a\r', flush=True, end='')
    action = input(':').lower()
    if len(torrents) == 1 and action.strip() == '':
        action = '0'
    elif action.strip() == '':
        action = 'n'
    print('\033[H\033[J')
    return action

def search(
    query,
    order_by='seeders',
    order='desc',
    category='all',
    url=None,
    command='open -a Transmission.app'
):
    print('\033[H\033[J')
    tpb = TPB() if (url is None) else TPB(url)
    page = 1
    action = 'n'
    pages = {}
    while action not in ('q', 'quit', 'x', 'exit'):
        try:
            if page not in pages:
                results = tpb.search(
                    query,
                    page=page,
                    order=orders[(order_by, order)],
                    category=categories[category]
                )
                pages[page] = results
            action = show(page, pages)
            if action in ('n', 'j'):
                page += 1
                continue
            elif action in ('p', 'k'):
                page -= 1
                if page < 1:
                    print('\a\r', flush=True, end='')
                    page = 1
                continue
            elif action in [str(k) for k in range(len(pages[page]))]:
                torrent = pages[page][int(action)]
                os.system(f"{command} '{torrent.magnetlink}'")
            else:
                print('\a\r', flush=True, end='')
        except ConnectionError as e:
            print(e.__class__.__name__, ':', e, file=sys.stderr)
            return
        except (EOFError, KeyboardInterrupt):
            print('\a\r\033[H\033[J', flush=True)
            return

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument(
        'query',
        help='search query'
    )
    parser.add_argument(
        '-b', '--order-by',
        default='seeders',
        choices={o for (o, _) in orders},
        help='the facet on which to order the results'
    )
    parser.add_argument(
        '-s', '--order',
        default='desc',
        choices={s for (_, s) in orders},
        help='how to order the results',
    )
    parser.add_argument(
        '-c', '--categories',
        default='all',
        choices=list(categories),
        help='the categories to search',
    )
    parser.add_argument(
        '-u', '--url',
        default=None,
        help='alternative Pirate Bay URL',
    )
    parser.add_argument(
        '--command',
        default='open -a Transmission.app',
        help='''command that will be run with the selected torrent's magnet link as a single argument, e.g.: "open -a Transmission.app $1"''',
    )
    args = parser.parse_args()
    search(
        args.query,
        order_by=args.order_by,
        order=args.order,
        category=args.categories,
        url=args.url
    )
