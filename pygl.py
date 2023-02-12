import numpy as np
from PIL import Image


class PyGlError(Exception):
    ...


class PyGlCanvas:
    # TODO: Split this into separate classes for rgb, rgba, grayscale
    def __init__(self, width, height, fill_colour=None, mode="RGB"):
        self._width = width
        self._height = height
        self._mode = mode
        self._pixels = np.empty(width * height * len(mode), dtype=np.uint8)
        self._pixels = self._pixels.reshape((width * height, len(mode)))
        self._fill_colour = fill_colour
        self._blending = False
        # Decides whether to blend with the background for rgba
        # but does not work the same with rgb
        self._blend_mode = "combine"
        # 'combine' does bitwise or between bytes, and 'blend'
        # averages the bytes
        if fill_colour is None:
            self.fill_colour(0x000000FF)
        else:
            self.fill_colour(fill_colour)

    @property
    def blending(self):
        return self._blending

    @blending.setter
    def blending(self, b):
        raise AttributeError(
            "Attribute `_blending` cannot be set manually,"
            " use `enable_blending` and `disable_blending` instead")

    def enable_blending(self):
        self._blending = True

    def disable_blending(self):
        self._blending = False

    @property
    def blend_mode(self):
        return self._blend_mode

    @blend_mode.setter
    def blend_mode(self, mode):
        if mode not in ("combine", "blend"):
            raise PyGlError(
                f"Invalid option `{mode}`:"
                " must be `combine` or `blend`")

    def fill_colour(self, colour: int):
        self._pixels[:] = self.hex_to_rgb(colour)

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
            col_1 = self._pixels[y * self._width + x]
            col_2 = self.hex_to_rgb(colour)
            if self._mode == "RGBA":
                self._pixels[y * self._width +
                             x] = self.mix_cols_rgba(col_1, col_2)
            else:
                if not self._blending:
                    self._pixels[y * self._width +
                                 x] = self.mix_cols_rgb(col_1, col_2)
                else:
                    self._pixels[y * self._width + x] = self.hex_to_rgb(colour)
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
        offset = 0
        if y3 == y2:
            offset += 1
        for y in range(y1, y2 + offset):
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

        for y in range(y2 + offset, y3 + 1):
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

    def save_to_png(self, fpath: str):
        img = Image.fromarray(
            self._pixels.reshape(
                self._height, self._width, len(
                    self._mode)), self._mode)

        img.save(fpath)

    def hex_to_rgb(self, col: int):
        from sys import byteorder
        if self._mode == "RGB":
            col_as_bytes = [(col >> (8 * 0)) & 0xFF,
                            (col >> (8 * 1)) & 0xFF,
                            (col >> (8 * 2)) & 0xFF]
            if byteorder == "little":
                # why does endianness even exist

                col_as_bytes = col_as_bytes[::-1]
        elif self._mode == "RGBA":
            col_as_bytes = [(col >> (8 * 0)) & 0xFF,
                            (col >> (8 * 1)) & 0xFF,
                            (col >> (8 * 2)) & 0xFF,
                            (col >> (8 * 3)) & 0xFF]
            if byteorder == "little":
                col_as_bytes = col_as_bytes[::-1]
        return col_as_bytes

    def mix_cols_rgb(self, orig: np.array, new: np.array):
        r1, g1, b1 = orig
        r2, g2, b2 = new
        r3, g3, b3 = self.hex_to_rgb(self._fill_colour)
        if r1 == r3 and g1 == g3 and b1 == b3 and not self._blending:
            return [r2, g2, b2]
        if self._blend_mode == "blend":
            r1 = (r1 + r2) / 2
            g1 = (g1 + g2) / 2
            b1 = (b1 + b2) / 2
            r1 = min(r1, 255)
            g1 = min(g1, 255)
            b1 = min(b1, 255)
        elif self._blend_mode == "combine":
            r1 |= r2
            g1 |= g2
            b1 |= b2
        return [r1, g1, b1]

    def mix_cols_rgba(self, orig: np.array, new: np.array):
        r1, g1, b1, a1 = orig
        r2, g2, b2, a2 = new
        r3, g3, b3, a3 = self.hex_to_rgb(self._fill_colour)
        if r1 == r3 and g1 == g3 and b1 == b3 and not self._blending:
            return [r2, g2, b2, 255]
        r1 = (r1 * (255 - a2) + r2 * a2) / 255
        r1 = min(r1, 255)
        g1 = (g1 * (255 - a2) + g2 * a2) / 255
        g1 = min(g1, 255)
        b1 = (b1 * (255 - a2) + b2 * a2) / 255
        b1 = min(b1, 255)
        r1, g1, b1, a1 = map(int, [r1, g1, b1, a1])
        return [r1, g1, b1, a1]
