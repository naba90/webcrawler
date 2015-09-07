

# Function to get page source
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ''
# To iterate over the links.
def print_all_links(page):
    while True:
        url, endpos = get_next_target(page)
        if url:
            print url
            page = page[endpos:]
        else:
            break
# To collect all url.
def get_next_target(s):
    start_link = s.find('<a href=')
    if start_link == -1:
        return None,0
    start_quote = s.find('"', start_link)
    end_quote = s.find ('"', start_quote + 1)
    url = s[start_quote + 1 : end_quote]
    return url, end_quote


print_all_links(get_page("http://xkcd.com/"))
