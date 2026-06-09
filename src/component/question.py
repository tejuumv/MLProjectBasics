import requests

def decode_secret_message(url):
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.strip().splitlines()

    grid = {}
    max_x = 0
    max_y = 0

    # Skip header line, parse: character, x, y
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        char = parts[0]
        x = int(parts[1])
        y = int(parts[2])
        grid[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    # Print grid top-to-bottom, left-to-right
    for y in range(max_y + 1):
        row = ""
        for x in range(max_x + 1):
            row += grid.get((x, y), " ")
        print(row)

decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")