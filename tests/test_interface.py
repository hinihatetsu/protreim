from unittest import TestCase
from protreim.interface import Protreim
from PIL import Image

test_image = './tests/test_image.jpg'

def dummy(im: Image.Image) -> Image.Image:
    return im


class TestProtreim(TestCase):

    def setUp(self) -> None:
        self.image: Image.Image = Image.open(test_image)


    def test_submit(self) -> None:
        p = Protreim()
        p2 = p.submit(dummy)
        assert len(p._process_chain) == 0
        self.assertEqual(p2._process_chain.pop(), dummy)
    

    def test_do(self) -> None:
        im = Protreim().submit(dummy).do(self.image)
        self.assertEqual(type(im), Image.Image)


    def test_extract_foreground(self) -> None:
        im = Protreim().extract_foreground().do(self.image)
        im.show(self.test_extract_foreground.__name__)
        self.assertEqual(type(im), Image.Image)


    def test_draw_outline(self) -> None:
        im = Protreim().draw_outline().do(self.image)
        im.show(self.test_draw_outline.__name__)
        self.assertEqual(type(im), Image.Image)


    def test_draw_text(self) -> None:
        text: str = 'text'
        p = Protreim()
        p.config.text.font.name = 'DejaVuSans.ttf'
        im = p.draw_text(text).do(self.image)
        im.show(f'{self.test_draw_text.__name__}, `{text}` shold show')
        self.assertEqual(type(im), Image.Image)


    def test_draw_title(self) -> None:
        title: str = 'title'
        p = Protreim()
        p.config.title.font.name = 'DejaVuSans.ttf'
        im = p.draw_title(title).do(self.image)
        im.show(f'{self.test_draw_title.__name__}, `{title}` shold show')
        self.assertEqual(type(im), Image.Image)
    

    def tearDown(self) -> None:
        self.image.close()


