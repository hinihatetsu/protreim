
import PySimpleGUI as sg

from protreim.typing import Color
from .base import ConfigBase

class Outline(ConfigBase):
    color: Color = 'black'
    width_x: int = 30
    width_y: int = 30

    def GUI(self, parent: str='') -> sg.Frame:
        label_size = (10, None)
        input_size_color = (9, None)
        width_range = list(range(300))
        return sg.Frame(
            '枠線',
            layout=[
                [
                    sg.Text('色', size=label_size),
                    sg.Input(
                        default_text=self.color,
                        key=f'{parent}.outline.color', 
                        size=input_size_color,
                        enable_events=True
                    ),
                    sg.ColorChooserButton('選択'),
                ],
                [
                    sg.Text('横幅', size=label_size),
                    sg.Combo(
                        width_range, 
                        default_value=self.width_x, 
                        key=f'{parent}.outline.width_x', 
                        enable_events=True
                    ),
                ],
                [
                    sg.Text('縦幅', size=label_size),
                    sg.Combo(
                        width_range, 
                        default_value=self.width_y, 
                        key=f'{parent}.outline.width_y', 
                        enable_events=True
                    )
                ],
            ]
        )