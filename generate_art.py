from PIL import Image, ImageDraw, ImageChops
import random
import colorsys


def randomize_color():
  h = random.random()
  s = 1
  v = 1

  float_rgb = colorsys.hsv_to_rgb(h, s, v)
  rgb = [int(x * 255) for x in float_rgb]
  
  return tuple(rgb)

def interpolate(startColor, endColor, factor: float):
  recip = 1 - factor
  return(
      int(startColor[0] * recip + endColor[0] * factor),
      int(startColor[1] * recip + endColor[1] * factor),
      int(startColor[2] * recip + endColor[2] * factor),
  )

def generate_art(path: str):
  print("Generating...")
  target_size = 256
  target_scale = 2
  img_sizePx = target_scale * target_size
  padding = 15 * target_scale
  img_bgColor = (0, 0, 0)
  startColor = randomize_color()
  endColor = randomize_color()
  image = Image.new("RGB", (img_sizePx, img_sizePx), img_bgColor)

  points = []

  for _ in range(10):
        random_point = (
          random.randint(padding, img_sizePx - padding), 
          random.randint(padding, img_sizePx - padding),
        )
        points.append(random_point)
  thic = 0
  n_points = len(points) - 1
  for i, point in enumerate(points):

      overlay_image = Image.new("RGB", (img_sizePx, img_sizePx), img_bgColor)
      overay_drawing = ImageDraw.Draw(overlay_image)

      p1 = point

      if i == len(points) - 1:
        p2 = points[0]
      else:
        p2 = points[i + 1]

      color_factor = i / n_points
      line_color = interpolate(startColor, endColor, color_factor)
      lineXY = (p1, p2)
      thic += target_scale
      overay_drawing.line(lineXY, fill=line_color, width=thic)
      image = ImageChops.add(image, overlay_image)
  image = image.resize((target_size, target_size), resample=Image.ANTIALIAS)
  image.save(path)

if __name__ == "__main__":
  for i in range(10):
    generate_art(f"Crazy_Lines{i}.png")