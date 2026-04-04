

import requests
import time
import random
import threading
import string
import os
import sys
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False


THREADS  = 50       
DELAY    = 0.02     
RETRIES  = 3
VERSION  = "1.0"
AUTHOR   = "40oo"


outdir   = os.path.dirname(os.path.abspath(__file__))
OUTFILE  = os.path.join(outdir, "available_roblox.txt")
UA       = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

_lock    = threading.Lock()
_checked = 0
_found   = 0
_errors  = 0
_total   = 0
_start   = 0.0
_tlocal  = threading.local()

letters  = list(string.ascii_lowercase)
digits   = list(string.digits)
vowels   = list("aeiou")
cons     = list("bcdfghjklmnprstvwxyz")

cool_starts = [
    "kr","dr","br","gr","tr","pr","fr",
    "bl","cl","fl","gl","pl","sl",
    "sk","sp","st","sw","sm","sn",
    "zr","vr","sh","ch","nx","vx","zx",
]

pat4 = ["CVCC","CVCV","CCVC","VCVC","CVVC","VCCV","CCVV","VVCV","CVVV","VVCV"]
pat5 = ["CVCCV","CVCVC","CCVCV","VCVCV","CVCVV","CVVCV","CCVCC","VCCVC","CVVCC","VVCVC"]



def col(txt, clr):
    if not HAS_COLOR:
        return str(txt)
    m = {
        "red":    Fore.RED,
        "green":  Fore.GREEN,
        "yellow": Fore.YELLOW,
        "cyan":   Fore.CYAN,
        "white":  Fore.WHITE,
        "gray":   Fore.WHITE + Style.DIM,
        "magenta":Fore.MAGENTA,
    }
    return m.get(clr, "") + str(txt) + Style.RESET_ALL


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    clear()
    print()
    print(col("  ┌─────────────────────────────────────────┐", "cyan"))
    print(col("  │                                         │", "cyan"))
    print(col("  │   ", "cyan") + col("R B L X", "white") + col("  -  ", "gray") + col("username sniper", "cyan") + col("        │", "cyan"))
    print(col("  │                                         │", "cyan"))
    print(col("  │   ", "cyan") + col("4 & 5 letter · roblox · fast", "gray") + col("         │", "cyan"))
    print(col("  │                                         │", "cyan"))
    print(col("  └─────────────────────────────────────────┘", "cyan"))
    print()
    print(col(f"  v{VERSION}  by {AUTHOR}", "gray"))
    print(col("  " + "─" * 43, "gray"))
    print()


def hdr(title):
    print(col(f"\n  [ {title} ]", "cyan"))
    print(col("  " + "─" * 40, "gray"))


def ask(txt):
    try:
        return input(col("  > ", "cyan") + col(txt + " ", "white")).strip()
    except EOFError:
        return ""


def opt(k, lbl, note=""):
    line = col(f"  [{k}]", "yellow") + col(f"  {lbl}", "white")
    if note:
        line += col(f"  ({note})", "gray")
    print(line)



