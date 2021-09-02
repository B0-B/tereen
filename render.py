#!/usr/bin/env python3
from PIL import Image
from shutil import get_terminal_size
from random import choice


def image(path, color=True, floor=[0,0,0], shade="-~%9@###"):
    with Image.open(path) as img:
        # get geometry of image and terminal
        map = img.load()
        w, h = img.size[0], img.size[1]
        ycorr = 2
        wt = get_terminal_size()[0]
        if wt > w: wt=w
        ht = int(h*wt/(w*ycorr))
        if w/wt < 2: stepX = 2
        else: stepX = int(w/wt)+1
        stepY = int(ycorr*stepX)
        print('step', stepX)
        rngX, rngY, step_inv, white_inv = range(stepX), range(stepY), 1./stepX, 1/25.5
        if stepX < stepY: r = int(stepX/2) 
        else: r = int(stepY/2)
        ascii = ''
        print(f'image size: {w}x{h}px\nterminal size: {wt}x{ht}px')
        for y in range(0,h,stepY):
            for x in range(0,w,stepX):
                # sample a few pixel to estimate the color
                col = [0,0,0]
                for i in range(stepX):
                    try:
                        m = map[x+choice(rngX), y+choice(rngY)]
                    except:
                        pass
                    for j in range(3): col[j] += int(m[j])
                for i in range(3): col[i] = int(col[i]/stepX)
                intensity_mean = int((0.3333*sum(col)*step_inv)*white_inv)
                if color:
                    ascii += "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format((col[0]+floor[0])%255, 
                    (col[1]+floor[1])%255, (col[2]+floor[2])%255, shade[intensity_mean])
                else: ascii += shade[intensity_mean]
            ascii += '\n'
        print(ascii)
    return ascii

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()
    path = args.file.name
    image(path)