import numpy as np
from PIL import Image


class PyGlCanvas:
    def __init__(self, width, height, fill_colour=None):
        self._width = width
        self._height = height
        self._pixels = np.empty(width * height * 3, dtype=int)
        self._pixels = self._pixels.reshape((width * height, 3))
        self.fill_colour(fill_colour or 0)

    def fill_colour(self, colour: int):
        self._pixels[:] = hex_to_rgb(colour)

    def _line_low(
            self,
            colour: int,
            x1: int,
            y1: int,
            x2: int,
            y2: int):
        # For lines with a gradient between 1 and -1
        dx = x2 - x1
        dy = y2 - y1
        yi = 1
        if dy < 0:
            yi = -1
            dy *= -1
        diff = (2 * dy) - dx
        y = y1

        for x in range(x1, x2 + 1):
            self.set_pixel(colour, x, y)
            if diff > 0:
                y += yi
                diff += (2 * (dy - dx))
            else:
                diff += 2 * dy

    def _line_high(
            self,
            colour: int,
            x1: int,
            y1: int,
            x2: int,
            y2: int):
        # For lines with a gradient > 1 or < -1
        dx = x2 - x1
        dy = y2 - y1
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        diff = (2 * dx) - dy
        x = x1
        for y in range(y1, y2 + 1):
            self.set_pixel(colour, x, y)
            if diff > 0:
                x += xi
                diff += (2 * (dx - dy))
            else:
                diff += 2 * dx

    def line(
            self,
            colour: int,
            x1: int,
            y1: int,
            x2: int,
            y2: int):
        if abs(y2 - y1) < abs(x2 - x1):
            if x1 > x2:
                self._line_low(colour, x2, y2, x1, y1)
            else:
                self._line_low(colour, x1, y1, x2, y2)
        else:
            if y1 > y2:
                self._line_high(colour, x2, y2, x1, y1)
            else:
                self._line_high(colour, x1, y1, x2, y2)

    def fill_rect(
            self,
            colour: int,
            x1: int,
            y1: int,
            x2: int,
            y2: int):
        x1, x2 = sorted([x2, x1])
        y1, y2 = sorted([y2, y1])
        for y in range(y1, y2 + 1):
            self.line(colour, x1, y, x2, y)
            # Treating rectangles as many lines stacked on each other

    def set_pixel(
            self,
            colour: int,
            x: int,
            y: int):
        if -1 < x < self._width and -1 < y < self._height:
            # Bounds checking
            self._pixels[y * self._width + x] = hex_to_rgb(colour)
            # Converting 2D coordinates to 1D coordinates
        return None

    def fill_triangle(
            self,
            colour: int,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            x3: int,
            y3: int):
        (x1, y1), (x2, y2), (x3, y3) = sorted(
            [(x1, y1), (x2, y2), (x3, y3)], key=lambda point: point[1])
        # Sorting points by y, with highest point being y1
        dx12 = x2 - x1
        dy12 = y2 - y1

        dx13 = x3 - x1
        dy13 = y3 - y1

        for y in range(y1, y2 + 1):
            if -1 < y < self._height:
                s1 = ((y - y1) * dx12 / dy12) + x1 if dy12 != 0 else x1
                s2 = ((y - y1) * dx13 / dy13) + x1 if dy13 != 0 else x1
                s1, s2 = map(int, sorted([s1, s2]))
                for x in range(s1, s2 + 1):
                    self.set_pixel(colour, x, y)

        dx32 = x2 - x3
        dy32 = y2 - y3
        dx31 = x1 - x3
        dy31 = y1 - y3

        for y in range(y2, y3 + 1):
            if -1 < y < self._height:
                s1 = ((y - y3) * dx32 / dy32) + x3 if dy32 != 0 else x3
                s2 = ((y - y3) * dx31 / dy31) + x3 if dy31 != 0 else x3
                s1, s2 = map(int, sorted([s1, s2]))
                for x in range(s1, s2 + 1):
                    self.set_pixel(colour, x, y)

    def fill_circle(
            self,
            colour: int,
            cx: int,
            cy: int,
            radius: int):
        x1 = cx - radius
        x2 = cx + radius
        y1 = cy - radius
        y2 = cy + radius
        for y in range(y1, y2 + 1):
            if -1 < y < self._width:
                for x in range(x1, x2 + 1):
                    if -1 < x < self._width:
                        dx = x - cx
                        dy = y - cy
                        if dx * dx + dy * dy < radius * radius:
                            self.set_pixel(colour, x, y)

    def save_to_ppm(self, fpath: str):
        with open(fpath, 'w') as f:
            f.write(f"P3\n{self._width} {self._height} 255\n")
            # PPM header specification
            for i in range(len(self._pixels)):
                col_as_bytes = [
                    (self._pixels[i] >> (8 * 0)),
                    (self._pixels[i] >> (8 * 1)),
                    (self._pixels[i] >> (8 * 2))
                ]
                # extracts the blue, green and red components from the colour
                f.write(
                    " ".join([str(i) for i in col_as_bytes]) + " ")

    def save_to_png(self, fpath: str):
        img = Image.fromarray(
            self._pixels.reshape(self._height,self._width,3).astype(
                np.uint8)).convert("RGB")
        img.save(fpath)


def hex_to_rgb(col: int):
    col_as_bytes = [(col >> (8 * 0)) & 0xFF,
                    (col >> (8 * 1)) & 0xFF,
                    (col >> (8 * 2)) & 0xFF]
    return col_as_bytes
