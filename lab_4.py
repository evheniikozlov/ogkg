import math
import random
from PIL import Image, ImageDraw

WIDTH = 960
HEIGHT = 540
BG_COLOR = (255, 255, 255)
CENTROID_RADIUS = 2
POINTS_FILENAME = "points.txt"
OUTPUT_FILENAME = "lab_4.png"

def get_pixels_coords(filename):
    pixel_coords = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                coordinates = line.split()
                pixel_coords.append((int(coordinates[0]), int(coordinates[1])))
    return pixel_coords

def transform_coords_to_image(coords, height):
    img_coords = []
    for x, y in coords:
        img_coords.append((x, height - y))
    return img_coords

def find_connected_components(points):
    points_set = set(points)
    clusters = []
    
    while points_set:
        start_node = points_set.pop()
        current_cluster = [start_node]
        queue = [start_node]
        
        while queue:
            x, y = queue.pop(0)
            
            neighbors = [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1),
                (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)
            ]
            
            for nx, ny in neighbors:
                if (nx, ny) in points_set:
                    points_set.remove((nx, ny))
                    current_cluster.append((nx, ny))
                    queue.append((nx, ny))
        
        clusters.append(current_cluster)
    
    return clusters

def calculate_centroids(clusters):
    centroids = []
    for cluster in clusters:
        sum_x = sum(p[0] for p in cluster)
        sum_y = sum(p[1] for p in cluster)
        n = len(cluster)
        centroids.append((sum_x / n, sum_y / n))
    return centroids

def generate_voronoi_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        colors.append((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
    return colors

def draw_voronoi_diagram(img, centroids):
    pixels = img.load()
    colors = generate_voronoi_colors(len(centroids))
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            min_dist = float('inf')
            closest_idx = -1
            
            for idx, (cx, cy) in enumerate(centroids):
                dist = (x - cx)**2 + (y - cy)**2
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = idx
            
            if closest_idx != -1:
                pixels[x, y] = colors[closest_idx]

def main():
    print("1. Зчитування датасету...")
    raw_coords = get_pixels_coords(POINTS_FILENAME)
    
    img_coords = transform_coords_to_image(raw_coords, HEIGHT)
    
    print(f"Завантажено {len(img_coords)} точок.")

    print("2. Пошук зв'язаних областей...")
    clusters = find_connected_components(img_coords)
    print(f"Знайдено {len(clusters)} зв'язаних областей.")

    print("3. Обчислення центрів ваги...")
    centroids = calculate_centroids(clusters)

    image = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(image, "RGBA")

    print("4. Побудова діаграми Вороного...")
    draw_voronoi_diagram(image, centroids)

    print("5. Відображення точок датасету (насиченість 10%)...")
    point_color = (0, 0, 0, 25) 
    
    draw.point(img_coords, fill=point_color)

    print("6. Відображення центрів ваги...")
    centroid_color = (255, 0, 0, 255)
    centroid_border = (255, 255, 255, 255)
    
    for cx, cy in centroids:
        x0, y0 = cx - CENTROID_RADIUS, cy - CENTROID_RADIUS
        x1, y1 = cx + CENTROID_RADIUS, cy + CENTROID_RADIUS
        draw.ellipse([x0, y0, x1, y1], fill=centroid_color, outline=centroid_border)

    print(f"7. Збереження результату у {OUTPUT_FILENAME}...")
    image.save(OUTPUT_FILENAME)
    print("Готово!")

if __name__ == "__main__":
    main()