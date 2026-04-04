<div align="center">
  <img src="preview.png" alt="rblx-sniper preview" width="700"/>
  <h1>rblx-sniper</h1>
  <p>Fast Roblox 4 & 5 letter username checker — find available names before anyone else</p>

  [![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square)](https://python.org)
  [![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey?style=flat-square)]()
  [![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)]()

  [Download](#installation) • [Usage](#usage) • [Discord](#discord)
</div>

---

## Preview

<div align="center">
  <img src="preview.png" alt="checker running" width="650"/>
</div>

---

## Features

- Check 4 and 5 letter Roblox usernames for availability
- Multiple generation modes:
  - **Pronounceable** — names that sound like real words
  - **Exhaustive** — every single combination (456,976 for 4-letter a–z)
  - **Letters + numbers** — e.g. `kr4vo`, `z9xn`
  - **Letters + underscore** — e.g. `kr_vo`, `z_xn`
  - **All combined** — widest possible net
  - **Custom file** — load your own `.txt` list
- Optimised thread count — fast without triggering rate limits
- Uses the official Roblox API for accurate results
- Live progress bar with ETA
- Hits print instantly and save to `available_roblox.txt`
- Adaptive rate limit handling — backs off automatically on 429s
- Works on Windows, Mac and Linux

---

## Installation

**Windows**
```bash
git clone https://github.com/40oo/rblx-sniper.git
cd rblx-sniper
pip install requests colorama
python roblox_sniper.py
```

**Linux**
```bash
git clone https://github.com/40oo/rblx-sniper.git
cd rblx-sniper
pip3 install requests colorama --break-system-packages
python3 roblox_sniper.py
```

**macOS**
```bash
git clone https://github.com/40oo/rblx-sniper.git
cd rblx-sniper
pip3 install requests colorama
python3 roblox_sniper.py
```

---

## Usage

Run the script and follow the on-screen menu:

```
[ Length ]    4 letters / 5 letters / both
[ Charset ]   pronounceable / exhaustive / letters+numbers / underscore / all / custom file
```

Press `ENTER` to start. Available names print live and are saved to `available_roblox.txt` as they're found. Press `Ctrl+C` at any time to stop — everything found so far is kept.

---

## Generation Modes

| Mode | What it generates | Best for |
|---|---|---|
| Pronounceable | CV patterns + cool prefixes | Clean, natural sounding names |
| Exhaustive | Every single combination | Maximum coverage on 4-letter |
| Letters + numbers | e.g. `kr4vo`, `z9xn` | More hits, less competition |
| Letters + underscore | e.g. `kr_vo`, `z_xn` | Unique looking names |
| All | Letters + numbers + underscore | Widest net |

---

## Tips

- Use **exhaustive** mode for 4-letter to cover every possible name
- Use **letters + numbers** for 5-letter — far more available than pure letters
- Results are randomised every run so different people check different names
- If you see lots of `[ERR]`, your connection may be unstable — try again later

---

## Discord

<div align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Join%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"/>
  </a>
  <p>Join for help, updates and to share your finds</p>
</div>

---

<div align="center">
  made by <strong>40oo</strong>
</div>
