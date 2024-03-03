from urllib.request import urlopen
import io
import re
import sys

contributions = {}

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
            title = re.findall('title=".*"', line)[0][7:-1]
            if title in contributions:
                contributions[title] += 1
            else:
                contributions[title] = 1
    return(contributions)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: ./parse_contribs.py user limit [min]")
    get_contribution_list(sys.argv[1],sys.argv[2])
    sorted_list = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
    for item in sorted_list:
        if len(sys.argv) > 3:
            if item[1] < int(sys.argv[3]):
                break
        print(item)


