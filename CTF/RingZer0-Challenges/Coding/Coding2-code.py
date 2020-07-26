#!/usr/bin/python
#
# punchcard.py 
#
# Copyright (C) 2011: Michael Hamilton
# The code is GPL 3.0(GNU General Public License) ( http://www.gnu.org/copyleft/gpl.html )
#
from PIL import Image
import sys
from optparse import OptionParser

# Counting on the Image, there's 80 units at column & 12 units at row
c_Cols = 80
c_Rows = 12

# Found measurements at http://www.quadibloc.com/comp/cardint.htm
# In the beginning, there was the 45-column card.
# Or, at least, I had originally thought so, but it turns out that the cards used by Herman Hollerith for the 1890 census had 28 columns of holes.
# Similar cards were still being used in the 1910 census.
# The 28-column cards used in the 1890 census had the 3 1/4" high and 7 3/8" wide dimensions of a modern card; shorter cards were also used for some purposes, 
# for example, cards with 24 columns, and those cards were 3 1/4" high and 6 5/8" wide.
c_Width = 7.0 + 3.0/8.0         # Inches
c_Height = 3.25                 # Inches
c_Col_Width = 0.087             # Inches
c_Hole_Width = 0.055            # Inches IBM, 0.056 Control Data
c_Row_Height = 0.25             # Inches
c_Hole_Height = 0.125           # Inches
cm_TopBot = 3.0/16.0            # Inches at top and bottom (Margin)
cm_Side = 0.2235                # Inches on each side


cm_Side_RATIO = cm_Side/c_Width                 # as proportion of card width (margin/width)
cm_Top_RATIO = cm_TopBot/c_Height               # as proportion of card height (margin/height)
c_Row_Height_RATIO = c_Row_Height/c_Height      # as proportion of card height - works
c_Col_Width_RATIO = c_Col_Width/c_Width         # as proportion of card height - works
c_Hole_Height_RATIO = c_Hole_Height/c_Height    # as proportion of card height - works
c_Hole_Width_RATIO = c_Hole_Width/c_Width       # as a proportion of card width

BRIGHTNESS_THRESHOLD = 200          # pixel brightness value (i.e. (R+G+B)/3)

IBM_MODEL_029_KEYPUNCH = """
    /&-0123456789ABCDEFGHIJKLMNOPQR/STUVWXYZ:#@'="`.<(+|!$*);^~,%_>? |
12 / O           OOOOOOOOO                        OOOOOO             |
11|   O                   OOOOOOOOO                     OOOOOO       |
 0|    O                           OOOOOOOOO                  OOOOOO |
 1|     O        O        O        O                                 |
 2|      O        O        O        O       O     O     O     O      |
 3|       O        O        O        O       O     O     O     O     |
 4|        O        O        O        O       O     O     O     O    |
 5|         O        O        O        O       O     O     O     O   |
 6|          O        O        O        O       O     O     O     O  |
 7|           O        O        O        O       O     O     O     O |
 8|            O        O        O        O OOOOOOOOOOOOOOOOOOOOOOOO |
 9|             O        O        O        O                         | 
  |__________________________________________________________________|"""

translate = None
if translate == None:
    translate = {}
    # Turn the ASCII art sideways and build a hash look up for 
    # column values, for example:
    #   (O, , ,O, , , , , , , , ):A
    #   (O, , , ,O, , , , , , , ):B
    #   (O, , , , ,O, , , , , , ):C
    rows = IBM_MODEL_029_KEYPUNCH[1:].split('\n');
    rotated = [[ r[i] for r in rows[0:13]] for i in range(5, len(rows[0]) - 1)]
    for v in rotated:
        translate[tuple(v[1:])] = v[0]
    #print translate

# generate a range of floats
def drange(start, stop, step=1.0):
    r = start
    while (step >= 0.0 and r < stop) or (step < 0.0 and r > stop):
        yield r
        r += step

