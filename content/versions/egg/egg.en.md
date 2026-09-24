---
title: "The 060 build"
description: "How big the 060 build was, how big its script DLL was, and what changed since."
translated: 2026-09-25
nav_label: "The egg"
icon: lucide/package
---

# The 060 build

<p class="kicker">2026-05-14 · how it looked five months ago</p>

This page is a trial run of the freeze mechanism, but the numbers in it are **real** —
read straight out of `060.zip`. It records one build of the editor, version 060.

|  |  |
| --- | --- |
| Version | 060 |
| Built | 2026-05-14 |
| Archive | 30.6 MiB (`060.zip`) |
| Unpacked | 81.8 MiB, 138 files |
| `1007.exe` | 666,624 bytes |
| `UnityPlayer.dll` | 31,100,840 bytes |
| `Assembly-CSharp.dll` | 269,824 bytes |
| SHA-256 of that DLL | `a8ea2a0e…ded4b` (full: `a8ea2a0ed1e5c4a9d916aca64b9943078098ca36280c073d09d2a05bb77ded4b`) |

## What grew over those five months

`Assembly-CSharp.dll` is where the editor's behaviour lives — tools, panels, drawing
logic. Its size is a rough scale for how many tools were added:

| Version | Built | `Assembly-CSharp.dll` |
| --- | --- | --- |
| 060 | 2026-05-14 | 269,824 bytes |
| 070 | 2026-05-20 | 305,152 bytes |
| 080 | 2026-06-02 | 322,560 bytes |
| 090 | 2026-07-26 | 372,224 bytes |
| 091 | 2026-08-30 | 378,368 bytes |
| 0100 | 2026-08-30 | 389,120 bytes |
| 0101 | 2026-09-06 | 398,336 bytes |

That is 47% growth from 060 to 0101, while `UnityPlayer.dll` did not change a single
byte — **everything that grew is script**.

## The one place the handbook changed with it

As tools were added, the notes changed once too. The `TerrainBash` section of 0101
records that "using this tool, there may be a spare adjuster bar in the bottom left,
which does nothing at all" — 060 did not have that bar yet.
