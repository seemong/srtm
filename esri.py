from __future__ import print_function
import fileinput
import sys
import math
import os

class Esri(object):
    """Represents an ESRI ASCII file"""

    @classmethod
    def _read_esri_header(cls, line, key):
        split = line.split()
        assert split[0] == key
        print(split)
        return split[1]

    def __init__(self, filename):
        self.file = open(filename, 'r')

        line = self.file.readline()
        self.ncols = int(Esri._read_esri_header(line, 'ncols'))

        line = self.file.readline()
        self.nrows = int(Esri._read_esri_header(line, 'nrows'))

        line = self.file.readline()
        self.xllcorner = float(Esri._read_esri_header(line, 'xllcorner'))

        line = self.file.readline()
        self.yllcorner =  float(Esri._read_esri_header(line, 'yllcorner'))

        line = self.file.readline()
        self.cellsize = float(Esri._read_esri_header(line, 'cellsize'))

        line = self.file.readline()
        self.NODATA_value = float(Esri._read_esri_header(line, 'NODATA_value'))

        self.data_start = self.file.tell()

    def __str__(self):
        return 'ncols=' + str(self.ncols) + ', nrows=' + str(self.nrows)

    def xurcorner(self):
        """x upper right corner"""
        return self.xllcorner + (self.ncols - 1) * self.cellsize

    def yurcorner(self):
        """y upper right corner"""
        return self.yllcorner + (self.nrows - 1) * self.cellsize

    def get_row_index(self, y):
        return self.nrows - int((y - self.yllcorner) / self.cellsize)

    def get_col_index(self, x):
        return int((x - self.xllcorner) / self.cellsize)

    def filter(self, left, bottom, right, top):
        startrow = self.get_row_index(top)
        endrow = self.get_row_index(bottom)
        startcol = self.get_col_index(left)
        endcol = self.get_col_index(right)

        print('ncols         ' + str(endcol - startcol + 1))
        print('nrows         ' + str(endrow - startrow + 1))
        print('xllcorner     ' + str(left))
        print('yllcorner     ' + str(bottom))
        print('cellsize      ' + str(self.cellsize))
        print('NODATA_value  ' + '-9999')

        # start at beginning of data
        self.file.seek(self.data_start, os.SEEK_SET)

        # skip to the correct row
        for i in range(0, startrow):
            self.file.readline()             # throw data away

        # read data from the correct rows
        for row in range(startrow, endrow+1):
            line = self.file.readline()

            split = line.split()
            for col in range(startcol, endcol + 1):
                print(split[col], end=' ')
            print("")

if __name__ == '__main__':
    esri = Esri(sys.argv[1])
    esri.filter(-121.90, 46.75, -121.56, 46.96)
