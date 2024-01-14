from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

def crop(image:Image):
    exif = image.getexif()
    if exif is not None:
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "Orientation":
                rotation = value
                if rotation == 2:
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                elif rotation == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif rotation == 4:
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                elif rotation == 5:
                    image = image.transpose(Image.ROTATE_270)
                elif rotation == 6:
                    image = image.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
                elif rotation == 7:
                    image = image.transpose(Image.ROTATE_90)
                elif rotation == 8:
                    image = image.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)

    min_img_axis = min(image.size)

    croped_img = image.crop(box=(0, 0, min_img_axis, min_img_axis))

    croped_img = croped_img.convert('RGB')

    return croped_img