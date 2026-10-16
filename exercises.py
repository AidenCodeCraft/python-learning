try:
    count = 0
    with open(".tmp/1.txt", "r", encoding="utf-8") as f:
        for line in f:
            count += 1
    print(count)
except FileNotFoundError:
    txt = ""