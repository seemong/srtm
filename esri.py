from __future__ import print_function
import fileinput
import sys

class Esri(object):
    """Represents an ESRI ASCII file"""

    @classmethod
    def _read_esri_header(cls, line, key):
        split = line.split()
        assert split[0] == key
        print(split)
        return split[1]

    def __init__(self, filename):
        self.file = open(filename)

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

        self.data_start = self.file.ftell()

    def __str__(self):
        return 'ncols=' + str(self.ncols) + ', nrows=' + str(self.nrows)


if __name__ == '__main__':
    esri = Esri(sys.argv[1])
    print(esri)
