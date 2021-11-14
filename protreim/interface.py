from __future__ import annotations
from os import PathLike
from pathlib import Path
from functools import reduce
from typing import Union

from PIL import Image
from PIL import ImageFont

from protreim import foreground, process
from protreim.config import Config
from protreim.typing import ProcessFunc



class Protreim:
    """ API of Protreim.
    
    Examples
    --------
    >>> protreim = Protreim()
    # Customize config
    >>> protreim.config.outline.color = 'blue'
    >>> protreim.config.text.size += 10
    >>> protreim.config.background.color = 'skyblue'
    # Build process chain
    >>> protreim = protreim.extract_foreground().draw_outline().draw_text('text').draw_title('title')
    # Open image as PIL.Image.Image and call do()
    >>> from PIL import Image
    >>> im = Image.open('exampls/before.jpg')
    >>> im = protreim.do(im)
    """
    config: Config = Config()
    _process_chain: list[ProcessFunc] = []

        
    def submit(self, func: ProcessFunc) -> Protreim:
        """ Add ProcessFunc.
        
        Parameters
        ----------
        func : ProcessFunc
            `ProcessFunc` is type of `(PIL.Image.Image) -> PIL.Image.Image`.
        
        Returns
        -------
        Protreim
            New instance of `Protreim`.
        """
        protreim = Protreim()
        protreim.config = self.config
        protreim._process_chain = self._process_chain.copy()
        protreim._process_chain.append(func)
        return protreim


    def do(self, im: Image.Image) -> Image.Image:
        """ Do built process. 
        
        Parameters
        ----------
        im : PIL.Image.Image
            Image to process.
        
        Returns
        -------
        PIL.Image.Image
            Processed image.
        """
        im = process.resize(im)
        im = reduce(lambda im, f: f(im), self._process_chain, im)
        return im


    def extract_foreground(self) -> Protreim:
        """ Extract foreground from image. 
        
        Returns
        -------
        Protreim
            New instance of `Protreim`
        """
        def f(im: Image.Image) -> Image.Image:
            return foreground.extract_foreground(
                im,
                background_color=self.config.background.color,
                grabcut_iter_count=self.config.background.grabcut_iter_count,
                boundary_fore=self.config.background.boundary_fore,
                boundary_back=self.config.background.boundary_back
            )
        return self.submit(f)


    def draw_outline(self) -> Protreim:
        """ Draw outline on image. 
        
        Returns
        -------
        Protreim
            New instance of `Protreim`.
        """
        def f(im: Image.Image) -> Image.Image:
            return process.draw_outline(
                im,
                color=self.config.outline.color,
                width_x=self.config.outline.width_x,
                width_y=self.config.outline.width_y
            )
        return self.submit(f)


    def draw_text(self, text: str) -> Protreim:
        """ Draw text on image. 

        Parameters
        ----------
        text : str
            Text to draw on image.
        
        Returns
        -------
        Protreim
            New instance of `Protreim`.
        """
        font = ImageFont.truetype(
            self.config.text.font.name,
            self.config.text.font.size,
            self.config.text.font.face
        )
        def f(im: Image.Image) -> Image.Image:
            return process.draw_text(
                im,
                text,
                color=self.config.text.color,
                stroke_width=self.config.text.stroke_width,
                stroke_color=self.config.text.stroke_color,
                font=font,
                margin_top=self.config.text.y,
                margin_left=self.config.text.x
            )
        return self.submit(f)

    
    def draw_title(self, title: str) -> Protreim:
        """ Draw text on lower of image. 

        Parameters
        ----------
        title : str
            Text to draw on image.
        
        Returns
        -------
        Protreim
            New instance of `Protreim`.
        """
        font = ImageFont.truetype(
            self.config.title.font.name,
            self.config.title.font.size,
            self.config.title.font.face
        )
        def f(im: Image.Image) -> Image.Image:
            return process.draw_text(
                im,
                title,
                color=self.config.title.color,
                stroke_width=self.config.title.stroke_width,
                stroke_color=self.config.title.stroke_color,
                font=font,
                margin_top=self.config.title.y + 150,
                margin_left=self.config.title.x
            )
        return self.submit(f)
    

    def load_config(self, filepath: Union[str, PathLike[str]]) -> Protreim:
        """ Load config.json. 
        
        Parameters
        ----------
        filepath : str | os.Pathlike[str]
            path to config.json
        
        Returns
        -------
        Protreim
            New instance of `Protreim`.
        """
        protreim = Protreim()
        protreim.config.load(Path(filepath))
        protreim._process_chain = self._process_chain.copy()
        return protreim











    