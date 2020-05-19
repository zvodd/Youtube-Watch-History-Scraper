import json
from io import IOBase

def get_clipboard():
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    clipboard = root.clipboard_get()
    return clipboard

def parse_cookies(cstring, include_domains=None):
    jcookies = json.loads(cstring)
    simple_cookie_dict = {}
    for cookie in jcookies:
        if include_domains and (not 
        any(domain in cookie['domain'] for domain in include_domains)):
            continue
        else:
            simple_cookie_dict.update({cookie['name']: cookie['value']})
    return simple_cookie_dict

def main():
    import argparse, sys
    from pprint import pprint
    # print sys.argv

    parser = argparse.ArgumentParser(description='Process some integers.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', action='store',
                        type=argparse.FileType('r', 0), metavar="FILENAME")
    group.add_argument('-c', '--clip', action='store_true')
    parser.add_argument('domains', type=str, nargs='*', default=None)
    args = parser.parse_args()
    
    if 'file' in args and isinstance(args.file, IOBase):
        cstring = args.file.read()
        args.file.close()
    elif args.clip:
        cstring = get_clipboard()
    simple_cookies = parse_cookies(cstring, include_domains=args.domains)
    pprint(simple_cookies)

if __name__ == "__main__":
    main()
