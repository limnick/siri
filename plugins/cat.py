import Image
import ImageDraw
import ImageFont
import textwrap
import os.path, random, string
from os import listdir
from random import choice
from util import hook, http

#TEXT = """
#I tell you I have been in the editorial business going on fourteen
#years, and it is the first time I ever heard of a man's having to know
#anything in order to edit a newspaper. You turnip!
#"""

def drawtext(draw, text, font, color, bbox):
    shadowcolor = "black"
    x0, y0, x1, y1 = bbox # note: y1 is ignored
    space = draw.textsize(" ", font)[0]
    #font2 = ImageFont.truetype("Impact.ttf", 51)
    words = text.split()
    x = x0; y = y0; h = 0
    for word in words:
        # check size of this word
        w, h = draw.textsize(word, font)
        # figure out where to draw it
        if x > x0:
            x += space
            if x + w > x1:
                # new line
                x = x0
                y += h
        #draw.text((x, y), word, font=font, fill=color)
        
        # thin border
        draw.text((x-.5, y-.5), word, font=font, fill=shadowcolor)
        draw.text((x-1.5, y-1.5), word, font=font, fill=shadowcolor)
        draw.text((x-1.5, y+1.5), word, font=font, fill=shadowcolor)
        draw.text((x+1.5, y-1.5), word, font=font, fill=shadowcolor)
        
        #text
        draw.text((x,y), word, font=font, fill=color)
        
        x += w
    return y + h

def randomFilename(chars="1234567890ABCDEFabcdef", length=16, prefix='',
                   suffix='', verify=True, attempts=10):
    for attempt in range(attempts):
        filename = ''.join([random.choice(chars) for i in range(length)])
        filename = prefix + filename + suffix
        if not verify or not os.path.exists(filename):
            return filename

ext2conttype = {"jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "gif": "image/gif"}

def content_type(filename):
    return ext2conttype[filename[filename.rfind(".")+1:].lower()]

def isimage(filename):
    """true if the filename's extension is in the content-type lookup"""
    filename = filename.lower()
    return filename[filename.rfind(".")+1:] in ext2conttype

def random_file(dir):
    """returns the filename of a randomly chosen image in dir"""
    images = [f for f in listdir(dir) if isimage(f)]
    return choice(images)

@hook.command
def catte(inp, nick='', chan=None, say=None, db=None, reply=None):
    
    text = inp
    dir = "/home/jewtron/public_html/cats/"
    r = random_file(dir)
    image = dir + r

    im = Image.open(image)
    imgWidth = im.size[0]
    imgHeight = im.size[0]
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/home/jewtron/skybot/plugins/Impact.ttf", 55)
    bbox = (50, 0, imgWidth, imgHeight)

    drawtext(draw, text, font, "white", bbox)

    catName = randomFilename(suffix=".jpg")
    catDir = "/home/jewtron/public_html/"
    catImage = catDir + catName
    im.save(catImage)
    if inp == '':
        output = "http://macros.cattes.us/cats/" + r
        say("plugin being re-written.")
    else:
        output = "http://macros.cattes.us/" + catName + " - Caption added to YOSCAT"
        say("plugin being re-written.")


if __name__ == "__main__":

    def test():

        #im = Image.new("RGB", (500, 500), "white")
        text = "yospos bitch yospos bitch yospos bitch yospos bitch"
        dir = "/home/jewtron/public_html/cats/"
        r = random_file(dir)
        image = dir + r

        im = Image.open(image)
        imgWidth = im.size[0]  
        imgHeight = im.size[1]
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("Impact.ttf", 50)
        bbox = (50, 0, imgWidth, imgHeight)

        #draw.rectangle(bbox, outline="red")

        drawtext(draw, text, font, "white", bbox)
        
        catName = randomFilename(suffix=".jpg")
        catDir = "/home/jewtron/public_html/"
        catImage = catDir + catName
        im.save(catImage)
        print catImage
        print "http://macros.cattes.us/" + catName
        #im.show()

    #test()
