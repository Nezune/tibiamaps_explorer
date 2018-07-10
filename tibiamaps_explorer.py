from PIL import Image
from PIL import ImagePalette
from shutil import copy2
from os import listdir

def mono(pixel):
    pixel = [palette[pixel][0],palette[pixel][1],palette[pixel][2]]
    newpixel = [0,0,0]
    if (pixel[0]/51+pixel[1]/51+pixel[2]/51) % 3 == 2:
        newpixel = [51,51,51]
    l = int((pixel[0]/51+pixel[1]/51+pixel[2]/51) / 3)
    newpixel[0] += l*51
    newpixel[1] += l*51
    newpixel[2] += l*51
    return newpixel
def invert(pixel):
    return [abs(palette[pixel][0]-255),abs(palette[pixel][1]-255),abs(palette[pixel][2]-255)]
def shift1(pixel):
    return [palette[pixel][1],palette[pixel][2],palette[pixel][0]]
def shift2(pixel):
    return [palette[pixel][2],palette[pixel][0],palette[pixel][1]]

mode = ""
while mode != "grid" and mode != "mono" and mode != "invert" and mode != "shift1" and mode != "shift2":
    mode = input("MODES: grid, mono, invert, shift1, shift2\r\n").strip()

palette = None
for file in listdir("./minimap"):
    if file[-3:] != "png" or not "Minimap_Color_" in file:
        copy2("./minimap/"+file, "./output/")
        continue
    print(file)
    im = Image.open("./minimap/"+file)
    px = 0
    py = 0
    if palette is None:
        palette = []
        impalette = im.getpalette()
        for r,g,b in zip(*[iter(impalette)]*3):
            palette.append([r,g,b])
    while py < im.size[1]:
        item_pixel = im.getpixel((px, py))
        if mode == "grid":
            if item_pixel != 0 and px % 2 == 0 and py % 2 == 0:
                im.putpixel((px,py), 0)
        elif mode == "mono":
            if not(palette[item_pixel][0] == palette[item_pixel][1] == palette[item_pixel][2]):
                im.putpixel((px,py), palette.index(mono(item_pixel)))
        elif mode == "invert":
            if item_pixel != 0:
                im.putpixel((px,py), palette.index(invert(item_pixel)))
        elif mode == "shift1":
            if item_pixel != 0:
                im.putpixel((px,py), palette.index(shift1(item_pixel)))
        elif mode == "shift2":
            if item_pixel != 0:
                im.putpixel((px,py), palette.index(shift2(item_pixel)))
        px += 1
        if px == im.size[0]:
            px = 0
            py += 1
    im.save('./output/'+file)
