import re

import requests


def get_page_text(url):
    response = requests.get(url)
    html = response.text
    page_text, page_words = "", []
    html = html[html.find("<body") + 5:html.find("</body>")]
    start_script = html.find("<script")
    while start_script > -1:
        # Remove any content within a script tag
        end_script = html.find("</script>")
        text_script = html[start_script:end_script + 9]
        html = html.replace(text_script, "")
        start_script = html.find("<script")
    try:
        ignore = []
        with open("../settings/ignore_list.txt", "r") as ign_words_file:
            for word in ign_words_file:
                # Create a list of ignore words for comparison
                # convert word to lowercase and remove any whitespace
                ignore.append(word.lower().strip())
    except IOError:
        print("Could not find the file")
    finished = False
    while not finished:
        nextCloseTag = html.find(">")
        nextOpenTag = html.find("<")
        if nextOpenTag > -1:
            content = " ".join(html[nextCloseTag + 1:nextOpenTag].strip().split())
            page_text = page_text + " " + content
            html = html[nextOpenTag + 1:]
        else:
            finished = True
    for word in page_text.split():
        if word[0].isalnum() and word.lower() not in ignore:
            word = re.sub(r'[^\w\s]', '', word)
            if word not in page_words:
                page_words.append(word)
    return page_words


def add_word_to_index(index, words, url):
    for word in words:
        if word in index.keys():
            if url not in index[word]:
                index[word].append(url)
        else:
            index[word] = [url]
    return index


def get_index_graph(url_graph):
    index = {}
    page_words = []
    for key, value in url_graph.items():
        page_words = get_page_text(key)
        add_word_to_index(index, page_words, key)
    return index