# Represents a punchcard image plus scanned data
class PunchCard(object):
    
    def __init__(self, image, bright=-1, debug=False, xstart=0, xstop=0, ystart=0, ystop=0, xadjust=0):
        pass
        self.text = ''
        self.decoded = []
        self.surface = [] 
        self.debug = debug
        self.threshold = 0
        self.ymin = ystart
        self.ymax = ystop
        self.xmin = xstart
        self.xmax = xstop
        self.xadjust = xadjust
        self.image = image
        self.pix = image.load()
        self._crop()
        self._scan(bright)
    
    # Brightness is the average of RGB values
    def _brightness(self, pixel):
        #print max(pixel)
        return ( pixel[0] + pixel[1] + pixel[2] ) / 3

    # For highlighting on the debug dump
    def _flip(self, pixel):
        return max(pixel)

    # The search is started from the "crop" edges.
    # Either use crop boundary of the image size or the valyes supplied
    # by the command line args
    def _crop(self):
        self.xsize, self.ysize = image.size
        if self.xmax == 0:
            self.xmax = self.xsize
        if self.ymax == 0:
            self.ymax = self.ysize
        self.midx = self.xmin + (self.xmax - self.xmin) / 2 + self.xadjust
        self.midy = self.ymin + (self.ymax - self.ymin) / 2

    # heuristic for finding a reasonable cutoff brightness
    def _find_threshold_brightness(self):
        left = self._brightness(self.pix[self.xmin, self.midy])
        right = self._brightness(self.pix[self.xmax - 1, self.midy])
        return min(left, right, BRIGHTNESS_THRESHOLD) - 10
        vals = []
        last = 0
        for x in range(self.xmin,self.xmax):
            val = self._brightness(self.pix[x, self.midy])
            if val > last:
                left = val
            else:
                break
            last = val
        for x in range(self.xmax,self.xmin, -1):
            val = self._brightness(self.pix[x, self.midy])
            if val > last:
                right = val
            else:
                break
            right = val
        print (left, right)
        return min(left, right,200)
        
        for x in range(self.xmin,self.xmax):
            val = self._brightness(self.pix[x, self.midy])
            vals.append(val)
        vals.sort()
        last_val = vals[0]
        biggest_diff = 0
        threshold = 0
        for val in vals:
            diff = val - last_val
            #print val, diff
            if val > 127 and val < 200 and diff >= 5:
                biggest_diff = diff
                threshold = val
            last_val = val
        if self.debug:
            print ("Threshold diff=", biggest_diff, "brightness=", val)
        return threshold - 10
    
    # Find the left and right edges of the data area at probe_y and from that
    # figure out the column and hole vertical dimensions at probe_y.
    def _find_data_horiz_dimensions(self, probe_y):
        left_border, right_border = self.xmin, self.xmax - 1
        for x in range(int(self.xmin), int(self.midx)):            
            if self._brightness(self.pix[x,  probe_y]) < self.threshold:
                left_border = x
                break
        for x in range(int(self.xmax)-1,  int(self.midx),  -1):
            if self._brightness(self.pix[x,  probe_y]) < self.threshold:
                right_border = x
                break
        width = right_border - left_border
        cm_Side_width = int(width * cm_Side_RATIO)
        data_left_x = left_border + cm_Side_width
        #data_right_x = right_border - cm_Side_width
        data_right_x = data_left_x + int((c_Cols * width) * c_Col_Width/c_Width)
        col_width = width * c_Col_Width_RATIO
        hole_width = width * c_Hole_Width_RATIO
        #print col_width
        if self.debug:
            # mark left and right edges on the copy
            for y in range(probe_y - self.ysize/100, probe_y + self.ysize/100):
                self.debug_pix[left_border if left_border > 0 else 0,y] = 255
                self.debug_pix[right_border if right_border < self.xmax else self.xmax - 1,y] = 255
            for x in range(1, (self.xmax - self.xmin) / 200):
                self.debug_pix[left_border + x, probe_y] = 255
                self.debug_pix[right_border - x, probe_y] = 255
                
        return data_left_x, data_right_x,  col_width, hole_width
 
    # find the top and bottom of the data area and from that the 
    # column and hole horizontal dimensions 
    def _find_data_vert_dimensions(self):
        top_border, bottom_border = self.ymin, self.ymax
        for y in range(int(self.ymin), int(self.midy)):
            #print pix[midx,  y][0] 
            if self._brightness(self.pix[self.midx,  y]) < self.threshold:
                top_border = y
                break
        for y in range(int(self.ymax) - 1,  int(self.midy), -1):
            if self._brightness(self.pix[self.midx,  y]) < self.threshold:
                bottom_border = y
                break
        c_Height = bottom_border - top_border
        cm_Top = int(c_Height * cm_Top_RATIO)
        data_begins = top_border + cm_Top
        hole_height = int(c_Height * c_Hole_Height_RATIO)
        data_top_y = data_begins + hole_height / 2
        col_height = int(c_Height * c_Row_Height_RATIO)
        if self.debug:
            # mark up the copy with the edges
            for x in range(self.xmin, self.xmax-1):
                self.debug_pix[x,top_border] = 255
                self.debug_pix[x,bottom_border] = 255
        if self.debug:
            # mark search parameters 
            for x in range(self.midx - self.xsize/20, self.midx + self.xsize/20):
               self.debug_pix[x,self.ymin] = 255
               self.debug_pix[x,self.ymax - 1] = 255
            for y in range(0, self.ymin):
               self.debug_pix[self.midx,y] = 255
            for y in range(self.ymax - 1, self.ysize-1):
               self.debug_pix[self.midx,y] = 255
        return data_top_y, data_top_y + col_height * 11, col_height, hole_height

    def _scan(self, bright=-1):
        if self.debug:
            # if debugging make a copy we can draw on
            self.debug_image = self.image.copy()
            self.debug_pix = self.debug_image.load()
            
        self.threshold = bright if bright > 0 else self._find_threshold_brightness()    
        #x_min, x_max,  col_width = self._find_data_horiz_dimensions(image, pix, self.threshold, self.ystart, self.ystop)
        y_data_pos, y_data_end, col_height, hole_height = self._find_data_vert_dimensions()
        data = {}
        
        # Chads are narrow so find then heuristically by accumulating pixel brightness
        # along the row.  Should be forgiving if the image is slightly wonky.
        y = y_data_pos #- col_height/8
        for row_num in range(c_Rows):
            probe_y = y + col_height if row_num == 0 else ( y - col_height if row_num == c_Rows -1 else y )  # Line 0 has a corner missing
            x_data_left, x_data_right,  col_width, hole_width = self._find_data_horiz_dimensions(probe_y)
            left_edge = -1 # of a punch-hole
            for x in range(x_data_left,  x_data_right):
                # Chads are tall so we can be sure if we probe around the middle of their height
                val = self._brightness(self.pix[x, y])
                if val >= self.threshold:
                    if left_edge == -1:
                        left_edge = x
                    if self.debug:
                        self.debug_pix[x,y] = self._flip(self.pix[x,y])
                else:
                    if left_edge > -1:
                        hole_length = x - left_edge
                        if hole_length >= hole_width * 0.75:
                            col_num = int((left_edge + hole_length / 2.0 - x_data_left) / col_width + 0.25)  
                            data[(col_num, row_num)] = hole_length
                        left_edge = -1
            if (self.debug):
                # Plot where holes might be on this row
                expected_top_edge = y - hole_height / 2
                expected_bottom_edge = y + hole_height / 2
                blue = 255 * 256 * 256
                for expected_left_edge in drange(x_data_left, x_data_right - 1, col_width):
                    for y_plot in drange(expected_top_edge, expected_bottom_edge, 2):
                        self.debug_pix[expected_left_edge,y_plot] = blue
                        #self.debug_pix[x + hole_width/2,yline] = 255 * 256 * 256
                        self.debug_pix[expected_left_edge + hole_width,y_plot] = blue
                    for x_plot in drange(expected_left_edge, expected_left_edge + hole_width):
                        self.debug_pix[x_plot, expected_top_edge] = blue
                        self.debug_pix[x_plot, expected_bottom_edge] = blue
            y += col_height

        if self.debug:
            self.debug_image.show()
            # prevent run-a-way debug shows causing my desktop to run out of memory
            raw_input("Press Enter to continue...")
        self.decoded = []
        # Could fold this loop into the previous one - but would it be faster?
        for col in range(0, c_Cols):
            col_pattern = []
            col_surface = []
            for row in range(c_Rows):
                key = (col, row)
                # avergage for 1/3 of a column is greater than the threshold
                col_pattern.append('O' if key in data else ' ')
                col_surface.append(data[key] if key in data else 0)
            tval = tuple(col_pattern)
            global translate
            self.text += translate[tval] if tval in translate else '@'
            self.decoded.append(tval)
            self.surface.append(col_surface)
           

        return self

    # ASCII art image of card
    def dump(self, id, raw_data=False):
        print (' Card Dump of Image file:', id, 'Format', 'Raw' if raw_data else 'Dump', 'threshold=', self.threshold)
        print (' ' + '123456789-' * (c_Cols/10))
        print (' ' + '_' * c_Cols + ' ')
        print ('/' + self.text +  '_' * (c_Cols - len(self.text)) + '|')
        for rnum in range(len(self.decoded[0])):
            sys.stdout.write('|')
            if raw_data:
                for val in self.surface:
                    sys.stdout.write(("(%d)" % val[rnum]) if val[rnum] != 0 else '.' )
            else:
                for col in self.decoded:
                    sys.stdout.write(col[rnum] if col[rnum] == 'O' else '.')
            print ('|')
        print ('`' + '-' * c_Cols + "'")
        print (' ' + '123456789-' * (c_Cols/10))
        print ('')
         
            
