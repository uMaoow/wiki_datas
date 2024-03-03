from urllib.request import urlopen
import io
import re
import sys

contributions = {}
contributions_url = {}
trans_theme = [

        "transidentité",
        "transgenre",
        "non binaire",
        "non-binaire",
        "transition de genre"
        ]

def get_contribution_list(user, limit):
    html_list = ""
    target = "class='mw-pager-body'"
    url = "https://fr.wikipedia.org/w/index.php?title=Sp%C3%A9cial:Contributions/" + user + "&target=" + user + "&offset=&limit=" + str(limit)
    html = urlopen(url)
    res = -1
    line = "\n"
    while res == -1 and line != "":
        line = html.readline().decode()
        res = line.rfind(target)

    target = "</section>"
    res = -1
    line = "\n"
    while res == -1 and line != "":
        line = html.readline().decode()
        html_list += line
        res = line.rfind(target)
    get_contributions(html_list, int(limit))

def get_contributions(html_list, limit):
    global contributions
    buf = io.StringIO(html_list)
    target = "mw-contributions-title"
    for i in range(limit):
        res = -1
        line = "\n"
        while res == -1 and line != "":
            line = buf.readline()
            res = line.rfind(target)
        if line != "":
            title = re.findall('title=".*?"', line)[0][7:-1]
            url = re.findall('href=".*?"', line)[0][6:-1]
            if title in contributions:
                contributions[title] += 1
            else:
                contributions[title] = 1
                contributions_url[title] = url
    return(contributions)

def is_theme_related(page_url, theme):
    url = "https://fr.wikipedia.org" + page_url
    html = urlopen(url)
    page = html.read().decode().lower()
    for target in theme:
        if page.rfind(target) != -1:
            return True
    return False

if __name__ == "__main__":
    count = 0
    theme_count = 0
    edit_count = 0
    edit_theme_count = 0
    if len(sys.argv) < 3:
        print("usage: ./parse_contribs.py user limit [min]")
    get_contribution_list(sys.argv[1],sys.argv[2])
    sorted_list = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
    for item in sorted_list:
        if len(sys.argv) > 3:
            if item[1] < int(sys.argv[3]):
                break
        print("\n")
        print(item)
        count += 1
        edit_count += item[1]
        if is_theme_related(contributions_url[item[0]], trans_theme) :
            theme_count += 1
            edit_theme_count += item[1]
            print ("trans related")


    print(str(theme_count) + " out of " + str(count))
    print(str(edit_theme_count) + " out of " + str(edit_count))
