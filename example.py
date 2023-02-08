import pygl

def lines_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0
    BG_COL = 0xFF
    file_path = "images/lines.png"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT, BG_COL)
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
    BG_COL = 0xFF
    file_path = "images/rect.png"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT, BG_COL)
    pixels.fill_rect(FG_COL, 100, 100, 410, 330)
    pixels.save_to_png(file_path)


def triangle_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0
    BG_COL = 0xFF
    file_path = "images/triangle.png"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT, BG_COL)
    pixels.fill_triangle(FG_COL, 400, 50, 160, 380, 600, 460)
    pixels.save_to_png(file_path)


def circle_example():
    WIDTH = 800
    HEIGHT = 600
    FG_COL = 0
    BG_COL = 0xFF
    file_path = "images/circle.png"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT, BG_COL)
    pixels.fill_circle(FG_COL, 300, 300, 100)
    pixels.save_to_png(file_path)
    

def combined_example():
    WIDTH = 960
    HEIGHT = 600
    BG_COL = 0xFF
    FG_COL = 0
    file_path = "images/combined.png"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT, BG_COL)
    pixels.fill_triangle(FG_COL, 30, 400, 210, 400, 120, 200)
    pixels.fill_triangle(BG_COL, 80, 370, 160, 370, 120, 270)
    pixels.fill_circle(FG_COL, 320, 300, 100)
    pixels.fill_circle(BG_COL, 320, 300, 50)
    pixels.fill_rect(FG_COL, 470, 200, 670, 400)
    pixels.fill_triangle(BG_COL, 500, 200, 640, 200, 570, 270)
    pixels.fill_triangle(BG_COL, 500, 400, 640, 400, 570, 330)
    pixels.fill_triangle(BG_COL, 470, 230, 470, 370, 540, 300)
    pixels.fill_triangle(BG_COL, 670, 230, 670, 370, 600, 300)
    pixels.fill_rect(FG_COL, 720, 200, 920, 400)
    pixels.fill_rect(BG_COL, 750, 230, 890, 370)
    pixels.save_to_png(file_path)


def main():
    lines_example()
    triangle_example()
    rect_example()
    circle_example()
    combined_example()


if __name__ == "__main__":
    main()
