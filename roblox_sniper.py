import os
import sys
import time
import string
import random
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

out_fn = "available_roblox.txt"
OUTFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_fn)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

letters = list(string.ascii_lowercase)
digits = list(string.digits)


def col(txt, c_name):
    if not HAS_COLOR:
        return str(txt)
    cols = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "gray": Fore.WHITE + Style.DIM,
    }
    return cols.get(c_name, "") + str(txt) + Style.RESET_ALL


def print_logo():
    os.system("cls" if os.name == "nt" else "clear")
    print(col("┌──────────────────────────────────────────────┐", "cyan"))
    print(col("│   _  _    ___    ___    ___                  │", "cyan"))
    print(col("│  | || |  / _ \\  / _ \\  / _ \\                 │", "cyan"))
    print(col("│  | || |_| | | || | | || | | |                │", "cyan"))
    print(col("│  |__   _| |_| || |_| || |_| |                │", "cyan"))
    print(col("│     |_|  \\___/  \\___/  \\___/                 │", "cyan"))
    print(col("└──────────────────────────────────────────────┘", "cyan"))


def ask_user(prompt, valid_options):
    while True:
        try:
            user_in = input(col(" > ", "cyan") + col(prompt, "white") + " ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return valid_options[0]
        if user_in in valid_options:
            return user_in


def ask_num(prompt, min_val, max_val, fallback):
    while True:
        try:
            inp = input(col(" > ", "cyan") + col(f"{prompt} [{fallback}]:", "white") + " ").strip()
        except (EOFError, KeyboardInterrupt):
            return fallback
        if not inp:
            return fallback
        if inp.isdigit():
            num = int(inp)
            if min_val <= num <= max_val:
                return num


def build_session(max_threads):
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA, "Accept": "application/json"})
    adapter = HTTPAdapter(
        pool_connections=max_threads,
        pool_maxsize=max_threads + 2,
        max_retries=Retry(total=2, backoff_factor=0.5, status_forcelist=[502, 503, 504])
    )
    sess.mount("https://", adapter)
    return sess


def check_roblox_user(sess, username):
    endpoint = "https://auth.roblox.com/v1/usernames/validate"
    payload = {"request.username": username, "request.birthday": "2000-01-01", "request.context": "signup"}
    
    # retry loop in case of ratelimits
    for i in range(3):
        try:
            res = sess.get(endpoint, params=payload, timeout=5)
            if res.status_code == 200:
                c = int(res.json().get("code", -1))
                if c == 0:
                    return True
                elif c == 1:
                    return False
                return None
            elif res.status_code == 429:
                time.sleep(4 + i) # backoff a bit
        except Exception:
            time.sleep(0.4)
    return None


def update_cli(name, status, done, total, hits, start_t):
    pct = int((done / total) * 100) if total else 0
    pbar = "█" * (pct // 5) + "░" * (20 - pct // 5)
    
    t_pass = time.time() - start_t
    eta_str = "--"
    if done and t_pass > 0:
        sec_left = (total - done) / (done / t_pass)
        if sec_left >= 60:
            eta_str = f"{int(sec_left // 60)}m{int(sec_left % 60)}s"
        else:
            eta_str = f"{int(sec_left)}s"

    if status is True:
        tag = col("[HIT]", "green")
    elif status is False:
        tag = col("[-─-]", "gray")
    else:
        tag = col("[ERR]", "yellow")

    out = f"\r {tag} {col(name.ljust(16), 'white')}{col(f' [{pbar}] {pct:3}%', 'gray')}{col(f' {done}/{total}', 'gray')}{col(f' Hits: {hits}', 'green')}{col(f' ETA: {eta_str} ', 'gray')}"
    sys.stdout.write(out)
    sys.stdout.flush()


def worker_job(name, hit_list, session, delay, stats):
    time.sleep(delay + random.uniform(0.005, 0.04))
    
    res = check_roblox_user(session, name)
    stats["checked"] += 1
    
    if res is True:
        stats["found"] += 1
        hit_list.append(name)
        try:
            with open(OUTFILE, "a", encoding="utf-8") as f:
                f.write(name + "\n")
        except Exception:
            pass
        update_cli("", True, stats["checked"], stats["total"], stats["found"], stats["start"])
    else:
        update_cli(name, res, stats["checked"], stats["total"], stats["found"], stats["start"])



def gen_alpha(length, count):
    out = set()
    while len(out) < count:
        out.add("".join(random.choices(letters, k=length)))
    return list(out)[:count]


def gen_alphanum(length, count):
    out = set()
    while len(out) < count:
        s = random.choice(letters)
        for _ in range(length - 1):
            s += random.choice(letters) if random.random() < 0.6 else random.choice(digits)
        out.add(s)
    return list(out)[:count]


def gen_scores(length, count):
    out = set()
    while len(out) < count:
        arr = [random.choice(letters)]
        has_us = False
        for i in range(length - 1):
            if not has_us and random.random() < 0.22 and i != length - 2:
                arr.append("_")
                has_us = True
            else:
                arr.append(random.choice(letters))
        s = "".join(arr)
        if not s.endswith("_"):
            out.add(s)
    return list(out)[:count]


def run():
    while True:
        print_logo()

        len_choice = int(ask_user("Length (4/5):", ["4", "5"]))
        print(col("\n [1] Letters  [2] Letters+Digits  [3] Underscores", "gray"))
        charset_type = ask_user("Charset (1/2/3):", ["1", "2", "3"])

        t_count = ask_num("Threads (1-50):", 1, 50, 25)
        req_delay = max(0.02, min(1.0, 0.5 / t_count))
        
        target_amount = 95000 if len_choice == 5 else 45000

        if charset_type == "1":
            user_list = gen_alpha(len_choice, target_amount)
        elif charset_type == "2":
            user_list = gen_alphanum(len_choice, target_amount)
        else:
            user_list = gen_scores(len_choice, target_amount)

        random.shuffle(user_list)
        total_names = len(user_list)

        print(f"\n Target: {len_choice}-char | Count: {total_names:,} | Threads: {t_count}")
        try:
            input(col(" Press [ENTER] to start...", "yellow"))
        except (KeyboardInterrupt, EOFError):
            break

        stats = {
            "checked": 0, 
            "found": 0, 
            "total": total_names, 
            "start": time.time()
        }
        hits = []

        try:
            with open(OUTFILE, "w", encoding="utf-8") as f:
                f.write(f"# Usernames | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        except Exception:
            pass

        http_sess = build_session(t_count)
        
        with ThreadPoolExecutor(max_workers=t_count) as exec_pool:
            tasks = [exec_pool.submit(worker_job, name, hits, http_sess, req_delay, stats) for name in user_list]
            for _ in as_completed(tasks):
                pass

        elapsed_time = time.time() - stats["start"]
        speed = stats["checked"] / elapsed_time if elapsed_time > 0 else 0
        
        print(f"\n\n Finished! Processed: {stats['checked']:,} | Hits: " + col(str(len(hits)), "green") + f" | Speed: {speed:.1f}/s")
        
        if hits:
            print(col("\n Hits:", "green"))
            for h in hits:
                print(col(f"   -> {h}", "green"))

        if ask_user("\nRun again? (y/n):", ["y", "n"]) != "y":
            break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(col("\n Exiting...", "cyan"))
        sys.exit(0)
