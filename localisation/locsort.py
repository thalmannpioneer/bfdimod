from pathlib import Path

def write_to_ru(line, path):
    with open(f"russian\\{path}_l_russian.yml", 'a', encoding='utf-8-sig') as file:
        file.write('\n'+line)

ENGLISH = Path("english")
RUSSIAN = Path("russian")

total = 0
missing = 0

en_entries = {}
ru_entries = {}

for path in RUSSIAN.iterdir():
    if not path.name.endswith("yml"):
        continue

    curr = set()
    lines = []
    end_id = 1

    with open(path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("l_russian"):
                continue
            stripped = line.strip()
            if stripped == "###TO TRANSLATE###":
                break
            if len(stripped) > 0 and not stripped.startswith('#'):
                entry = stripped.split(':')[0]
                curr.add(entry)
            end_id += 1

    if end_id < len(lines):
        with open(path, 'w', encoding='utf-8-sig') as file:
            file.writelines(lines[:end_id+2])
    else:
        with open(path, 'a', encoding='utf-8-sig') as file:
            file.write("\n\n ###TO TRANSLATE###\n")

    ru_entries[path.name[:-14]] = curr.copy()


for path in ENGLISH.iterdir():
    if not path.name.endswith("yml"):
        continue

    with open(path, 'r', encoding="utf-8-sig") as file:
        for line in file:
            if line.startswith("l_english"):
                continue
            stripped = line.strip()
            if len(stripped) > 0 and not stripped.startswith('#'):
                total += 1
                entry = stripped.split(':')[0]
                if not entry in ru_entries[path.name[:-14]]:
                    missing += 1
                    write_to_ru(stripped, path.name[:-14])

for path in RUSSIAN.iterdir():
    lines = []
    with open(path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()
    for i in range(1, len(lines)):
        if not lines[i].startswith(" "):
            lines[i] = " " + lines[i]
    with open(path, 'w', encoding="utf-8-sig") as file:
            file.writelines(lines)

print(f"TOTAL KEYS: {total}\nMISSING KEYS: {missing}\n{missing/total*100}% LOC MISSING")