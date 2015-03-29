'''
Created on Mar 28, 2015

@author: jnaylor
'''

import sys
import re
import urllib


def main(domain):
    all_emails = [];
    urls_visited = [];
    probe(domain, all_emails, urls_visited)
    print "Found these email addresses on domain {}:".format(domain)
    unique_emails = set(all_emails)
    for email in unique_emails:
        print email;
    
def probe(site, all_emails, urls_visited):
    child_urls = []
    url = site;
    if not site.startswith('http://') and not site.startswith('https://') and not site.startswith('//'):
        url = "http://" + site
    if url not in urls_visited:            
        print "opening {}".format(url);
        page = ''
        try:
            url_handle = urllib.urlopen(url)
            page = url_handle.read()
            url_handle.close()
            urls_visited.append(url)
        except:
            print "problem opening url {}".format(url)
        # print page
        all_emails += find_emails(page);
        child_urls += find_urls(page, site);
        for child_url in child_urls:
            probe(child_url, all_emails, urls_visited);
    
def find_emails(page):
    email_pattern=r'(\w+@\w+(\.\w+)+)'
    email_list = re.findall(email_pattern, page)
    emails = [e[0] for e in email_list]
    return emails

def find_urls(page, site):
    url=r'\<a .*?href=[\"\'](.*?)[\"\']'
    url_list = re.findall(url, page)
    urls = [u for u in url_list if not u.startswith('#') and site in u]
    # print "urls", urls
    return urls

def usage():
    print '''
Usage:
    sys.argv[0], <domain name>
'''
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1);
    main(sys.argv[1]);
