import pygl


def lines_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0
    BG_COL = 0xFF0000
    file_path = "images/lines.png"
    pixels = pygl.PyGlCanvasRGB(WIDTH, HEIGHT, BG_COL)
    pixels.line(FG_COL, 130, 150, 130, 450)
    pixels.line(FG_COL, 130, 450, 190, 450)
    pixels.line(FG_COL, 250, 450, 310, 450)
    pixels.line(FG_COL, 250, 150, 310, 150)
    pixels.line(FG_COL, 280, 150, 280, 450)
    pixels.line(FG_COL, 370, 150, 370, 450)
    pixels.line(FG_COL, 370, 150, 430, 450)
    pixels.line(FG_COL, 430, 150, 430, 450)
    pixels.line(FG_COL, 490, 150, 490, 450)
    pixels.line(FG_COL, 490, 150, 550, 150)
    pixels.line(FG_COL, 490, 300, 550, 300)
    pixels.line(FG_COL, 490, 450, 550, 450)
    pixels.line(FG_COL, 610, 150, 670, 150)
    pixels.line(FG_COL, 610, 150, 670, 450)
    pixels.line(FG_COL, 610, 450, 670, 450)
    pixels.save_to_png(file_path)


def rect_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0
    BG_COL = 0xFF0000
    file_path = "images/rect.png"
    pixels = pygl.PyGlCanvasRGB(WIDTH, HEIGHT, BG_COL)
    pixels.fill_rect(FG_COL, 100, 100, 410, 330)
    pixels.save_to_png(file_path)


def triangle_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0
    BG_COL = 0xFF0000
    file_path = "images/triangle.png"
    pixels = pygl.PyGlCanvasRGB(WIDTH, HEIGHT, BG_COL)
    pixels.fill_triangle(FG_COL, 400, 50, 160, 380, 600, 460)
    pixels.save_to_png(file_path)


def circle_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0
    BG_COL = 0xFF0000
    file_path = "images/circle.png"
    pixels = pygl.PyGlCanvasRGB(WIDTH, HEIGHT, BG_COL)
    pixels.fill_circle(FG_COL, 400, 300, 100)
    pixels.save_to_png(file_path)


def combined_example():
    WIDTH = 800
    HEIGHT = 600
    BG_COL = 0xFF0000
    FG_COL = 0x000000
    file_path = "images/combined.png"
    pixels = pygl.PyGlCanvasRGB(WIDTH, HEIGHT, BG_COL)
    pixels.fill_triangle(FG_COL, 10, 400, 190, 400, 100, 200)
    pixels.fill_triangle(BG_COL, 60, 370, 140, 370, 100, 270)
    pixels.fill_rect(FG_COL, 360, 200, 560, 400)
    pixels.fill_triangle(BG_COL, 390, 200, 530, 200, 460, 270)
    pixels.fill_triangle(BG_COL, 390, 400, 530, 400, 460, 330)
    pixels.fill_triangle(BG_COL, 360, 230, 360, 370, 430, 300)
    pixels.fill_triangle(BG_COL, 560, 230, 560, 370, 490, 300)
    pixels.fill_circle(FG_COL, 270, 300, 100)
    pixels.fill_circle(BG_COL, 270, 300, 50)
    pixels.fill_rect(FG_COL, 585, 200, 785, 400)
    pixels.fill_rect(BG_COL, 615, 230, 755, 370)
    pixels.save_to_png(file_path)


def transparent_example():
    WIDTH = 800
    HEIGHT = 600
    BG_COL = 0xFFFFFF
    pixels = pygl.PyGlCanvasRGB(WIDTH, HEIGHT, BG_COL)
    pixels.enable_blending()
    pixels.fill_circle(0x0000FF, 400, 250, 100)
    pixels.fill_circle(0xFF0000, 350, 340, 100)
    pixels.fill_circle(0x00FF00, 450, 340, 100)
    file_path = "images/transparent.png"
    pixels.save_to_png(file_path)

def checkers_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0xFF
    STRIDE = 40
    offset = STRIDE
    pixels = pygl.PyGlCanvasGS(WIDTH, HEIGHT)
    for y in range(0, HEIGHT, STRIDE):
        offset = 0 if offset == STRIDE else STRIDE
        for x in range(offset, WIDTH, STRIDE * 2):
            pixels.fill_rect(FG_COL, x, y, x+39, y+39)
    pixels.save_to_png("images/checkers.png")


def main():
    #lines_example()
    #triangle_example()
    #rect_example()
    #circle_example()
    #combined_example()
    #transparent_example()
    checkers_example()


if __name__ == "__main__":
    main()
