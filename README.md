# Tiny chess engine in ≤ 4 KB of Python — make.fun "tiny-chess-01"

A complete, deterministic chess engine whose entire entry file, `main.py`,
is **3,998 bytes** (cap: 4,096 bytes as committed), Python 3.13 stdlib only.

## How it plays

- Reads the environment base URL from `MAKEFUN_ENV_URL`.
- `POST /game {}` creates games; answers carry `game`, `fen`,
  `legal_moves` (UCI), `status`.
- While `status == "your_move"`: picks a move and answers
  `POST /move {game, move}`.
- The played move is always chosen from the environment's own
  `legal_moves` list, so a move the environment considers illegal can
  never be sent. This engine never resigns.

## Engine design

- 64-square board, make/unmake with an undo stack (captured piece,
  castling rights, en-passant square, castling rook move).
- Full legal move generation: castling (with all legality conditions),
  en-passant (including the pinned-ep case), promotions to Q/R/B/N.
- Negamax with alpha-beta pruning, iterative deepening to a **fixed node
  budget** (24,000 nodes — no clock anywhere, so play is deterministic
  and finals replay move-for-move), quiescence search over captures and
  promotions, MVV-LVA + promotion move ordering.
- Evaluation: material (P100 N320 B330 R500 Q975) + classic piece-square
  tables for all six piece types, tapered by game phase.

## The 4 KB packing

`main.py` is a self-contained lzma-compressed (preset 9 extreme),
base85-encoded payload of the readable dev engine behind a 2-line `exec`
stub. Compressed-payload unpacking by `exec` is explicitly allowed by the
contest rules and counts toward the 4,096 bytes. It reads, imports, or
execs no other repository file. (The packer that produced it renames
identifiers at the token level; a `__slots__` rename mismatch found in
the first packed trial was fixed before the final pack.)

## Verified results (measured 2026-11-23)

- Perft vs known values: startpos d3 = 8,902; Kiwipete d2 = 2,039;
  en-passant position d3 = 2,812; promotion position d2 = 264 — all match.
- Differential test vs python-chess 1.11.2 over 12 random games:
  identical legal move sets at every ply.
- Mock-environment trial with the committed `main.py` itself: exit 0,
  both games won by checkmate, 47 engine moves; an identical second run
  reproduced the exact same 47 moves (determinism confirmed), and a
  replay confirmed every move legal.
- Speed: ~0.75–1.12 s per move at the 24,000-node budget on a shared VM
  (limits: 10 s/move hard, ~3 s/move average).
- Size: `main.py` = 3,998 bytes ≤ 4,096.

## Files

- `main.py` — the entry (3,998 bytes).
- `LICENSE` — MIT.
