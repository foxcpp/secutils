#!/usr/bin/python3

import sys
import socket 


def get_by_url(url):
    if url.startswith('file://'):
        with open(url[7:]) as f:
            return f.read()
    import urllib.request
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0')
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def is_ip(addr):
    try:
        socket.inet_pton(socket.AF_INET, addr)
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, addr)
        except socket.error:
            return False
    return True


def is_domain(domain):
    import string
    if len(domain) < 4 or len(domain) > 255:
        return False
    splitten = domain.split('.')
    for block in splitten:
        if len(block) < 1 or len(block) > 63:
            return False
        if block.startswith('-') or block.endswith('-'):
            return False
        for c in block:
            if c not in string.ascii_letters and c not in string.digits and c != '-' and c != '_':
                return False
    return True


def extract_domains_abp(source):
    domains = []
    for line in source.split('\n'):
        trimmed = line.strip()
        if trimmed.startswith('!'):
            continue
        if not trimmed.startswith('||') or not trimmed.endswith('^'):
            continue
        url = trimmed[2:-1]
        if '/' not in url and is_domain(url):
            domains.append(url)
    return domains


def extract_domains(source):
    domains = []
    for line in source.split('\n'):
        trimmed = line.strip()
        if len(trimmed) == 0:
            continue
        if trimmed.startswith('#'):
            continue
        if trimmed.startswith('[Adblock Plus'):
            return extract_domains_abp(source)

        splitten = trimmed.split()
        if is_ip(splitten[0]):
            for domain in splitten[1:]:
                if domain.startswith('#'):
                    break
                if not is_domain(domain):
                    continue
                domains.append(domain)
        elif is_domain(splitten[0]):
            domains.append(splitten[0])
    domains = set(map(str.lower, domains))
    if len(domains) == 0:
        raise Exception('No domains extracted.')
    return domains


def download_and_extract(sources, log_tag='blacklisted'):
    domains = set()
    status_format = '\rCollected {} {} domains. Processed {}/{} sources.'
    print(status_format.format(len(domains), log_tag, 0, len(sources)), end='', file=sys.stderr)
    for i, url in enumerate(sources):
        try:
            domains.update(extract_domains(get_by_url(url)))
        except Exception as e:
            print('\nFailed to process list', url, file=sys.stderr)
            print(type(e).__qualname__ + ': ' + str(e), file=sys.stderr)
        print(status_format.format(len(domains), log_tag, i + 1, len(sources)), end='', file=sys.stderr)
    print(file=sys.stderr)
    return domains


def main():
    whitelists = []
    blacklists = []

    # Parse arguments into two lists above.
    target_list = blacklists
    for arg in sys.argv[1:]:
        if arg == '-w':
            target_list = whitelists
            continue
        with open(arg) as f:
            for line in f:
                trimmed = line.strip()
                if len(trimmed) == 0 or trimmed.startswith('#'):
                    continue
                target_list.append(trimmed)
        target_list = blacklists
    if target_list is whitelists:
        print('Missing value to -w argument', file=sys.stderr)
        return
    if len(blacklists) == 0:
        print('No sources!', file=sys.stderr)
        return

    blacklisted = download_and_extract(blacklists)
    whitelisted = []
    if len(whitelists) != 0:
        whitelisted = download_and_extract(whitelists, 'whitelisted')

    print('127.0.0.1', socket.gethostname(), 'localhost localhost.localdomain')
    print('255.255.255 broadcasthost')

    for domain in blacklisted.difference(whitelisted):
        print('0.0.0.0', domain)


if __name__ == '__main__':
    main()

