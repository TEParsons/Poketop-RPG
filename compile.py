from pathlib import Path
import pandas as pd
import re

# read in stats
stats = pd.read_csv("data/stats.csv")
# read in moves
moves = pd.read_csv("data/moves.csv")
# read in levelling info
levelling = pd.read_csv("data/levelling.csv", index_col="name")
# read in evolution info
evolution = pd.read_csv("data/evos.csv", index_col="name")
# array to store moves strings
all_moves = {}
moves_by_type = {}
# read in template
template = Path("data/pokemon_template.md").read_text()

# iterate through moves
for _, row in moves.iterrows():
    # array to store values in
    attrs = {}
    # generate key
    key = row['Name'].lower().replace(" ", "").replace("-", "")
    # store basics
    attrs['name'] = row['Name']
    attrs['type'] = row['Type'].title()
    attrs['pp'] = row['PP']
    attrs['categ'] = row['Category']
    # get description
    if not pd.isna(row['Description']):
        attrs['desc'] = row['Description']
    else:
        attrs['desc'] = ""
    # replace spelling of defense
    attrs['desc'] = attrs['desc'].replace("Defense", "Defence")
    # make stat modifier attacks more explicit
    def add_amount(match):
        sharply, action, target, stat, extra = match.groups()
        # work out amount
        amount = 1
        if sharply:
            amount = 2
        # reassemble string
        return f"{action} {target}'s {stat}{extra or ''} by {amount}."
    mod_re = (
        # optional intensifier
        r"([Ss]harply )?"
        # action (raises, lowers, etc.)
        r"([Ll]owers?|[Ll]owers? an|[Ll]owers? the|[Rr]aises?|[Rr]aises? an|[Rr]aises? the) "
        # target (user vs opponent)
        r"(user|opponent)'s "
        # stat
        r"(Special Defence|Special Attack|Defence|Attack|Evasiveness|Speed)\.?"
        # extra stats
        r"( and (?:Special Defence|Special Attack|Defence|Attack|Evasiveness|Speed))?\.?"
        # gunk at the end
        r"(?: by \w* stages?)?\.?"
        r""
    )
    stat_names_re = r"Special Defence|Special Attack|Defence|Attack|Evasiveness"
    action_names_re = r"[Ll]owers?|[Ll]owers? an|[Ll]owers? the|[Rr]aises?|[Rr]aises? an|[Rr]aises? the"
    attrs['desc'] = re.sub(
        pattern=mod_re,
        repl=add_amount,
        string=attrs['desc']
    )
    # rephrase critical hit ratio
    attrs['desc'] = attrs['desc'].replace(
        "High critical hit ratio.", 
        "Critical hits on a 19."
    )
    attrs['desc'] = attrs['desc'].replace(
        "Increases critical hit ratio.", 
        "Subsequent attacks critical hit on a 19."
    )
    # recoil damage
    attrs['desc'] = attrs['desc'].replace(
        "User receives recoil damage",
        "User takes recoil damage equal to their Attack modifier"
    )
    # guaranteed hits
    attrs['desc'] = attrs['desc'].replace(
        "Ignores Accuracy and Evasiveness",
        "Always hits"
    )
    # give clarity on "may" effects
    attrs['desc'] = attrs['desc'].replace(
        "May ",
        "On a hit above 18 will "
    )
    # clearer times
    attrs['desc'] = attrs['desc'].replace(
        "a period of time",
        "1d6 turns"
    )
    
    # work out accuracy modifier
    try:
        acc = int(row['Accuracy'])
    except:
        attrs['acc'] = None
        attrs['acc_str'] = ""
    else:
        attrs['acc'] = int(acc / 10 - 5)
        attrs['acc_str'] = str(attrs['acc'])
        if attrs['acc'] > 0:
            attrs['acc_str'] = "+" + attrs['acc_str']
        attrs['acc_str'] += " to hit, "
    # work out damage
    try:
        pwr = int(row['Power'])
    except:
        attrs['dmg'] = None
        attrs['dmg_str'] = ""
    else:
        dmg = pwr / 10
        attrs['dmg'] = min((4, 6, 8, 10, 12, 20), key=lambda x:abs(x-dmg))
        attrs['dmg_str'] = "d%(dmg)s" % attrs
        if attrs['categ'] == "Physical":
            attrs['dmg_str'] += "+Atk"
        elif attrs['categ'] == "Special":
            attrs['dmg_str'] += "+SpAtk"
        attrs['dmg_str'] += " damage. "
    # lowercase desc if needed
    if attrs['acc_str'] and not attrs['dmg_str']:
        attrs['desc'] = attrs['desc'][0].lower() + attrs['desc'][1:]
    # create description
    move_template = "***%(name)s** %(type)s-type %(categ)s Move*: %(acc_str)s%(dmg_str)s%(desc)s"
    # store content
    all_moves[key] = move_template % attrs
    # store against its type
    if attrs['type'] not in moves_by_type:
        moves_by_type[attrs['type']] = []
    moves_by_type[attrs['type']].append(move_template % attrs)