if __name__ == '__main__':
    
    usage = """usage: %prog [options] image [image...]
    decode punch card image into ASCII."""
    parser = OptionParser(usage)
    parser.add_option('-b', '--bright-threshold', type='int', dest='bright', default=-1, help='Brightness (R+G+B)/3, e.g. 127.')
    parser.add_option('-s', '--side-margin-ratio', type='float', dest='side_margin_ratio', default=cm_Side_RATIO, help='Manually set side margin ratio (sideMargin/cardWidth).')
    parser.add_option('-d', '--dump', action='store_true', dest='dump', help='Output an ASCII-art version of the card.')
    parser.add_option('-i', '--display-image', action='store_true', dest='display', help='Display an anotated version of the image.')
    parser.add_option('-r', '--dump-raw', action='store_true', dest='dumpraw', help='Output ASCII-art with raw row/column accumulator values.')
    parser.add_option('-x', '--x-start', type='int', dest='xstart', default=0, help='Start looking for a card edge at y position (pixels)')
    parser.add_option('-X', '--x-stop', type='int', dest='xstop', default=0, help='Stop looking for a card edge at y position')
    parser.add_option('-y', '--y-start', type='int', dest='ystart', default=0, help='Start looking for a card edge at y position')
    parser.add_option('-Y', '--y-stop', type='int', dest='ystop', default=0, help='Stop looking for a card edge at y position')
    parser.add_option('-a', '--adjust-x', type='int', dest='xadjust', default=0, help='Adjust middle edge detect location (pixels)')
    (options, args) = parser.parse_args()
    
    for arg in args:
        image = Image.open(arg)
        card = PunchCard(image,  bright=options.bright, debug=options.display, xstart=options.xstart, xstop=options.xstop, ystart=options.ystart, ystop=options.ystop, xadjust=options.xadjust)
        print (card.text)
        if (options.dump):
            card.dump(arg)
        if (options.dumpraw):
            card.dump(arg, raw_data=True)