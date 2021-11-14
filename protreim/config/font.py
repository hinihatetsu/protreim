

import PySimpleGUI as sg

from .base import ConfigBase


class Font(ConfigBase):
    name: str = 'meiryo.ttc'
    face: int = 0
    size: int = 48


    def GUI(self, parent: str='') -> sg.Frame:
        label_size = (10, None)
        size_list = list(range(216))
        return sg.Frame(
            'フォント',
            layout=[
                [
                    sg.Text('ファイル', size=label_size), 
                    sg.Input(
                        default_text=self.name, 
                        key=f'{parent}.font.name', 
                        size=(10, None),
                        enable_events=True
                    ),
                    sg.FileBrowse(disabled=True)
                ],
                [
                    sg.Text('フェイス', size=label_size),
                    sg.Input(
                        default_text=self.face,
                        key=f'{parent}.font.face',
                        size=6,
                        enable_events=True
                    ),
                ],
                [
                    sg.Text('サイズ', size=label_size),
                    sg.Combo(
                        size_list, 
                        default_value=self.size, 
                        key=f'{parent}.font.size', 
                        enable_events=True
                    )
                ],
            ]
        )


