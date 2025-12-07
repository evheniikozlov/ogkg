from PIL import Image, ImageDraw

def find_convex_hull(points):
    if len(points) <= 2:
        return points

    def find_first_point():
        first_point = points[0]
        for point in points:
            if (point[0] < first_point[0]) or \
               (point[0] == first_point[0] and point[1] < first_point[1]):
                first_point = point
        return first_point

    def find_next_point(base_point):
        curr_point = None
        for p in points:
            if p != base_point:
                curr_point = p
                break
        
        if curr_point is None:
            return base_point

        curr_point_x_delta = curr_point[0] - base_point[0]
        curr_point_y_delta = curr_point[1] - base_point[1]
        
        for point in points:
            if point == base_point:
                continue

            point_x_delta = point[0] - base_point[0]
            point_y_delta = point[1] - base_point[1]

            val = point_y_delta * curr_point_x_delta - curr_point_y_delta * point_x_delta

            if val > 0:
                curr_point = point
                curr_point_x_delta = point_x_delta
                curr_point_y_delta = point_y_delta
            elif val == 0:
                dist_curr_sq = curr_point_x_delta**2 + curr_point_y_delta**2
                dist_new_sq = point_x_delta**2 + point_y_delta**2
                if dist_new_sq > dist_curr_sq:
                    curr_point = point
                    curr_point_x_delta = point_x_delta
                    curr_point_y_delta = point_y_delta
        
        return curr_point

    start_point = find_first_point()
    convex_hull = [start_point]
    current_point = start_point

    while True:
        next_point = find_next_point(current_point)
        if next_point == start_point:
            break 
        convex_hull.append(next_point)
        current_point = next_point
    
    return convex_hull

def get_pixels_coords(filename):
    pixel_coords = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                coordinates = line.split(" ")
                pixel_coords.append((int(coordinates[0]), int(coordinates[1])))
    return pixel_coords

def set_pixels(pixels, coordinates, color, height, width):
    for pixel_coord in coordinates:
        x = pixel_coord[0]
        y = height - pixel_coord[1]
        if 0 <= x < width and 0 <= y < height:
            pixels[x, y] = color

def draw_hull_lines(img, hull_points, color, width=3):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    
    draw_points = []
    for p in hull_points:
        draw_points.append((p[0], img_height - p[1]))
    
    if len(draw_points) > 0:
        draw_points.append(draw_points[0])
    
    draw.line(draw_points, fill=color, width=width, joint="curve")


if __name__ == "__main__":
    width = 960
    height = 540

    pixels_filename = "points.txt"
    image_filename = "lab_3.png"

    pixel_coords = get_pixels_coords(pixels_filename)

    convex_hull = find_convex_hull(pixel_coords)

    img = Image.new("RGB", (width, height), color="black")
    pixels = img.load()

    set_pixels(pixels, pixel_coords, (255, 255, 255), height, width)

    draw_hull_lines(img, convex_hull, (0, 0, 255), width=3)

    img.save(image_filename)
    print("Зображення створено!")