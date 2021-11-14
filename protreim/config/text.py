
import PySimpleGUI as sg

from protreim.typing import Color
from .base import ConfigBase
from .font import Font


class Text(ConfigBase):
    font: Font = Font()
    color: Color = 'white'
    stroke_width: int = 0
    stroke_color: Color = 'black'
    x: int = 0
    y: int = 0

    def GUI(self, parent: str='') -> sg.Frame:
        label_size = (10, None)
        input_size_color = (9, None)
        margin_range = list(range(-300, 300))
        return sg.Frame(
            title='テキスト',
            layout=[
                [
                    sg.Text('色', size=label_size),
                    sg.Input(
                        default_text=self.color,
                        key=f'{parent}.text.color', 
                        size=input_size_color,
                        enable_events=True
                    ),
                    sg.ColorChooserButton('選択'),
                ],
                [
                    sg.Text('ストローク幅', size=label_size),
                    sg.Combo(
                        list(range(10)), 
                        default_value=self.stroke_width, 
                        key=f'{parent}.text.stroke_width', 
                        enable_events=True
                    ),
                ],
                [
                    sg.Text('ストローク色', size=label_size),
                    sg.Input(
                        default_text=self.stroke_color, 
                        key=f'{parent}.text.stroke_color', 
                        size=input_size_color, 
                        enable_events=True
                    ),
                    sg.ColorChooserButton('選択')
                ],
                [
                    sg.Text('位置x', size=label_size),
                    sg.Combo(
                        margin_range, 
                        default_value=self.x, 
                        key=f'{parent}.text.x', 
                        enable_events=True
                    ),
                ],
                [    
                    sg.Text('位置y', size=label_size),
                    sg.Combo(
                        margin_range, 
                        default_value=self.y, 
                        key=f'{parent}.text.y', 
                        enable_events=True
                    ),
                ],
                [
                    self.font.GUI(f'{parent}.text')
                ],
            ]
        )