from PIL import Image

def render_recurrence_plot(
  size: int, 
  plot: list[bool], 
  flip_y: bool=True
) -> Image.Image:
  
  assert size * size == len(plot)
  
  img = Image.new("1", (size, size))
  
  for i in range(size):
    for j in range(size):
      index = j + (size - i - 1) * size if flip_y else j + i * size
      img.putpixel((j, i), 1 if plot[index] else 0)

  return img