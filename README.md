<div align="center">

<img src="preview.png" alt="preview" width="700"/>

<br/>

# rblx-sniper

**Fast Roblox 4 & 5 letter username checker — find available names**

[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)](https://python.org)
[![Version](https://img.shields.io/badge/Version-1.0-cyan?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#)
[![Discord](https://img.shields.io/badge/Discord-Join-7289da?style=flat-square&logo=discord)](https://discord.gg/c95uE5ejff)

<br/>

[**Download**](#installation) • [**Usage**](#usage) • [**Discord**](https://discord.gg/c95uE5ejff)

</div>

---

## preview

<div align="center">
<img src="preview.png" alt="checker running" width="650"/>
</div>

---

## video tutorial

<div align="center">

[![Watch Tutorial](https://img.shields.io/badge/Watch%20Tutorial-YouTube-red?style=for-the-badge&logo=youtube)](YOUR_YOUTUBE_LINK)

</div>

---

## features

- 4 and 5 letter Roblox username checking
- multiple generation modes:
  - pronounceable names (sounds like real words)
  - exhaustive — every single combination (456,976 for 4-letter a-z)
  - letters + numbers
  - letters + underscore
  - all combined
  - load from custom `.txt` file
- up to 100 threads for fast checking
- uses official Roblox API — accurate results
- live progress bar with ETA
- saves results to `available_roblox.txt` automatically
- run again option after finishing
- works on Windows, Mac and Linux

---

## installation

### Windows

```
git clone https://github.com/40oo/rblx-sniper.git
cd rblx-sniper
pip install requests colorama
python roblox_sniper.py
```

### Linux

```
git clone https://github.com/40oo/rblx-sniper.git
cd rblx-sniper
pip3 install requests colorama --break-system-packages
python3 roblox_sniper.py
```

### macOS

```
git clone https://github.com/40oo/rblx-sniper.git
cd rblx-sniper
pip3 install requests colorama
python3 roblox_sniper.py
```

---

## usage

run the script and follow the menu:

```
[ Length ]     4 letters / 5 letters / both
[ Charset ]    pronounceable / exhaustive / letters+numbers / underscore / all / custom file
[ Speed ]      normal (25) / fast (50) / turbo (100 threads)
```

press `ENTER` to start — hits print live and save to `available_roblox.txt`.
press `Ctrl+C` to stop at any time, results already found are kept.

---

## generation modes explained

| Mode | What it generates | Best for |
|------|-------------------|----------|
| Pronounceable | CV patterns + cool prefixes | clean sounding names |
| Exhaustive | literally every combo | maximum coverage |
| Letters + numbers | e.g. `kr4vo`, `z9xn` | more hits, less competition |
| Letters + underscore | e.g. `kr_vo`, `z_xn` | unique looking names |
| All | letters + numbers + underscore | widest net |

---

## tips

- use **exhaustive** mode for 4-letter to check every possible name
- use **letters + numbers** for 5-letter — way more available than pure letters
- if you get lots of `[ERR]` lower the thread count to 25
- results are randomized every run so everyone checks different names

---

## discord

<div align="center">

[![Discord Server](https://img.shields.io/badge/Join%20the%20Discord-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/c95uE5ejff)

join for help, updates and to share your finds

</div>

---

## credits

<div align="center">

made by [40oo](https://github.com/40oo)

</div>
