import re

SEARCH = "SEARCH"
STR = "STR"
CON = "CON"
DEX = "DEX"
INT = "INT"
WIS = "WIS"
CHA = "CHA"
ACTIONS = "ACTIONS"


class StatBlock:
    def __init__(self):
        self.ac = -1
        self.hp = -1
        self.cr = -1
        self.str = -1
        self.con = -1
        self.dex = -1
        self.int = -1
        self.wis = -1
        self.cha = -1
        self.actions = {}
        self.resists = set()
        self.immunes = set()


def main():
    filename = 'test_mm.txt' # "/Users/spen/Documents/Projects/Coding/dnd/raw_monster_manual.txt"

    with open(filename, "r") as file:
        lines = file.readlines()

    creature_lines = get_creature_section(lines)
    creatures = get_creatures(creature_lines)


def get_creature_section(lines):
    begin_index = 0
    end_index = len(lines)
    found_begin = False
    for index, line in enumerate(lines):
        if not found_begin and "AARAKOCRA" in line:
            begin_index = index
            found_begin = True

        if "INDEX OF STAT BLOCKS" in line:
            end_index = index
            break

    return lines[begin_index:end_index]


def get_creatures(creature_lines):
    creatures = {}

    state = SEARCH
    name = "Nullizoid"
    nameless_count = 0
    stats = StatBlock()
    for line in creature_lines:
        line = line.rstrip()

        if state == SEARCH:
            if line.isupper():
                if line == STR:
                    state = STR
                    continue
                elif line == CON:
                    state = CON
                    continue
                elif line == DEX:
                    state = DEX
                    continue
                elif line == INT:
                    state = INT
                    continue
                elif line == WIS:
                    state = WIS
                    continue
                elif line == CHA:
                    state = CHA
                    continue

                elif ACTIONS in line:
                    state = ACTIONS

                # Capitalized word not matching those above
                elif len(line) > 2:
                    if False not in [w.isalpha() for w in line.split()]:
                        name_format_line = " ".join([n.capitalize() for n in line.split()])
                        if name_format_line != name:
                            name = name_format_line
                            stats = StatBlock()
                            creatures[name] = stats
                            continue

            else:
                has_ac = re.match("^Armor Class (\d+).*", line)
                if has_ac:
                    ac = has_ac.group(1)

                    if stats.ac != -1:
                        stats, nameless_count = add_nameless_creature(nameless_count, creatures)

                    stats.ac = ac
                    continue

                has_hp = re.match("^Hit Points (\d+).*", line)
                if has_hp:
                    hp = has_hp.group(1)
                    stats.hp = hp
                    continue

                has_cr = re.match("^Challenge (\d+).*", line)
                if has_cr:
                    cr = has_cr.group(1)
                    stats.cr = cr
                    continue

                has_resists = re.match("^Damage Resistances (.+)", line)
                if has_resists:
                    resists = has_resists.group(1)
                    stats.resists = set(resists.split())
                    continue

                has_immunes = re.match("^Damage Immunities (.+)", line)
                if has_immunes:
                    immunes = has_immunes.group(1)
                    stats.immunes = set(immunes.split())
                    continue

        elif state == STR:
            has_str = re.match("^(\d+).+", line)
            if has_str:
                str = has_str.group(1)
                stats.str = str

        elif state == CON:
            has_con = re.match("^(\d+).+", line)
            if has_con:
                con = has_con.group(1)
                stats.con = con

        elif state == DEX:
            has_stat = re.match("^(\d+).+", line)
            if has_stat:
                stat = has_stat.group(1)
                stats.dex = stat

        elif state == WIS:
            has_stat = re.match("^(\d+).+", line)
            if has_stat:
                stat = has_stat.group(1)
                stats.wis = stat

        elif state == INT:
            has_stat = re.match("^(\d+).+", line)
            if has_stat:
                stat = has_stat.group(1)
                stats.int = stat

        elif state == CHA:
            has_stat = re.match("^(\d+).+", line)
            if has_stat:
                stat = has_stat.group(1)
                stats.cha = stat

        elif state == ACTIONS:
            pass

        state = SEARCH

    return creatures


def add_nameless_creature(nameless_count, creatures):
    name = "Nullizoid " + str(nameless_count)
    nameless_count += 1
    stats = StatBlock()
    creatures[name] = stats
    return stats, nameless_count


if __name__ == '__main__':
    main()
