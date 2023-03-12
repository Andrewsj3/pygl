import numpy as np
from PIL import Image
from abc import ABCMeta, abstractmethod


class PyGlError(Exception):
    ...


class AbstractPyGlCanvas(metaclass=ABCMeta):
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @abstractmethod
    def from_png(cls, fpath):
        # Alternate constructor that allows you to create a canvas from an
        # existing PNG
        import os
        obj = object.__new__(cls)
        img = Image.open(os.path.expanduser(fpath))
        img.load()
        obj._pixels = np.array(img, dtype=np.uint8)
        obj._width, obj._height = img.size
        return obj

    @abstractmethod
    def set_pixel(self, colour: int, x: int, y: int):
        # Sets the pixel given by the x and y coordinates to a colour
        if -1 < x < self._width and -1 < y < self._height:
            self._pixels[y][x] = colour

    @abstractmethod
    def fill_colour(self, colour: int):
        # Fills the entire canvas with one colour
        self._pixels[:] = hex_to_rgb(colour)

    @abstractmethod
    def save_to_png(self, fpath: str):
        # Saves the current state of the canvas to the specified file path,
        # which does not necessarily need to exist
        img = Image.fromarray(self._pixels, self._mode)
        img.save(fpath)

    def flip_horiz(self):
        # Flips the canvas along the y axis
        self._pixels = np.fliplr(self._pixels)

    def flip_vert(self):
        # Flips the canvas along the x axis
        self._pixels = np.flipud(self._pixels)

    def right_90(self, rotations=1):
        # Warning: this modifies in-place
        self._pixels = np.rot90(self._pixels, rotations, (1, 0))

    def left_90(self, rotations=1):
        # Warning: this modifies in-place
        self._pixels = np.rot90(self._pixels, rotations)

    def fill_triangle(
            self,
            colour: int,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            x3: int,
            y3: int):
        if isinstance(self, PyGlCanvasRGB):
            colour = hex_to_rgb(colour)
        elif isinstance(self, PyGlCanvasRGBA):
            colour = hex_to_rgba(colour)
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
                self._line_horiz(colour, s1, s2, y)

        dx32 = x2 - x3
        dy32 = y2 - y3
        dx31 = x1 - x3
        dy31 = y1 - y3

        for y in range(y2 + offset, y3 + 1):
            if -1 < y < self._height:
                s1 = ((y - y3) * dx32 / dy32) + x3 if dy32 != 0 else x3
                s2 = ((y - y3) * dx31 / dy31) + x3 if dy31 != 0 else x3
                s1, s2 = map(int, sorted([s1, s2]))
                self._line_horiz(colour, s1, s2, y)

    def fill_circle(
            self,
            colour: int,
            cx: int,
            cy: int,
            radius: int):
        if isinstance(self, PyGlCanvasRGB):
            colour = hex_to_rgb(colour)
        elif isinstance(self, PyGlCanvasRGBA):
            colour = hex_to_rgba(colour)
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

    @abstractmethod
    def _line_horiz(self, colour, x1, x2, y):
        # Special case where the gradient is 0
        colour = hex_to_rgb(colour)
        # This allows us to fill a line with just one instruction
        self._pixels[y, x1:x2 + 1] = colour

    @abstractmethod
    def _line_vert(self, colour, y1, y2, x):
        # Special case where the gradient is infinite
        colour = hex_to_rgb(colour)
        y1, y2 = sorted((y1, y2))
        self._pixels[y1:y2 + 1, x] = colour

    def line(
            self,
            colour: int,
            x1: int,
            y1: int,
            x2: int,
            y2: int):
        if y1 == y2:
            self._line_horiz(colour, x1, x2, y1)
        if x1 == x2:
            self._line_vert(colour, y1, y2, x1)
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
        if isinstance(self, PyGlCanvasRGB):
            colour = hex_to_rgb(colour)
        elif isinstance(self, PyGlCanvasRGBA):
            colour = hex_to_rgba(colour)
        x1, x2 = sorted([x2, x1])
        y1, y2 = sorted([y2, y1])
        x1 = clamp(x1, 0, self._width - 1)
        x2 = clamp(x2, 0, self._width - 1)
        y2 = clamp(y2, 0, self._height - 1)
        y2 = clamp(y2, 0, self._height - 1)
        # Clamping parameters so we don't have to check for offscreen coords
        if x2 - x1 > y2 - y1:
            for y in range(y1, y2 + 1):
                self._line_horiz(colour, x1, x2, y)
                # Treating rectangles as many lines stacked on each other
        else:
            for x in range(x1, x2 + 1):
                self._line_vert(colour, y1, y2, x)


