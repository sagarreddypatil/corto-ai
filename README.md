# Quarto MinMax AI

AI for [this board game](https://en.wikipedia.org/wiki/Quarto_(board_game))

## How to use

add your moves to board.py

Convention: `((row, col), piece)`

For each action, you place the piece that the previous player gave you, and you pick the piece for the next player. So the row and col are the position for the piece you're given, not the one you're picking.

row is 0-indexed from the top, col is 0-indexed from the left

```patch
@@ -204,6 +204,19 @@ if __name__ == "__main__":
 
     # you play by writing moves here lmao
     moves = [
+        ((0, 0), 0b0110),
+        ((0, 2), 0b1011),
+        ((0, 1), 0b1111),
+        ((0, 0), 0b1001),
+        ((1, 1), 0b0101),
+        ((3, 2), 0b1100),
+        ((2, 2), 0b0001),
+        ((3, 3), 0b0000),
+        ((2, 0), 0b1000),
+        ((0, 3), 0b0010),
+        ((3, 0), 0b1010),
+        ((1, 2), 0b1101),
+        ((3, 1), 0b0011),
     ]
```

run `python board.py` to see the AI's moves.

Use `pypy3 board.py` for faster execution.

Example output:

```
1111 1011 0110 1000 
---- 1001 1010 ---- 
0000 ---- 1100 ---- 
0010 1101 0101 0001 

1
(2, 1) piece:  light square small no hole
```

It goes
```
<board state>

<eval>
<position> piece: <piece>
```

It's evaluated from the perspective of the player who's turn it is to play, after the last move. i.e. if eval is 1, you're winning, if it's -1, you're losing.
