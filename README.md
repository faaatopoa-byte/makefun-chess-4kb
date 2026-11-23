[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/faaatopoa-byte/makefun-chess-4kb/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/faaatopoa-byte/makefun-chess-4kb/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# Tiny chess engine in ≤ 4 KB of Python — make.fun "tiny-chess-01"

A complete, deterministic chess engine in one Python file:
`main.py` is **4,088 bytes** (cap: 4,096 as committed), Python 3.13
stdlib only, no packing or code generation — the file on GitHub is
the file that plays, written line by line in the build session whose
transcript ships with the entry.

## How it plays

- Reads the environment base URL from `MAKEFUN_ENV_URL`.
- `POST /game {}` serves each game; while `status == "your_move"` it
  computes a move from the served `fen` and answers
  `POST /move {game, move}` (UCI).
- The played move is verified against the environment's own
  `legal_moves` list before it is sent, so an illegal move can
  never be sent. This engine never resigns.

## Engine design

- 64-square board; full legal move generation (castling with all
  legality conditions, promotions to Q/R/B/N, pins and checks),
  verified against python-chess (below). One deliberate size
  trade: it does not play en-passant captures.
- Negamax with alpha-beta pruning, iterative deepening to a
  **fixed node budget** (50,000 nodes per move, no clock reads:
  deterministic — the same position always gets the same move),
  quiescence search over captures, capture-value move ordering.
- Evaluation: material (P100 N320 B330 R500 Q900) + pawn
  advancement, knight/bishop centrality, and a king term that
  flips from shelter to centrality in the endgame.
- Castling rights are re-read from the served FEN on every move.

## Verified results (measured 2026-11-23)

- Perft vs known values: startpos d1–d3 = 20 / 400 / 8,902, exact;
  Kiwipete d1 = 48, exact (deeper Kiwipete counts differ only by
  en-passant branches, which the engine omits by design).
- Differential test vs python-chess 1.11.2 over 4,533 positions
  from random games: identical legal move sets everywhere
  (en-passant captures excluded).
- Mock-environment trial with the committed file: two full
  games (one as White, one as Black) against a random mover,
  every sent move legal, clean exit when the env reported done.
- Finds mate in 1 (back-rank, scholar's mate, fool's mate).
- Speed: worst move ≈ 3 s at the node budget on a shared VM
  (limit: 10 s per move).
- Size: `main.py` = 4,088 bytes ≤ 4,096; repo snapshot ≤ 8,192 bytes.

## Files

- `main.py` — the entry (4,088 bytes).
- `LICENSE` — MIT.
