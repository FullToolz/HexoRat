def main(path):
    from rich.console import Console
    from rich.table import Table

    with open(path, "rb") as f:
        data = f.read()

    WINDOW = 32

    # ---------------- helper functions ----------------

    def has_cmp(window):
        return any(0x38 <= b <= 0x3F for b in window)

    def has_jcc(window):
        return any(0x70 <= b <= 0x7F for b in window)

    def has_xor(window):
        return any(0x30 <= b <= 0x35 for b in window)

    def has_backward_jump(window):
        for j, b in enumerate(window):
            if 0x70 <= b <= 0x7F:
                if j + 1 >= len(window):
                    continue
                offset = window[j + 1]
                if offset & 0x80:  # negative jump
                    return True
        return False

    def score_window(w):
        score = 0
        if has_cmp(w):
            score += 3
        if has_jcc(w):
            score += 4
        if has_xor(w):
            score += 5
        if has_backward_jump(w):
            score += 4
        return score

    # ---------------- scanning ----------------

    hints = []  # collect hints
    last_hint_offset = -WINDOW
    MIN_SPACING = 16  # minimum spacing between hints

    # Ask once per run
    include_low = input("Include LOW level hints? [Y/N]: ").strip().upper() == "Y"
    include_med = input("Include MED level hints? [Y/N]: ").strip().upper() == "Y"

    for i in range(len(data) - WINDOW):
        w = data[i : i + WINDOW]
        score = score_window(w)
        pattern = None

        if has_xor(w) and has_backward_jump(w):
            pattern = "XOR loop (possible string decoder)"
        elif has_cmp(w) and has_jcc(w):
            pattern = "CMP + JCC cluster"
        elif has_jcc(w):
            pattern = "JCC cluster before RET"

        if pattern and i - last_hint_offset >= MIN_SPACING:
            if score >= 9:
                level = "HIGH"
            elif score >= 7:
                if include_med:
                    level = "MED "
                else:
                    continue
            else:
                if include_low:
                    level = "LOW "
                else:
                    continue  # skip LOW hints
            hints.append((level, hex(i), pattern))
            last_hint_offset = i

    # ---------------- write to file ----------------

    with open("output.txt", "w", encoding="utf-8") as f:
        for level, offset, pattern in hints:
            f.write(f"[{level}] {offset} — {pattern}\n")

    # ---------------- rich table ----------------

    console = Console()
    table = Table(title=f"[bold cyan]Suspicious Hints → {path}")

    table.add_column("Level", style="red", no_wrap=True)
    table.add_column("Offset", style="yellow")
    table.add_column("Pattern", style="magenta")

    for level, offset, pattern in hints:
        table.add_row(level, offset, pattern)

    console.print(table)
    print(f"[+] {len(hints)} hints written to output.txt")
