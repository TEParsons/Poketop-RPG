import pandas as pd
import requests
from pyquery import PyQuery

base_url = "https://bulbapedia.bulbagarden.net/wiki/{}_(Pok%C3%A9mon)/Generation_I_learnset#By_leveling_up"

stats = pd.read_csv("stats.csv")

data = []

for _, row in stats.iterrows():
    # stop after 151
    if row['#'] > 151:
        break
    # skip mega evos
    if "Mega " in row['Name']:
        continue
    # construct basic row
    pokerow = {n: [] for n in range(100)}
    pokerow['name'] = row['Name']
    # get pokemon name
    name = row['Name'].replace("'", "%27").replace(" ", "_")
    # construct url
    url = base_url.format(name)
    # get html from site
    try:
        resp = requests.get(url, timeout=2)
    except requests.exceptions.ReadTimeout:
        print(f"Failed {name}")
        continue
    html = resp.text
    # parse
    content_html = PyQuery(html)
    # get html table
    grand_table_html = content_html("h4 span#By_leveling_up").parent().next()
    table_html = grand_table_html("tbody tr td table:nth-child(1)")
    # get headings from html table
    columns = []
    for obj in table_html("table.sortable tr th"):
        while obj.getchildren():
            obj = obj.getchildren()[0]
        columns.append(obj.text.replace("\xa0", "").replace("\n", ""))
    # iterate through html table rows
    got_moves = False
    for row_html in table_html("table.sortable tr"):
        row_html = PyQuery(row_html)
        row = {}
        # iterate through html table row cells
        for i, cell in enumerate(row_html("td")):
            while cell.getchildren():
                cell = cell.getchildren()[0]
            # add text content to dict
            row[columns[i]] = cell.text
        # skip blank rows
        if not row:
            continue
        # add move at given level
        if "Level" in row and "Move" in row:
            pokerow[int(row['Level'])].append(row['Move'])
            got_moves = True
        elif "Y" in row and "Move" in row:
            try:
                i = int(row['Y'])
            except ValueError:
                i = 0
            # sometimes they have different levels in yellow, so has different headings
            pokerow[i].append(row['Move'])
            got_moves = True
        else:
            print(row)
    # warn if no moves (there should be at least one)
    if not got_moves:
        print(f"Failed to get moves for {name} ({url})")
        break
    # stringify
    for key in pokerow:
        if key == "name":
            continue
        pokerow[key] = ",".join(pokerow[key])
    # add to overall data
    data.append(pokerow)
    # log
    print(f"Finished {name}")

data = pd.DataFrame(data)
data.to_csv("data/levelling.csv")

