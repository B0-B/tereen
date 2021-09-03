#!/usr/bin/env python3
from PIL import Image, ImageSequence
from shutil import get_terminal_size
from random import choice
from time import sleep
from os import system as shell


def image(path=None, imageObject=None, color=True, floor=[0,0,0], printer=False, shade=".-~%9@###", filled=False):

    '''
    Renders the image specified by path in terminal. The adaption to the terminal 
    happens by coarse graining a common mean field method to derive a transformed 
    (lower resolved) lattice. For performance sake the integration of colors 
    per segment is obtained by a stratified sampler (random Montecarlo estimate).

    Arguments
    - path [string]: path to image file
    - color [boolean]: poly-to-monochromatic switch (if disabled the filled arg will not work instead ASCII will be used)
    - floor [list]: A 3-vector RGB filter which will be added to the actual color. Each element can be a number between 0-255.
    - printer [boolean]: Outputs the rendered image directly in terminal when enabled, but generally returns it.
    - shade [string]: A 0-10 length string for texture shading. From dark to bright = small to large ASCII surface.
    - filled [boolean]: Use the max. ASCII span. Good for "HD" images, but works only if color is enabled.
    '''

    # get geometry of image and terminal
    if imageObject != None and path == None:
        img, map = imageObject, imageObject.load()
    else:
        with Image.open(path) as img:
            map = img.load()
    w, h, ycorr, wt = img.size[0], img.size[1], 2, get_terminal_size()[0]
    if wt > w: wt=w
    if w/wt < 2: stepX = 2
    else: stepX = int(w/wt)+1
    stepY = int(ycorr*stepX)
    rngX, rngY, step_inv, white_inv = range(stepX), range(stepY), 1./stepX, 1/25.5
    if filled and color: shade="█"
    ascii, shade_length = '', len(shade)
    for y in range(0,h,stepY):
        for x in range(0,w,stepX):
            c = [0,0,0]
            for i in range(stepX):
                try:
                    m = map[x+choice(rngX), y+choice(rngY)]
                    for j in range(3): c[j] += int(m[j])
                except:
                    i -= 1
            for i in range(3): c[i] = int(c[i]*step_inv)
            intensity_mean = int(0.3333*sum(c)*step_inv*white_inv)
            if color:
                ascii += "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format((c[0]+floor[0])%255, 
                (c[1]+floor[1])%255, (c[2]+floor[2])%255, shade[intensity_mean%shade_length])
            else: ascii += shade[intensity_mean%shade_length]
        ascii += '\n'
    if printer: print(ascii)
    return ascii

def gif(path, filled=True, delay=0.1, loop=False, **kwargs):
    
    '''
    Renders a gif animation and plays directly in terminal. 
    
    - filled [boolean]: Argument is True by default.
    - delay [float]: The time between frames in seconds.
    - loop [boolean]: Will loop the animation until a keyboard interrupt.
    - **kwargs: Same as image.
    '''
    
    d, dias = abs(delay), [] # collect image dias
    print(f'loading {path} ...')
    im = Image.open(path)
    for frame in ImageSequence.Iterator(im):
        dias.append(
            image(imageObject=frame.convert('RGB'), filled=True, **kwargs))
    while True:
        try:
            for t in range(len(dias)):
                print(dias[t])
                sleep(d)
        except KeyboardInterrupt:
            print(' interrupt.')
            break
        if not loop: break

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()
    path = args.file.name
    if '.gif' in path.lower():
        gif(path, filled=True)
    else:
        image(path, printer=True, filled=True)#, floor=[20,20,20])