def draw(name, result):
    pct = int((_checked / _total) * 100) if _total > 0 else 0
    bar = "█" * (pct // 5) + "░" * (20 - pct // 5)

    elapsed = time.time() - _start
    if _checked > 0 and elapsed > 0:
        rem = (_total - _checked) / (_checked / elapsed)
        if rem >= 3600:
            eta = f"{int(rem//3600)}h{int((rem%3600)//60)}m"
        elif rem >= 60:
            eta = f"{int(rem//60)}m{int(rem%60)}s"
        else:
            eta = f"{int(rem)}s"
    else:
        eta = "--"

    if result is True:
        tag = col("  [HIT] ", "green")
    elif result is False:
        tag = col("  [----]", "gray")
    else:
        tag = col("  [ERR] ", "yellow")

    line = (
        f"\r{tag} "
        + col(name.ljust(12), "white")
        + col(f" [{bar}] {pct:3}%", "gray")
        + col(f"  {_checked}/{_total}", "gray")
        + col(f"  hits:{_found}", "green")
        + col(f"  eta:{eta}  ", "gray")
    )
    try:
        sys.stdout.write(line)
        sys.stdout.flush()
    except Exception:
        pass



def get_sess():
    if not hasattr(_tlocal, "s"):
        s = requests.Session()
        s.headers.update({"User-Agent": UA, "Accept": "application/json"})
        adp = HTTPAdapter(
            pool_connections=THREADS,
            pool_maxsize=THREADS,
            max_retries=Retry(total=2, backoff_factor=0.3)
        )
        s.mount("https://", adp)
        _tlocal.s = s
    return _tlocal.s



def check(name):
    # Official Roblox validation API
    # code 0 = available, code 1 = taken, other = invalid/uncertain
    url = "https://auth.roblox.com/v1/usernames/validate"
    p   = {
        "request.username": name,
        "request.birthday": "2000-01-01",
        "request.context": "signup"
    }
    for attempt in range(RETRIES):
        try:
            r = get_sess().get(url, params=p, timeout=6)
            if r.status_code == 200:
                code = r.json().get("code", -1)
                if code == 0:   return True
                elif code == 1: return False
                else:           return None
            elif r.status_code == 429:
                time.sleep(6 * (attempt + 1))
            else:
                return None
        except Exception:
            time.sleep(1)
    return None



def worker(name, hits):
    global _checked, _found, _errors

    if not name or " " in name:
        return

    time.sleep(DELAY + random.uniform(0, 0.05))
    result = check(name)

    with _lock:
        _checked += 1

        if result is True:
            _found += 1
            hits.append(name)
            try:
                with open(OUTFILE, "a", encoding="utf-8") as f:
                    f.write(name + "\n")
            except Exception:
                pass
            sys.stdout.write("\r" + " " * 90 + "\r")
            sys.stdout.flush()
            print(col(f"  [AVAILABLE]  {name}", "green") +
                  col(f"  [{datetime.now().strftime('%H:%M:%S')}]", "gray"))
        elif result is False:
            draw(name, False)
        else:
            _errors += 1
            draw(name, None)




def gen_exhaustive(length, charset):
    """Generate ALL possible combinations for the given length and charset.
    For 4-letter a-z this is 456,976 names — fully exhaustive."""
    combos = list(itertools.product(charset, repeat=length))
    random.shuffle(combos)
    
    result = []
    for c in combos:
        name = "".join(c)
        if name[0].isalpha():
            # max 1 underscore, no consecutive underscores, no trailing
            if name.count("_") <= 1 and "__" not in name and not name.endswith("_"):
                result.append(name)
    return result


def gen_pronounceable(length, count):
    """Generate pronounceable letter-only names using CV patterns and cool prefixes."""
    names = set()
    pats  = pat4 if length == 4 else pat5

   
    for pat in pats:
        for _ in range(8000):
            n = "".join(random.choice(vowels if c == "V" else cons) for c in pat)
            if len(n) == length:
                names.add(n)

    
    for start in cool_starts:
        if len(start) >= length:
            continue
        for _ in range(1000):
            fill, was_v = "", start[-1] in vowels
            for i in range(length - len(start)):
                ch = random.choice(cons) if was_v else (
                    random.choice(vowels) if random.random() > 0.3 else random.choice(cons))
                fill += ch
                was_v = ch in vowels
            n = start + fill
            if len(n) == length:
                names.add(n)

    
    while len(names) < count:
        n, sc = "", random.random() > 0.3
        for i in range(length):
            n += random.choice(cons if (i % 2 == 0) == sc else vowels)
        if n[0].isalpha():
            names.add(n)

    out = list(names)
    random.shuffle(out)
    return out[:count]


def gen_letters_numbers(length, count):
    """Letters + numbers, always starts with a letter."""
    names = set()
    while len(names) < count:
        n = [random.choice(letters)]
        for _ in range(length - 1):
            n.append(random.choice(letters) if random.random() < 0.6 else random.choice(digits))
        names.add("".join(n))
    out = list(names)
    random.shuffle(out)
    return out[:count]


def gen_underscore(length, count):
    """Letters + exactly 1 underscore, always starts with a letter."""
    names = set()
    while len(names) < count:
        n, used = [random.choice(letters)], False
        for i in range(length - 1):
            if random.random() < 0.72 or used:
                n.append(random.choice(letters))
            elif n[-1] != "_" and i != length - 2:
                n.append("_")
                used = True
            else:
                n.append(random.choice(letters))
        s = "".join(n)
        if not s.endswith("_"):
            names.add(s)
    out = list(names)
    random.shuffle(out)
    return out[:count]


def gen_all_mixed(length, count):
    """All chars: letters + numbers + 1 underscore max."""
    names = set()
    while len(names) < count:
        n, used = [random.choice(letters)], False
        for i in range(length - 1):
            r = random.random()
            if r < 0.52:
                n.append(random.choice(letters))
            elif r < 0.82:
                n.append(random.choice(digits))
            elif not used and n[-1] != "_" and i != length - 2:
                n.append("_")
                used = True
            else:
                n.append(random.choice(letters))
        s = "".join(n)
        if not s.endswith("_"):
            names.add(s)
    out = list(names)
    random.shuffle(out)
    return out[:count]



def run():
    global _checked, _found, _errors, _total, _start

    while True:
        banner()

        
        hdr("Length")
        opt("1", "4 letters")
        opt("2", "5 letters")
        opt("3", "Both 4 and 5 letters")
        lc = ask("Choose length:")
        while lc not in ["1", "2", "3"]:
            print(col("  enter 1, 2 or 3", "red"))
            lc = ask("Choose length:")
        lengths = [4] if lc == "1" else [5] if lc == "2" else [4, 5]

        
        hdr("Character Set")
        opt("1", "Letters only          (a-z)         — pronounceable names")
        opt("2", "FULL letters only     (a-z)         — every combination, exhaustive")
        opt("3", "Letters + numbers     (a-z, 0-9)")
        opt("4", "Letters + underscore  (a-z, _)")
        opt("5", "All                   (a-z, 0-9, _)")
        opt("6", "Load from .txt file")
        cc = ask("Choose charset:")
        while cc not in ["1", "2", "3", "4", "5", "6"]:
            print(col("  enter 1-6", "red"))
            cc = ask("Choose charset:")

        
        COUNT_PER_LENGTH = {
            4: 456976,   
            5: 1000000,  
        }

        names    = []
        custom   = False
        fname    = ""

        if cc == "6":
            hdr("Load File")
            print(col("  one username per line, no spaces", "gray"))
            fname = ask("Filename (e.g. usernames.txt):")
            fpath = fname if os.path.isabs(fname) else os.path.join(outdir, fname)
            if not os.path.exists(fpath):
                print(col("  file not found", "red"))
                input(col("\n  press ENTER to try again\n", "yellow"))
                continue
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                names = [l.strip() for l in f if l.strip() and not l.startswith("#") and " " not in l.strip()]
            random.shuffle(names)
            custom = True
            print(col(f"  loaded {len(names):,} usernames", "green"))
        else:
            hdr("Generating")
            print(col("  generating, please wait...", "gray"))
            for length in lengths:
                count = COUNT_PER_LENGTH.get(length, 500000)
                if cc == "1":
                    batch = gen_pronounceable(length, count)
                elif cc == "2":
                    # exhaustive — every single combo
                    batch = gen_exhaustive(length, string.ascii_lowercase)
                elif cc == "3":
                    batch = gen_letters_numbers(length, count)
                elif cc == "4":
                    batch = gen_underscore(length, count)
                else:
                    batch = gen_all_mixed(length, count)
                names.extend(batch)
                print(col(f"  {length}-letter: {len(batch):,} names", "white"))

            
            names = list(set(names))
            random.shuffle(names)
            print(col(f"  total: {len(names):,} unique names ready", "green"))

        
        hdr("Speed")
        opt("1", "Normal   (25 threads)")
        opt("2", "Fast     (50 threads)")
        opt("3", "Turbo    (100 threads)  — may get rate limited faster")
        sc = ask("Choose speed:")
        threads = {"1": 25, "2": 50, "3": 100}.get(sc, 50)

        _total = len(names)

        hdr("Summary")
        print(col("  Platform   ", "gray") + col("Roblox", "white"))
        if custom:
            print(col("  Source     ", "gray") + col(fname, "white"))
        else:
            length_str = " + ".join(f"{l}-letter" for l in lengths)
            charset_labels = {"1":"pronounceable","2":"exhaustive a-z","3":"letters+numbers","4":"letters+underscore","5":"all mixed"}
            print(col("  Length     ", "gray") + col(length_str, "white"))
            print(col("  Charset    ", "gray") + col(charset_labels.get(cc, "custom"), "white"))
        print(col("  Threads    ", "gray") + col(str(threads), "white"))
        print(col("  Usernames  ", "gray") + col(f"{_total:,}", "white"))
        print(col("  Output     ", "gray") + col("available_roblox.txt", "white"))
        print(col("  Sample     ", "gray") + col(", ".join(names[:8]), "white"))
        print()

        try:
            input(col("  Press ENTER to start  |  Ctrl+C to stop\n", "yellow"))
        except KeyboardInterrupt:
            print()
            break

        _checked = _found = _errors = 0
        hits     = []
        _start   = time.time()

        try:
            with open(OUTFILE, "w", encoding="utf-8") as f:
                f.write("# Available Roblox Usernames\n")
                f.write(f"# by {AUTHOR}  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        except Exception as e:
            print(col(f"  warning: could not create output file ({e})", "yellow"))

        hdr("Checking")
        print(col("  [HIT] = available   [----] = taken   [ERR] = uncertain\n", "gray"))

        t0 = time.time()
        try:
            with ThreadPoolExecutor(max_workers=threads) as ex:
                futs = {ex.submit(worker, u, hits): u for u in names}
                for ft in as_completed(futs):
                    try:
                        ft.result()
                    except Exception:
                        pass
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            print(col("\n  stopped.", "red"))

        elapsed = time.time() - t0
        rate    = _checked / elapsed if elapsed > 0 else 0

        sys.stdout.write("\n")
        hdr("Results")
        print(col("  Checked    ", "gray") + col(f"{_checked:,}", "white"))
        print(col("  Time       ", "gray") + col(f"{elapsed:.1f}s  ({rate:.1f}/sec)", "white"))
        print(col("  Found      ", "gray") + col(str(len(hits)), "green" if hits else "white"))
        print(col("  Uncertain  ", "gray") + col(str(_errors), "yellow" if _errors else "white"))

        if hits:
            print()
            print(col("  Available usernames:", "green"))
            for h in hits:
                print(col(f"    ->  {h}", "green"))

        print()
        print(col("  " + "─" * 43, "gray"))
        print(col(f"  rblx-sniper by {AUTHOR}", "cyan"))
        print()

        try:
            again = ask("run again? [y/n]").lower()
        except KeyboardInterrupt:
            break

        if again != "y":
            break

    print(col("\n  bye!\n", "cyan"))


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(col("\n\n  bye!\n", "cyan"))
        sys.exit(0)
