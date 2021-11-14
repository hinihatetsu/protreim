import PySimpleGUI as sg

from protreim.typing import Color
from .base import ConfigBase

class BackGround(ConfigBase):
    color: Color = 'white'
    grabcut_iter_count: int = 5
    boundary_fore: int = 90
    boundary_back: int = 160

    def GUI(self, parent: str='') -> sg.Frame:
        label_size = (10, None)
        input_size_color = (9, None)
        return sg.Frame(
            '背景',
            layout=[
                [
                    sg.Text('色', size=label_size),
                    sg.Input(
                        default_text=self.color,
                        key=f'{parent}.background.color', 
                        size=input_size_color,
                        enable_events=True
                    ),
                    sg.ColorChooserButton('選択'),
                ],
                [
                    sg.Text('GrabCut回数', size=label_size),
                    sg.Combo(
                        list(range(100)), 
                        default_value=self.grabcut_iter_count,  
                        key=f'{parent}.background.grabcut_iter_count',
                        enable_events=True
                    )
                ],
                [
                    sg.Text('前景境界', size=label_size),
                    sg.Combo(
                        list(range(0, 255)), 
                        default_value=self.boundary_fore, 
                        key=f'{parent}.background.boundary_fore', 
                        enable_events=True
                    ),
                ],
                [
                    sg.Text('背景境界', size=label_size),
                    sg.Combo(
                        list(range(0, 255)), 
                        default_value=self.boundary_back, 
                        key=f'{parent}.background.boundary_back',
                        enable_events=True
                    )
                ]
            ]
        )