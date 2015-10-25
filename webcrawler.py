__author__ = 'Naba'


# ! /usr/bin/python2.7.8


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
        url, endpos = get_next_target(page)  # Collect end position of page to iterate
        if url:
            links.append(url)
            page = page[endpos:]  # New page will begin from the end of the captured link.
        else:
            break
    return links


def crawl_web(seed):
    """

    :rtype : list.
    """
    to_crawl = [seed]
    crawled = []
    index = []
    while to_crawl:  # limits the max dept in a particular link to be crawled.
        # link = to_crawl.pop()  # Dept first algorithm
        link = to_crawl[0]
        to_crawl.remove(link)
        if link not in crawled:
            content = get_page(link)
            add_page_to_index(index, link, content)
            union(to_crawl, get_all_links(content))  # To add links into next_dept w/o duplication
            # to_crawl = union(to_crawl, new_links)
            crawled.append(link)
    return index


# To record uses clicks
def record_user_click(index, keyword, url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] += 1


def add_to_index(index, keyword, url):
    """

    :type index: list
    """
    for entry in index:
        # format of index : [[keyword, [[url, count], [url, count],...]],...]
        if entry[0] == keyword:
            for element in entry[1]:
                if element[0] == url:
                    return
            entry[1].append([url,0])
            return
    # not found, add new keyword to index
    index.append([keyword, [url,0]])


# to update in index with all the word occurrences found in page
def add_page_to_index(index, url, content):
    words = []
    atsplit = True
    splitlist = " ';:?/<>,._+-={}[]|\n!@#$%^&*()"
    for char in content:  # iterate through each character
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                words.append(char)
                atsplit = False
            else:
                # at char to last word
                words[-1] = words[-1] + char
    #    words = content.split()
    for word in words:
        add_to_index(index, word, url)


def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []


print crawl_web("https://www.udacity.com/cs101x/index.html")