class PyGlCanvasRGB(AbstractPyGlCanvas):
    def __init__(self, width, height, fill_colour=None):
        super().__init__(width, height)
        self._pixels = np.empty((height, width, 3), dtype=np.uint8)
        self._fill_colour = fill_colour
        self._blending = False
        # Overrides previous pixel value by default
        self._blend_mode = "combine"
        # 'combine' does bitwise or between bytes, and 'blend'
        # averages the bytes
        self.fill_colour(fill_colour or 0x000000)

    @classmethod
    def from_png(cls, fpath):
        import os
        obj = object.__new__(cls)
        img = Image.open(os.path.expanduser(fpath)).convert("RGB")
        img.load()
        obj._pixels = np.array(img, dtype=np.uint8)
        obj._width, obj._height = img.size
        obj._blending = False
        obj._blend_mode = "combine"
        obj._fill_colour = None
        return obj

    @property
    def blending(self):
        return self._blending

    @blending.setter
    def blending(self, mode: bool):
        if mode in (True, False):
            self._blending = mode
        else:
            raise AttributeError(
                "Attribute `_blending` cannot be set manually,"
                " use `enable_blending` and `disable_blending` instead")

    def enable_blending(self):
        self._blending = True

    def disable_blending(self):
        self._blending = False

    def _line_horiz(self, colour: int, x1: int, x2: int, y: int):
        if self._blending:
            for x in range(x1, x2 + 1):
                # Unfortunately, horizontal/vertical lines can't be optimised
                # if blending calculations are needed
                self.set_pixel(colour, x, y)
        else:
            self._pixels[y, x1:x2 + 1] = colour

    def _line_vert(self, colour: int, y1: int, y2: int, x: int):
        if self._blending:
            for y in range(y1, y2 + 1):
                self.set_pixel(colour, x, y)
        else:
            self._pixels[y1:y2 + 1, x] = colour

    @property
    def blend_mode(self):
        return self._blend_mode

    @blend_mode.setter
    def blend_mode(self, mode: str):
        if mode not in ("combine", "blend"):
            raise PyGlError(
                f"Invalid option `{mode}`:"
                " must be `combine` or `blend`")
        else:
            self._blend_mode = mode

    def fill_colour(self, colour: int):
        self._pixels[:] = hex_to_rgb(colour)

    def set_pixel(
            self,
            colour: int,
            x: int,
            y: int):
        if -1 < x < self._width and -1 < y < self._height:
            # Bounds checking
            col_1 = self._pixels[y][x]
            if self._blending:
                self._pixels[y][x] = self.mix_cols(col_1, colour)
            else:
                self._pixels[y][x] = colour

    def save_to_png(self, fpath: str):
        import os
        dirname = os.path.dirname(fpath)
        if not os.path.exists(dirname) and fpath.count("/") != 0:
            if '~' in dirname:
                # Need to expand '~' if it exists, otherwise errors will occur
                dirname = os.path.expanduser(dirname)
                fpath = os.path.expanduser(fpath)
            os.makedirs(dirname, exist_ok=True)
        img = Image.fromarray(self._pixels, "RGB")
        img.save(fpath)

    def mix_cols(self, orig: np.array, new: np.array):
        r1, g1, b1 = orig
        r2, g2, b2 = new
        if self._fill_colour is not None:
            r3, g3, b3 = hex_to_rgb(self._fill_colour)
            if r1 == r3 and g1 == g3 and b1 == b3 and self._blending:
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


