#Some key imports.
#Struct is used to create the actual bytes.
#It is super handy for this type of thing.
import struct, random

#Function to write a bmp file.  It takes a dictionary (d) of
#header values and the pixel data (bytes) and writes them
#to a file.  This function is called at the bottom of the code.
def bmp_write(d,byte):
    mn1 = struct.pack('<B',d['mn1'])
    mn2 = struct.pack('<B',d['mn2'])
    filesize = struct.pack('<L',d['filesize'])
    undef1 = struct.pack('<H',d['undef1'])
    undef2 = struct.pack('<H',d['undef2'])
    offset = struct.pack('<L',d['offset'])
    headerlength = struct.pack('<L',d['headerlength'])
    width = struct.pack('<L',d['width'])
    height = struct.pack('<L',d['height'])
    colorplanes = struct.pack('<H',d['colorplanes'])
    colordepth = struct.pack('<H',d['colordepth'])
    compression = struct.pack('<L',d['compression'])
    imagesize = struct.pack('<L',d['imagesize'])
    res_hor = struct.pack('<L',d['res_hor'])
    res_vert = struct.pack('<L',d['res_vert'])
    palette = struct.pack('<L',d['palette'])
    importantcolors = struct.pack('<L',d['importantcolors'])
    #create the outfile
    outfile = open('bitmap_imagevert.bmp','wb')
    #write the header + the bytes
    outfile.write(mn1+mn2+filesize+undef1+undef2+offset+headerlength+width+height+\
                  colorplanes+colordepth+compression+imagesize+res_hor+res_vert+\
                  palette+importantcolors+byte)
    outfile.close()

###################################
def main():
    #Here is a minimal dictionary with header values.
    #Of importance is the offset, headerlength, width,
    #height and colordepth.
    #Edit the width and height to your liking.
    #These header values are described in the bmp format spec.
    #You can find it on the internet. This is for a Windows
    #Version 3 DIB header.
    d = {
        'mn1':66,
        'mn2':77,
        'filesize':0,
        'undef1':0,
        'undef2':0,
        'offset':54,
        'headerlength':40,
        'width':200,
        'height':200,
        'colorplanes':0,
        'colordepth':24,
        'compression':0,
        'imagesize':0,
        'res_hor':0,
        'res_vert':0,
        'palette':0,
        'importantcolors':0
        }

    #Function to generate a random number between 0 and 255
    def rand_color():
        x = random.randint(0,255)
        return x

    def rand_color_mem2d(buddy_color = None):
        """


        :return:
        """
        global last_color
        if last_color is not None:
            #print ('not none')
            if buddy_color is not None:
                r = random.randint(buddy_color[0] - 10, buddy_color[0] + 10)
            else:
                r = random.randint(last_color[0] - 10, last_color[0] + 10)
            if r < 0:
                r *= -1
            elif r > 255:
                r = 255 - (r - 255)
            if buddy_color is not None:
                g = random.randint(buddy_color[1] - 10, buddy_color[1] + 10)
            else:
                g = random.randint(last_color[1] - 10, last_color[1] + 10)
            if g < 0:
                g *= -1
            elif g > 255:
                g = 255 - (g - 255)
            if buddy_color is not None:
                b = random.randint(buddy_color[2] - 10, buddy_color[2] + 10)
            else:
                b = random.randint(last_color[2] - 10, last_color[2] + 10)
            if b < 0:
                b *= -1
            elif b > 255:
                b = 255 - (b - 255)
        else:
            #print ('none')
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
        x = [r,g,b]
        last_color = x
        return x

    #Build the byte array.  This code takes the height
    #and width values from the dictionary above and
    #generates the pixels row by row.  The row_mod and padding
    #stuff is necessary to ensure that the byte count for each
    #row is divisible by 4.  This is part of the specification.
    byte = bytes()
    for row in range(d['height']-1,-1,-1):# (BMPs are L to R from the bottom L row)
        #(d['height'] - (row+1))
        bitmapList.append([])
        for column in range(d['width']):
            if (d['height'] - (row+1) > 0):
                color = rand_color_mem2d(bitmapList[d['height'] - (row+1) - 1][column])
            else:
                color = rand_color_mem2d()
            bitmapList[d['height'] - (row+1)].append(color)
            b = color[1]
            g = color[2]
            r = color[0]
            pixel = struct.pack('<BBB',b,g,r)
            #pixel.unpack('<BBB')
            byte = byte + pixel
        row_mod = (d['width']*d['colordepth']/8) % 4
        if row_mod == 0:
            padding = 0
        else:
            padding = (4 - row_mod)
        padbytes = bytes()
        for i in range(padding):
            x = struct.pack('<B',0)
            padbytes = padbytes + x
        byte = byte + padbytes

    #call the bmp_write function with the
    #dictionary of header values and the
    #bytes created above.
    bmp_write(d,byte)
    print ('list', bitmapList)
last_color = None
last_row = None
bitmapList = list()
if __name__ == '__main__':
    main()
