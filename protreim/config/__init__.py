from __future__ import annotations
from pathlib import Path
import json
import logging
from typing import Any, Dict

import PySimpleGUI as sg

from protreim.common import DEFAULT_CONFIG_PATH
from protreim.config.base import ConfigBase, load
from protreim.config.outline import Outline
from protreim.config.text import Text
from protreim.config.title import Title
from protreim.config.background import BackGround


logger = logging.getLogger(__name__)


class Config(ConfigBase):
    outline: Outline = Outline() 
    text: Text = Text()
    title: Title = Title()
    background: BackGround = BackGround()
    

    def load(self, path: Path=DEFAULT_CONFIG_PATH) -> Config:
        """ Load config from `path`.

        If `path` doesn't exist, new config.json will be created there.

        If any exception raised, load default config.

        Parameters
        ----------
        path : pathlib.Path
            Path to config.json.
        
        Returns
        -------
        Config
            Config object loaded from `path`.
        """    
        if not path.exists():
            self.create(path)
            logger.info(f'Created {path}.')

        with path.open() as f:
            d: dict[str, Any] = json.load(f)
            logger.info(f'Loaded config from {str(path)}')
        return load(self, d)

            
        
    
    def asdict_recursive(self) -> Dict[str, Any]:
        def asdict(d: Dict[str, Any]) -> Dict[str, Any]:
            for key, val in d.items():
                if issubclass(type(val), ConfigBase):
                    d[key] = val.asdict()
                    asdict(d[key])
            return d

        return asdict(self.asdict())
        


    def create(self, path: Path) -> None:
        """ Create config.json """
        try:
            with open(path, 'w') as f:
                json.dump(self.asdict_recursive(), f, indent=2)
        except Exception as e:
            logger.error(f'Cannot create {path}.')
            logger.debug(e, exc_info=True)
            raise e


    def save(self, path: Path) -> None:
        """ Arias of Config.create(). """
        self.create(path)


    def GUI(self, parent: str='') -> sg.Frame:
        return sg.Frame(
            title='設定',
            layout=[
                [
                    sg.Column(
                        layout=[
                            [
                                self.outline.GUI('config')
                            ],
                            [
                                self.background.GUI('config')
                            ],
                        ],
                        vertical_alignment='top'
                    ),
                    sg.Column(
                        layout=[
                            [
                                self.title.GUI('config')
                            ],
                            [
                                self.text.GUI('config')
                            ],
                        ],
                        vertical_alignment='top'
                    ),
                ],
                [
                    sg.Input(key='load_config', visible=False, enable_events=True),
                    sg.FileBrowse('ファイルから読み込む', file_types=(('JSON', '*.json'),)),
                    sg.Save('設定を保存', key='save_config_button', bind_return_key=False, disabled=True),
                    sg.Input(key='saveas_config', visible=False, enable_events=True),
                    sg.SaveAs('名前を付けて保存', file_types=(('JSON', '*.json'),))
                ]
            ]
        )



