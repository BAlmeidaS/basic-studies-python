"""A module for dealing with BMP bitmap image files."""

import math

def write_grayscale(filename, pixels):
    """Creates and writes a grayscale BMP file.

    Args:
        filename: The name of the BMP file to me created.

        pixels: A rectangular image store as a sequence of rows.
            Each row must be an iterable series of integers in the
            range 0-255

    Raises:
        OSError: If the file couldn't be written.
    """

    height = len(pixels)
    width = len(pixels[0])

    with open(filename, 'wb') as bmp:
        # BMP HEADER
        bmp.write(b'BM')

        size_bookmark = bmp.tell()  #the next four bytes hold the filesize as a 32bits. This method give us the offset of the beggining so far.

        bmp.write(b'\x00\x00\x00\x00')

        bmp.write(b'\x00\x00')
        bmp.write(b'\x00\x00')

        pixel_offset_bookmark = bmp.tell()
        bmp.write(b'\x00\x00\x00\x00')

        # Image Header
        bmp.write(b'\x28\x00\x00\x00')
        bmp.write(_int32_to_bytes(width))
        bmp.write(_int32_to_bytes(height))
        bmp.write(b'\x01\x00')
        bmp.write(b'\x08\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')

        # Color palette - a linear grayscale
        for c in range(256):
            bmp.write(bytes((c,c,c,0))) # Blue, Green, Red, Zero

        # Pixel data
        pixel_data_bookmark = bmp.tell()
        for row in reversed(pixels):
            row_data = bytes(row)
            bmp.write(row_data)
            padding = b'\x00' * (4 - (len(row) % 4)) #Pad row to multiple of four bytes
            bmp.write(padding)

        # End of file
        eof_bookmark = bmp.tell()

        # Fill in file size placeholder
        bmp.seek(size_bookmark)
        bmp.write(_int32_to_bytes(eof_bookmark))

        # Fill in pixel offeset placeholder
        bmp.seek(pixel_offset_bookmark)
        bmp.write(_int32_to_bytes(pixel_data_bookmark))


def dimensions(filename):
    with open(filename, 'rb') as f:
        magic = f.read(2)
        if magic != b'BM':
            raise ValueError("{} is not a BML file".format(filename))

        f.seek(18)
        width_bytes = f.read(4)
        height_bytes = f.read(4)

        return (_bytes_to_int32(width_bytes),
                _bytes_to_int32(height_bytes))

def cc():
    return "boa"

def _bytes_to_int32(b):
    return b[0] | (b[1] << 8) | (b[2] << 16) | (b[3] << 24)

 
def _int32_to_bytes(i):
    """Convert an integer to four bytes in little-endian format."""
    return bytes((i & 0xff,
                  i >> 8 & 0xff,
                  i >> 16 & 0xff,
                  i >> 24 & 0xff))


def mandel(real, imag):
    x = 0
    y = 0
    for i in range (1, 257):
        if x * x + y * y > 4.0:
            break
        xt = real + x * x - y * y
        y = imag + 2.0 * x * y
        x = xt
    return int(math.log(i) * 256 / math.log(256)) - 1


def mandelbrot(size_x, size_y):
    return [[mandel((3.5 * x / size_x) - 2.5,
                    (2.0 * y / size_y) - 1.0)
             for x in range(size_x)]
            for y in range(size_y)]


