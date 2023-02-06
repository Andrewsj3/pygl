import pygl

def lines_example():
    WIDTH = 80
    HEIGHT = 60
    FG_COL = 0xFF000000
    BG_COL = 0xFF0000FF
    file_path = "images/lines.ppm"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT)
    pixels.fill(BG_COL)
    pixels.line(FG_COL, 13, 15, 13, 45)
    pixels.line(FG_COL, 13, 45, 19, 45)
    pixels.line(FG_COL, 25, 45, 31, 45)
    pixels.line(FG_COL, 25, 15, 31, 15)
    pixels.line(FG_COL, 28, 15, 28, 45)
    pixels.line(FG_COL, 37, 15, 37, 45)
    pixels.line(FG_COL, 37, 15, 43, 45)
    pixels.line(FG_COL, 43, 15, 43, 45)
    pixels.line(FG_COL, 49, 15, 49, 45)
    pixels.line(FG_COL, 49, 15, 55, 15)
    pixels.line(FG_COL, 49, 30, 55, 30)
    pixels.line(FG_COL, 49, 45, 55, 45)
    pixels.line(FG_COL, 61, 15, 67, 15)
    pixels.line(FG_COL, 61, 15, 67, 45)
    pixels.line(FG_COL, 61, 45, 67, 45)   
    pixels.save_to_ppm(file_path)


def rect_example():
    WIDTH = 80
    HEIGHT = 60
    FG_COL = 0xFF000000
    BG_COL = 0xFF0000FF
    file_path = "images/rect.ppm"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT)
    pixels.fill(BG_COL)
    pixels.fill_rect(FG_COL, 5, 5, 15, 15)
    pixels.save_to_ppm(file_path)


def triangle_example():
    WIDTH = 80
    HEIGHT = 60
    FG_COL = 0xFF000000
    BG_COL = 0xFF0000FF
    file_path = "images/triangle.ppm"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT)
    pixels.fill(BG_COL)
    pixels.fill_triangle(FG_COL, 40, 5, 16, 38, 60, 46)
    pixels.save_to_ppm(file_path)


def circle_example():
    WIDTH = 80
    HEIGHT = 60
    FG_COL = 0xFF000000
    BG_COL = 0xFF0000FF
    file_path = "images/circle.ppm"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT)
    pixels.fill(BG_COL)
    pixels.fill_circle(FG_COL, 20, 20, 10)
    pixels.save_to_ppm(file_path)
    

def combined_example():
    WIDTH = 96
    HEIGHT = 60
    BG_COL = 0xFF000000
    FG_COL = 0xFFFFFFFF
    file_path = "images/combined.ppm"
    pixels = pygl.PyGlCanvas(WIDTH, HEIGHT)
    pixels.fill(BG_COL)
    pixels.fill_triangle(FG_COL, 3, 40, 21, 40, 12, 20)
    pixels.fill_triangle(BG_COL, 8, 37, 16, 37, 12, 25)
    pixels.fill_circle(FG_COL, 32, 30, 10)
    pixels.fill_circle(BG_COL, 32, 30, 5)
    pixels.fill_rect(FG_COL, 47, 20, 67, 40)
    pixels.fill_triangle(BG_COL, 50, 20, 64, 20, 57, 27)
    pixels.fill_triangle(BG_COL, 50, 40, 64, 40, 57, 33)
    pixels.fill_triangle(BG_COL, 47, 23, 47, 37, 54, 30)
    pixels.fill_triangle(BG_COL, 67, 23, 67, 37, 60, 30)
    pixels.fill_rect(FG_COL, 72, 20, 92, 40)
    pixels.fill_rect(BG_COL, 75, 23, 89, 37)
    pixels.save_to_ppm(file_path)


def main():
    lines_example()
    triangle_example()
    rect_example()
    circle_example()
    combined_example()


if __name__ == "__main__":
    main()
