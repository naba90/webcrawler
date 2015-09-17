#! /usr/bin/python2.7.8

# Function to get page source from link
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ''


# Function Tt collect all url.
def get_next_target(s):
    start_link = s.find('<a href=')
    if start_link == -1:
        return None, 0  # if NO link found return 0
    start_quote = s.find('"', start_link)
    end_quote = s.find('"', start_quote + 1)
    url = s[start_quote + 1: end_quote]
    return url, end_quote


# Tu check for repeated links
def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)
    return p


# Function to iterate over all the links.
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)  # Collect end posotion of page to iterate
        if url:
            links.append(url)
            page = page[endpos:]  # New page will begin from the end of the captured link.
        else:
            break
    return links


def crawl_web(seed, max_dept):
    """

    :rtype : list.
    """
    to_crawl = [seed]
    crawled = []
    next_dept = []
    dept = 0
    while to_crawl and dept <= max_dept:  # limits the max dept in a particular link to be crawled.
        # link = to_crawl.pop()  # Dept first algorithm
        link = to_crawl[0]
        to_crawl.remove(link)
        if link not in crawled:
            # new_links = get_all_links(get_page(link))
            # print "I am at newlinks\n"
            # print new_links
            union(next_dept, get_all_links(get_page(link)))  # To add links into next_dept w/o duplication
            # to_crawl = union(to_crawl, new_links)
            # to_crawl.append(get_all_links(get_page(link)))
            crawled.append(link)
        if not to_crawl:  # This updates to_crawl with links in next_dept
            to_crawl, next_dept = next_dept, []
            dept += 1
    return crawled


# links = get_all_links(get_page("https://www.udacity.com/cs101x/index.html"))
# print crawl_web("http://www.murtazachunia.com/index.html", 2)
print crawl_web("https://www.udacity.com/cs101x/index.html", 1)