class PyGlCanvasRGBA(AbstractPyGlCanvas):
    def __init__(self, width, height, fill_colour=None):
        super().__init__(width, height)
        self._pixels = np.empty((height, width, 4), dtype=np.uint8)
        self._fill_colour = fill_colour
        self._bg_blending = False
        if fill_colour is None:
            self.fill_colour(0x000000FF)
        else:
            self.fill_colour(fill_colour)

    @classmethod
    def from_png(cls, fpath):
        import os
        obj = cls.__new__(cls)
        img = Image.open(os.path.expanduser(fpath)).convert("RGBA")
        img.load()
        obj._pixels = np.array(img, dtype=np.uint8)
        obj._width, obj._height = img.size
        obj._fill_colour = None
        return obj

    def save_to_png(self, fpath: str):
        import os
        dirname = os.path.dirname(fpath)
        if not os.path.exists(dirname) and fpath.count("/") != 0:
            if '~' in dirname:
                dirname = os.path.expanduser(dirname)
                fpath = os.path.expanduser(fpath)
            os.makedirs(dirname, exist_ok=True)
        img = Image.fromarray(self._pixels, "RGBA")
        img.save(fpath)

    def fill_colour(self, colour: int):
        self._pixels[:] = hex_to_rgba(colour)

    def set_pixel(
            self,
            colour: int,
            x: int,
            y: int):
        if -1 < x < self._width and -1 < y < self._height:
            # Bounds checking
            col_1 = self._pixels[y][x]
            self._pixels[y][x] = self.mix_cols(col_1, colour)

    def mix_cols(self, orig: np.array, new: np.array):
        r1, g1, b1, a1 = orig
        r2, g2, b2, a2 = new
        if self._fill_colour is not None:
            r3, g3, b3, a3 = hex_to_rgba(self._fill_colour)
            if r1 == r3 and g1 == g3 and b1 == b3 and not self._bg_blending:
                return [r2, g2, b2, 255]
        r1 = (r1 * (255 - a2) + r2 * a2) / 255
        g1 = (g1 * (255 - a2) + g2 * a2) / 255
        b1 = (b1 * (255 - a2) + b2 * a2) / 255
        r1, g1, b1, a1 = map(int, [r1, g1, b1, a1])
        return [r1, g1, b1, a1]

    def _line_horiz(self, colour: int, x1: int, x2: int, y: int):
        for x in range(x1, x2 + 1):
            self.set_pixel(colour, x, y)

    def _line_vert(self, colour: int, y1: int, y2: int, x: int):
        for y in range(y1, y2 + 1):
            self.set_pixel(colour, x, y)

    @property
    def blending(self):
        return self._bg_blending

    @blending.setter
    def blending(self, b):
        raise AttributeError(
            "Attribute `_bg_blending` cannot be set manually,"
            " use `enable_blending` and `disable_blending` instead")

    def enable_blending(self):
        self._bg_blending = True

    def disable_blending(self):
        self._bg_blending = False


class PyGlCanvasGS(AbstractPyGlCanvas):
    def __init__(self, width, height, fill_colour=None):
        super().__init__(width, height)
        self._pixels = np.empty((height, width), dtype=np.uint8)
        self.fill_colour(fill_colour or 0x00)

    def save_to_png(self, fpath: str):
        import os
        dirname = os.path.dirname(fpath)
        if not os.path.exists(dirname) and fpath.count("/") != 0:
            if '~' in dirname:
                dirname = os.path.expanduser(dirname)
                fpath = os.path.expanduser(fpath)
            os.makedirs(dirname, exist_ok=True)
        img = Image.fromarray(self._pixels)
        img.save(fpath)

    @classmethod
    def from_png(cls, fpath):
        import os
        obj = cls.__new__(cls)
        img = Image.open(os.path.expanduser(fpath))
        img.load()
        obj._pixels = np.array(img, dtype=np.uint8)
        obj._width, obj._height = img.size
        return obj

    def set_pixel(self, colour: int, x: int, y: int):
        if -1 < x < self._width and -1 < y < self._height:
            self._pixels[y][x] = colour

    def _line_horiz(self, colour: int, x1: int, x2: int, y: int):
        y = clamp(y, 0, self._height - 1)
        x1 = clamp(x1, 0, self._width - 1)
        x2 = clamp(x2, 0, self._width - 1)
        x1, x2 = sorted([x1, x2])
        self._pixels[y, x1:x2 + 1] = colour

    def _line_vert(self, colour: int, y1: int, y2: int, x: int):
        x = clamp(x, 0, self._width - 1)
        y1 = clamp(y1, 0, self._height - 1)
        y2 = clamp(y2, 0, self._height - 1)
        y1, y2 = sorted([y1, y2])
        self._pixels[y1:y2 + 1, x] = colour

    def fill_colour(self, colour: int):
        self._pixels[:] = colour


def hex_to_rgb(col: int | str):
    from sys import byteorder
    if isinstance(col, str):
        try:
            col = int(col.replace("#", ""), base=16)
        except ValueError:
            raise PyGlError(f"String {col} is not a valid hex code")

    col_as_bytes = [(col >> (8 * 0)) & 0xFF,
                    (col >> (8 * 1)) & 0xFF,
                    (col >> (8 * 2)) & 0xFF]

    if byteorder == "little":
        # order needs to be reversed for little-endian machines
        col_as_bytes = col_as_bytes[::-1]
    return col_as_bytes


def hex_to_rgba(col: int | str):
    from sys import byteorder
    if isinstance(col, str):
        try:
            col = int(col.replace("#", ""), base=16)
        except ValueError:
            raise PyGlError(f"String {col} is not a valid hex code")

    col_as_bytes = [(col >> (8 * 0)) & 0xFF,
                    (col >> (8 * 1)) & 0xFF,
                    (col >> (8 * 2)) & 0xFF,
                    (col >> (8 * 3)) & 0xFF]
    if byteorder == "little":
        col_as_bytes = col_as_bytes[::-1]
    return col_as_bytes


def clamp(num: int, low: int, high: int):
    return min(max(num, low), high)
