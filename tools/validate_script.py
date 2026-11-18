#!/usr/bin/env python3
"""Check a Tiny Spanish script: Spanish punctuation, Latin American rules, cast names, structure.
Usage: python tools/validate_script.py script.txt [more.txt ...]   (exit code 1 on errors)"""
import re, sys

CAST = {"emma", "mateo", "cami", "santi"}
VOSOTROS = re.compile(r"\b(vosotros|vosotras|vuestro|vuestra|vuestros|vuestras|habláis|tenéis|sois|estáis|vais|queréis)\b", re.I)
LINE = re.compile(r"^([A-Za-zÀ-ÿ' ]+):\s*(.+)$")
HEADERS = {"title", "episode", "level", "topic", "scene", "cast", "variety", "duration", "objective", "kind", "weather", "cover"}
SECTIONS = {"hook", "story", "vocab", "grammar", "quiz", "ending", "intro", "listening", "conclusion", "practice"}


def balanced(text, opener, closer):
    return text.count(opener) == text.count(closer)


def check_spanish(s, where, errors, latam):
    if not balanced(s, "¿", "?"):
        errors.append(f"{where}: unbalanced ¿ ? in: {s}")
    if not balanced(s, "¡", "!"):
        errors.append(f"{where}: unbalanced ¡ ! in: {s}")
    if latam and VOSOTROS.search(s):
        errors.append(f"{where}: vosotros form in Latin American script: {s}")


def validate(path):
    errors, header, latam, section = [], {}, True, None
    for i, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^\[(\w+)\]$", line)
        if m:
            section = m.group(1).lower()
            if section not in SECTIONS:
                errors.append(f"line {i}: unknown section [{section}]")
            continue
        key, _, val = line.partition(":")
        k = key.strip().lower()
        if section is None and k in HEADERS:
            header[k] = val.strip()
            if k == "variety":
                latam = val.strip().lower() != "spain"
            continue
        where = f"line {i}"
        if k in ("vocab", "example", "grammar"):
            parts = [p.strip() for p in val.split("|")]
            if k != "grammar":
                if len(parts) < 2 or not parts[1]:
                    errors.append(f"{where}: needs 'Spanish | English'")
                check_spanish(parts[0], where, errors, latam)
            continue
        if k == "quiz":
            parts = [p.strip() for p in val.split("|")]
            if len(parts) < 5 or parts[4].upper() not in ("A", "B", "C"):
                errors.append(f"{where}: quiz needs question | A | B | C | answer letter")
            for p in parts[1:4]:
                if re.search(r"[¿¡]", p):
                    check_spanish(p, where, errors, latam)
            continue
        m = LINE.match(line)
        if m:
            speaker = m.group(1).strip().lower()
            if speaker not in CAST:
                errors.append(f"{where}: unknown speaker '{m.group(1)}'")
            parts = [p.strip() for p in m.group(2).split("|")]
            if len(parts) < 2 or not parts[1]:
                errors.append(f"{where}: dialogue needs 'Spanish | English'")
            check_spanish(parts[0], where, errors, latam)
        else:
            errors.append(f"{where}: cannot read line: {line[:60]}")
    for req in ("title", "episode", "level"):
        if req not in header:
            errors.append(f"missing header: {req}")
    cast = [c.strip().lower() for c in header.get("cast", "").split(",") if c.strip()]
    for c in cast:
        if c not in CAST:
            errors.append(f"cast: unknown character '{c}'")
    return errors


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        errs = validate(p)
        print(("OK   " if not errs else "FAIL ") + p)
        for e in errs:
            print("   -", e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)
