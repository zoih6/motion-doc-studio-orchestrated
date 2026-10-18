#!/usr/bin/env python3
"""Build a simple labeled contact sheet from diagnostic/reference stills."""
import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output')
    ap.add_argument('images', nargs='+')
    ap.add_argument('--cols', type=int, default=4)
    ap.add_argument('--cell-width', type=int, default=320)
    ap.add_argument('--cell-height', type=int, default=220)
    ap.add_argument('--label-height', type=int, default=28)
    args=ap.parse_args()

    files=[Path(x) for x in args.images]
    rows=(len(files)+args.cols-1)//args.cols
    sheet=Image.new('RGB',(args.cols*args.cell_width,rows*(args.cell_height+args.label_height)),'white')
    draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(files):
        img=Image.open(p).convert('RGB')
        thumb=ImageOps.contain(img,(args.cell_width,args.cell_height))
        x=(i%args.cols)*args.cell_width+(args.cell_width-thumb.width)//2
        y=(i//args.cols)*(args.cell_height+args.label_height)+(args.cell_height-thumb.height)//2
        sheet.paste(thumb,(x,y))
        label=p.name[:45]
        draw.text(((i%args.cols)*args.cell_width+6,(i//args.cols)*(args.cell_height+args.label_height)+args.cell_height+5),label,fill='black')
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    sheet.save(args.output,quality=92)

if __name__=='__main__':
    main()
