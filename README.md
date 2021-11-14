# Protreim
**Protreim** is a useful tool to make pictures more noticeable.

This library is originally created for tires pictures. 
However, you can extract something black from pictures and remove background with **Protreim**.

### Before

![before](https://github.com/ecoreuse/protreim/blob/master/examples/before.jpg?raw=true)

### After

![after](https://github.com/ecoreuse/protreim/blob/master/examples/after.jpg?raw=true)


## Requirements

Python 3.8 or later

Install python on your computer from https://www.python.org/downloads/.

## Installation

```shell
pip install protreim
```

## Usage

### CLI
```shell
protreim --title <title> --text <text>　--file <filename>
```

Processed images are saved in cwd.

### GUI
```shell
protreimGUI
```
![gui](https://github.com/ecoreuse/protreim/blob/master/examples/protreim_gui.png?raw=true)

Supports only Japanese, so far.

### Python Interface

First, create a `Protreim` instance.
```python
>>> from protreim import Protriem
>>> protreim = Protreim()
```

Second, edit config as you like.
```python
>>> protreim.config.outline.color = 'blue'
>>> protreim.config.text.size += 10
>>> protreim.config.background.color = 'skyblue'
```

Third, build your process chain.
```python
>>> protreim = protreim.\
... extract_foreground().\
... draw_outline().\
... draw_text('text').\
... draw_title('title')
```

Then, call do() with a PIL.Image.Image instance!
```python
>>> from PIL import Image
>>> im = Image.open('my_picture.jpg')
>>> im = protreim.do(im)
>>> im.save('procesed.jpg')
```

Example
```python
from protreim import Protreim
from PIL import Image

im = Image.open('example.jpg')

protreim = Protreim()
protreim.config.outline.color = 'blue'
im = protreim.\
    extract_foreground().\
    draw_outline().\
    draw_text('text').\
    draw_title('title').\
    do(im)

im.save('processed.jpg')
```

#### Load config from file
```python
protreim.load_config('config.json') # load config from file
```

#### Insert your function
```python
from protreim import Protreim
from PIL import Image
def your_func(im: Image.Image) -> Image.Image:
    return im

protreim = Protreim()
im = protreim.\
    extract_foreground().\
    submit(your_func).\
    draw_outline().\
    do(im)
```

## Configuration

Edit `config.json` if you want to customize processing.

## License
MIT License
