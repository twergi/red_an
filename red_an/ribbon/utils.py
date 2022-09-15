from PIL import Image


def square_crop(path):
    with Image.open(path) as im:
        x = im.width
        y = im.height

        if x % 2 != y % 2:
            if x % 2:
                x -= 1
            else:
                y -= 1

        if im.width > im.height:
            dif = (x - y) // 2
            im = im.crop((dif, 0, dif + y, y))

        if im.height > im.width:
            dif = (y - x) // 2
            im = im.crop((0, dif, x, dif + x))

        if x > 300:
            im.thumbnail((300, 300))
        im.save(path)