# write moves page
content = (
    f"# Moves\n"
    f"\n"
)
for this_type, this_moves in moves_by_type.items():
    content += (
        f"## {this_type}\n"
        f"\n"
    )
    for this_move in this_moves:
        content += (
            f"{this_move}\n"
            f"\n"
        )
# save moves page
outfile = Path("source/moves.md")
outfile.write_text(content, encoding="utf-8")
# log
print("Written moves")


# iterate through pokemon
for _, row in stats.iterrows():
    # stop after 151
    if row['#'] > 151:
        break
    # skip mega evos
    if "Mega " in row['Name']:
        continue
    # file to save to
    outfile = Path("source/pokemon") / ("z%(#)s_%(Name)s.md" % row)
    # array to store values in
    attrs = {}
    # get basics
    attrs['name'] = row['Name']
    attrs['num'] = row['#']
    attrs['name_lower'] = row['Name'].lower().replace("'", "").replace("♀", "-f").replace("♂", "-m").replace(". ", "-")
    attrs['hp'] = int(row['HP'] / 2)
    # combine types
    attrs['type'] = row['Type 1']
    if not pd.isna(row['Type 2']):
        attrs['type'] += " / " + row['Type 2']
    # construct evolution string
    attrs['evo'] = ""
    this_evo = dict(evolution.loc[attrs['name'].upper(), :])
    this_evo['into'] = str(this_evo['into']).title()
    evo_lvl = re.match(pattern=r"Level (\d+)", string=this_evo['evolves at'])
    evo_stone = re.findall(pattern=r"(\w*) STONE", string=str(this_evo['by means of']))
    evo_trade = re.match(pattern=r"LINK CABLE", string=str(this_evo['by means of']))
    if evo_lvl:
        this_evo['lvl'] = evo_lvl.group(1)
        attrs['evo'] = "*Evolves at lvl%(lvl)s into %(into)s*" % this_evo
    elif evo_stone:
        this_evo['stone'] = "/".join(stone.lower() for stone in evo_stone)
        attrs['evo'] = "*Evolves by %(stone)s stone into %(into)s*" % this_evo
    elif evo_trade:
        attrs['evo'] = "*Evolves by trade into %(into)s*" % this_evo
    # calculate modifiers
    for stat, key in (
        ("Attack", "atk"),
        ("Sp. Atk", "spatk"),
        ("Defense", "def"),
        ("Sp. Def", "spdef"),
        ("Speed", "speed")
    ):
        # store base value
        val = attrs[key] = row[stat]
        # calculate modifier
        mod = int((val / 100 - 0.8) * 6)
        # stringify modifier
        mod_str = str(mod)
        if mod >= 0:
            mod_str = "+" + mod_str
        # store modifier
        attrs[key + "_mod"] = mod_str
    # calculate hp multiplier
    attrs['hp_mod'] = int(attrs['hp'] / 10)
    
    # construct moves string
    moves_str = ""
    for lvl, this_moves in levelling.loc[row['Name'], :].items():
        if not isinstance(this_moves, str):
            continue
        moves_str += f"#### Level {lvl}\n"
        for this_move in this_moves.split(","):
            # generate key
            key = this_move.lower().replace(" ", "").replace("-", "")
            if key not in all_moves:
                print(f"Couldn't find move {key} ({row['Name']})")
                continue
            # append move text
            moves_str += f"\n{all_moves[key]}\n"
    attrs['moves'] = moves_str

    # write
    outfile.write_text(template % attrs, encoding="utf-8")
    # log
    print("Written %(name)s" % attrs)
