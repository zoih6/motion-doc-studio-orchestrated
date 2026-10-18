#!/usr/bin/env bash
# GitHub helper (token read from $GH_TOKEN_FILE, default /tmp/.ghtok — never commit tokens).
#   tools/gh.sh push BRANCH                     git push current HEAD to BRANCH
#   tools/gh.sh repo NAME "description"         create public repo under the token's user
#   tools/gh.sh release OWNER/REPO TAG FILE...  create release TAG if missing, upload/replace assets
set -e; TOK=$(cat "${GH_TOKEN_FILE:-/tmp/.ghtok}"); H="Authorization: Bearer $TOK"; API=https://api.github.com
case "$1" in
push) git -c http.extraheader="Authorization: Basic $(printf 'x-access-token:%s' "$TOK" | base64 -w0)" push -q origin "HEAD:$2" ;;
repo) curl -s -X POST -H "$H" $API/user/repos -d "{\"name\":\"$2\",\"description\":\"$3\",\"private\":false}" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('html_url'),d.get('message',''))" ;;
release) R=$2; TAG=$3; shift 3
  ID=$(curl -s -H "$H" $API/repos/$R/releases/tags/$TAG | python3 -c "import sys,json;print(json.load(sys.stdin).get('id',''))")
  [ -z "$ID" ] && ID=$(curl -s -X POST -H "$H" $API/repos/$R/releases -d "{\"tag_name\":\"$TAG\",\"name\":\"$TAG\"}" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
  for F in "$@"; do N=$(basename "$F")
    for old in $(curl -s -H "$H" "$API/repos/$R/releases/$ID/assets?per_page=100" | python3 -c "import sys,json;print(' '.join(str(a['id']) for a in json.load(sys.stdin) if a['name']=='$N'))"); do curl -s -X DELETE -H "$H" $API/repos/$R/releases/assets/$old; done
    case "$N" in *.mp4) CT=video/mp4;; *.jpg|*.jpeg) CT=image/jpeg;; *.png) CT=image/png;; *) CT=application/octet-stream;; esac
    curl -s -H "$H" -H "Content-Type: $CT" --data-binary @"$F" "https://uploads.github.com/repos/$R/releases/$ID/assets?name=$N" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('state'),d.get('browser_download_url'))"
  done ;;
*) sed -n 2,5p "$0" ;;
esac
