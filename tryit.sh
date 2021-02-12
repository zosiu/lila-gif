set -x
curl -X POST \
-H "Accept: application/json" \
-H "Content-type: application/json" \
-d "{\"fen\":\"$2\",
     \"pgn\":\"$3\"}" \
http://localhost:6175/from_pgn.gif --output $1.gif
