from PIL import Image

def get_pixels_coords(filename):
    pixel_coords = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        
        for line in lines:
            line = line.strip()
            coordinates = line.split(" ")

            pixel_coords.append((int(coordinates[0]), int(coordinates[1])))
    
    return pixel_coords

def create_image(width, height, pixel_coords):
    img = Image.new('1', (width, height), color="black")
    pixels = img.load()

    for pixel_coord in pixel_coords:
        pixels[pixel_coord[0], height - pixel_coord[1]] = 1
    
    return img


if __name__ == "__main__":
    width = 960
    height = 540

    pixels_filename = "points.txt"
    image_filename = "lab_2.png"

    pixel_coords = get_pixels_coords(pixels_filename)
    img = create_image(width, height, pixel_coords)

    img.save(image_filename)
    print("Зображення створено!")