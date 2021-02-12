lila-gif
========

Webservice to render Gifs of chess positions and games, and stream them
frame by frame.

![example](/example.gif)

Usage
-----

```
lila-gif 0.1.0

USAGE:
    lila-gif [OPTIONS]

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information

OPTIONS:
        --address <address>    Listen on this address [default: 127.0.0.1]
        --port <port>          Listen on this port [default: 6175]
```

HTTP API
--------

### `POST http://localhost:6175/from_pgn.gif`

```sh
curl -X POST \
-H "Accept: application/json" \
-H "Content-type: application/json" \
-d '{"fen":"8/8/8/4k3/8/8/3Q4/4K3 w - - 0 1",
     "pgn":"1. Qd7 Ke4 2. Kf2 Ke5 3. Kf3 Kf6 4. Kf4 Kg6 5. Qe7 Kh6 6. Kf5 Kh5 7. Qg5# *"}' \
http://localhost:6175/from_pgn.gif --output your.gif
```

### `GET /image.gif`

```
curl http://localhost:6175/image.gif?fen=4k3/6KP/8/8/8/8/7p/8 --output image.gif
```

name | type | default | description
--- | --- | --- | ---
**fen** | ascii | *starting position* | FEN of the position. Board part is sufficient.
white | utf-8 | *none* | Name of the white player. Known chess titles are highlighted. Limited to 100 bytes.
black | utf-8 | *none* | Name of the black player. Known chess titles are highlighted. Limited to 100 bytes.
comment | utf-8 | `https://github.com/niklasf/lila-git` | Comment to be added to GIF meta data. Limited to 255 bytes.
lastMove | ascii | *none* | Last move in UCI notation (like `e2e4`).
check | ascii | *none* | Square of king in check (like `e1`).
orientation | | `white` | Pass `black` to flip the board.

### `POST /game.gif`

```javascript
{
  "white": "Molinari", // optional
  "black": "Bordais", // optional
  "comment": "https://www.chessgames.com/perl/chessgame?gid=1251038", // optional
  "orientation": "white", // default
  "delay": 50, // default frame delay in centiseconds
  "frames": [
    // [...]
    {
      "fen": "r1bqkb1r/pp1ppppp/5n2/2p5/2P1P3/2Nn2P1/PP1PNP1P/R1BQKB1R w KQkq - 1 6",
      "delay": 500, // optionally overwrite default delay
      "lastMove": "b4d3", // optionally highlight last move
      "check": "e1" // optionally highlight king
    }
  ]
}
```

### `GET /example.gif`

```
curl http://localhost:6175/example.gif --output example.gif
```

Render an [example game](https://lichess.org/Q0iQs5Zi).

Technique
---------

Instead of rendering vector graphics at runtime, all pieces are prerendered
on every possible background. This allows preparing a minimal color palette
ahead of time. (Pieces are not just black and white, but need other colors
for anti-aliasing on the different background colors).

![Sprite](/theme/sprite_blue_kosal.gif)

All thats left to do at runtime, is copying sprites and Gif encoding.
More than 95% of the rendering time is spent in LZW compression.

For animated games, frames only contain the changed squares on transparent
background. The example below is the last frame of the animation.

![Example frame](/example-frame.gif)

License
-------

lila-gif is licensed under the GNU Affero General Public License, version 3 or
any later version, at your option.

The generated images include text in
[Noto Sans](https://fonts.google.com/specimen/Noto+Sans) (Apache License 2.0),
a piece set from [lichess](https://github.com/ornicar/lila/tree/master/public/piece/kosal) (GNU Affero General Public License 3),
and a piece set by
[Colin M.L. Burnett](https://en.wikipedia.org/wiki/User:Cburnett)
(GFDL or BSD or GPL).
