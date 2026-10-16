def count_lines(path: str) -> int:
    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            count += 1
    return count

if __name__ == "__main__":
    print(count_lines(".tmp/t.txt"))