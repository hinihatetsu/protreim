from PIL import Image, ImageDraw, ImageFont

from protreim.typing import Color


def resize(im: Image.Image) -> Image.Image:
    """ Resize image to be 600px in pixel.

    Parameters
    ----------
    im : PIL.Image.Image
        Image to process
    
    Returns
    -------
    PIL.Image.Image
        Resized image whose width is 600px.
    """
    w, h = im.size
    new_w = 600
    new_h = h * new_w // w
    return im.resize((new_w, new_h))


def draw_outline(
    im: Image.Image,
    color: Color,
    width_x: int,
    width_y: int,
) -> Image.Image:
    """ Draw outline on the image.

    Parameters
    ----------
    im : PIL.Image.Image.
        Target image.
    color : Color
        Color of outline.
    width_x : int
        Width in pixel of side outline.
    width_y : int
        Width in pixel of topdown outline. 

    Returns
    -------
    PIL.Image.Image
        Image on which outline is drawn.
    """
    res: Image.Image = im.copy()
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(res)
    w, h = im.size
    draw.rectangle((0, 0, width_x, h), fill=color)
    draw.rectangle((w-width_x, 0, w, h), fill=color)
    draw.rectangle((0, 0, w, width_y), fill=color)
    draw.rectangle((0, h-width_y, w, h), fill=color)
    return res


def draw_text(
    im: Image.Image,
    text: str,
    color: Color,
    stroke_width: int,
    stroke_color: Color,
    font: ImageFont.ImageFont,
    margin_top: int = 0,
    margin_left: int = 0,
) -> Image.Image:
    """ Draw `text` at center of image

    Parameters
    ----------
    im : PIL.Image.Image
        Target image.
    text : str
        String to draw.
    color : Color
        Color of the text.
    stroke_width : int
        Width of stroke.
    stroke_color : Color
        Color of stroke.
    font : PIL.ImageFont.ImageFont
        Font of the text.
    margin_top : int
        Margin top in pixel.
    margin_left : int
        Margin left in pixel.

    Returns
    -------
    PIL.Image.Image
        Image on which `text` is written.
    """
    res: Image.Image = im.copy()
    w, h = im.size
    draw = ImageDraw.Draw(res)
    text_w, text_h = draw.textsize(text, font=font)
    place = ((w-text_w)/2 + margin_left, (h-text_h)/2 + margin_top)
    draw.multiline_text(place, text, fill=color, font=font, stroke_width=stroke_width, stroke_fill=stroke_color)
    return res

