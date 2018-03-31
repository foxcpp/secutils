#!/usr/bin/python3

import sys


def get_by_url(url):
    # TODO: Allow to source files.
    import urllib.request
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0')
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def is_ip(addr):
    import socket
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


def extract_domains(source):
    domains = []
    for line in source.split('\n'):
        trimmed = line.strip()
        if len(trimmed) == 0:
            continue
        if trimmed.startswith('#'):
            continue

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


def main():
    if len(sys.argv) < 2:
        print('At least one file with sources is required.')

    urls = []
    for file in sys.argv[1:]:
        with open(file) as f:
            for line in f:
                trimmed = line.strip()
                if len(trimmed) == 0 or trimmed.startswith('#'):
                    continue
                urls.append(trimmed)

    domains = set()
    status_format = '\rCollected {} domains. Processed {}/{} sources.'
    for i, url in enumerate(urls):
        print(status_format.format(len(domains), i, len(urls)), end='', file=sys.stderr)
        try:
            domains.update(extract_domains(get_by_url(url)))
        except Exception as e:
            print('\nFailed to process list', url, file=sys.stderr)
            print(type(e).__qualname__ + ': ' + str(e))

    for domain in domains:
        print('0.0.0.0', domain)


if __name__ == '__main__':
    main()

