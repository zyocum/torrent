#!/usr/bin/env python3

import os
import sys

from tpblite import TPB
from tpblite.models.constants import CATEGORIES, ORDERS

from torrent import orders
from torrent import categories
from torrent import show

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

def browse(
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
                results = tpb.browse(
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
        '-c', '--category',
        default='hdmovies',
        choices=[c for c in categories if c != 'all'],
        help='category to browse'
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
        '-u', '--url',
        default='https://tpb.party/browse',
        help='alternative Pirate Bay URL',
    )
    parser.add_argument(
        '--command',
        default='open -a Transmission.app',
        help='''command that will be run with the selected torrent's magnet link as a single argument, e.g.: "open -a Transmission.app $1"''',
    )
    args = parser.parse_args()
    browse(
        order_by=args.order_by,
        order=args.order,
        category=args.category,
        url=args.url
    )
