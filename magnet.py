#!/usr/bin/env python3

"""Createa torrent magnet URI from a torrent info_hash."""

def main(info_hash, *trackers):
    uri = f'magnet:?xt=urn:btih:{info_hash}'
    for tracker in trackers:
        uri += f'&tr:{tracker}'
    return uri

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument(
        'info_hash',
        help='a magnet URI info hash for a torrent'
    )
    parser.add_argument(
        '--trackers',
        nargs='+',
        default=[],
        help='torrent tracker URLs'
    )
    args = parser.parse_args()
    print(main(args.info_hash, *args.trackers))

