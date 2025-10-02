#!/bin/bash
set -x

test_post_text(){
  TEXT="$(uuidgen)"
  curl -X POST http://localhost:5000/api/tx_clipboard \
    -H "Content-Type: application/json" \
    -d "$(printf '{"text":"%s"}' $TEXT)"
  
  echo $TEXT
}

test_post_files(){
  set -x

  mapfile -t FILES < <(fd ".+" -t f ~/work/books/ | shuf -n 5)
  
  ARGS=()
  for f in "${FILES[@]}"; do
    ARGS+=(-F "files=${f};filename=$(basename "$f")")
  done

  curl -X POST http://localhost:5000/api/tx_clipboard \
    -H "Content-Type: multipart/form-data" \
    "${ARGS[@]}" 

  set +x
}

set +x
if [[ $# -gt 0 ]]; then
  "$@"
else
  for fn in $(declare -F | awk '{print $3}' | grep '^test_'); do
    echo ">>> Running $fn"
    "$fn"
    echo
  done
fi
