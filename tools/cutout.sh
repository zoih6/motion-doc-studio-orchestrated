#!/usr/bin/env bash
# Background removal for generated objects (crown, compass, tools…). ONE process per image (batching OOMs at 2 GB RAM).
# usage: tools/cutout.sh in.png out.png      (pip install "rembg[cpu]" once; model cached in $U2NET_HOME)
export U2NET_HOME=${U2NET_HOME:-/var/tmp/u2net}
python3 - "$1" "$2" <<'PY'
import sys; from rembg import remove, new_session; from PIL import Image
im = Image.open(sys.argv[1]).convert('RGB'); out = remove(im, session=new_session('isnet-general-use'))
bb = out.getbbox(); out.crop(bb).save(sys.argv[2]); print('cutout', sys.argv[2], out.crop(bb).size)
PY
