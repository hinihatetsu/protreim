from pathlib import Path
import logging
from typing import Dict, List, Any, Optional

from PIL import Image, ImageTk
import PySimpleGUI as sg

from protreim.interface import Protreim
from protreim.common import DEFAULT_CONFIG_PATH, PROCESSED_FLAG, PROJECT_NAME
from protreim.gui.icon import MAINICON
from protreim.gui.windows.base import WindowBase
from .columns.main import create_main_column
from .columns.config import create_config_column

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RootWindow(WindowBase):
    title = PROJECT_NAME
    config_path: Path = DEFAULT_CONFIG_PATH
    protreim: Protreim = Protreim().extract_foreground().draw_outline()
    _img_cache: Optional[Image.Image] = None
    


    @property
    def icon(self) -> Optional[bytes]:
        return MAINICON

    @property
    def layout(self) -> List[Any]:
        layout = [
            [
                create_main_column(),
                create_config_column(self.protreim.config),
            ]            
        ]
        return layout


    def on_event(self, window: sg.Window, event: Optional[str], values: Optional[Dict[str, Any]]) -> None:
        
        if event is None:
            self.on_close(window)
            return

        if values is None:
            self.on_close(window)
            return

        if event == 'file':
            self.on_file_selected(window)

        if event == 'process_button':
            self.on_process_button_pushed(window)

        if event == 'save_button_bind':
            self.on_event(window, 'save_button', values)

        if event == 'save_button':
            self.on_save_button_pushed(window)

        if event == 'config_button':
            self.on_config_button_pushed(window)
            
        if event.split(sep='.')[0] == 'config':
            self._update_config(event, values)
            self.on_config_changed(window)
            self.on_process_button_pushed(window)
            
        if event == 'load_config':
            self.on_load_config(window)
            self._update_config_GUI(window, values)

        if event == 'save_config_button':
            self.on_save_config_button_pushed(window)

        if event == 'saveas_config' and values['saveas_config']:
            self.on_saveas_config(window)

    
    def on_close(self, window: sg.Window) -> None:
        """ Called when close button is pushed. """
        save_config_button: sg.Button = window['save_config_button']
        if not save_config_button.Disabled:
            ans = sg.popup_yes_no(
                '未保存の設定変更があります。', 
                '保存しますか？',
                icon=MAINICON
            )
            if ans == 'Yes':
                self.protreim.config.save(self.config_path)


    def on_file_selected(self, window: sg.Window) -> None:
        """ Called when file is selected. """
        input_file: sg.Input = window['file']
        save_file: sg.Input = window['save_file']
        process_button: sg.Button = window['process_button']
        filepath = Path(input_file.get())
        save_file.update(
            str(
                filepath.parent / (filepath.stem + PROCESSED_FLAG  + filepath.suffix)
            )
        )
        process_button.update(disabled=False)
        process_button.click()


    def on_process_button_pushed(self, window: sg.Window) -> None:
        """ Called when process button is pushed. """
        input_file: sg.Input = window['file']
        input_title: sg.Input = window['title']
        input_text: sg.Input = window['text']
        processed_image: sg.Image = window['processed_image']
        save_button: sg.Button = window['save_button']
        if not input_file.get():
            return
        title: str = input_title.get()
        text: str = input_text.get()
        if input_file.get():
            input_title.set_focus()
        if input_title.get():
            input_text.set_focus()

        if self._img_cache:
            im = self._img_cache.copy()
            im.putalpha(150)
            processed_image.update(data=ImageTk.PhotoImage(im))
            window.finalize()
        
        self._img_cache = self.protreim.\
            draw_text(text).\
            draw_title(title).\
            do(Image.open(input_file.get()))
        processed_image.update(data=ImageTk.PhotoImage(self._img_cache))
        save_button.update(disabled=False)


    def on_save_button_pushed(self, window: sg.Window) -> None:
        """ Called when save button is pushed. """
        save_file: sg.Input = window['save_file']
        if not save_file.get():
            return
        if self._img_cache:
            self._img_cache.save(save_file.get())
            sg.popup(f'{save_file.get()}に保存しました。')


    def on_config_button_pushed(self, window: sg.Window) -> None:
        """ Called when config button is pushed. """
        config_column: sg.Column = window['config_column']
        config_column.update(visible=not config_column.visible)


    def on_config_changed(self, window: sg.Window) -> None:
        """ Called when config is changed. """
        save_config_button: sg.Button = window['save_config_button']
        save_config_button.update(disabled=False)


    def on_load_config(self, window: sg.Window) -> None:
        """ Called when loading config. """
        input_config: sg.Input = window['load_config']
        if not input_config.get():
            return
        self.config_path = Path(input_config.get())
        self.protreim.config.load(self.config_path)


    def on_save_config_button_pushed(self, window: sg.Window) -> None:
        """ Called save-config button is pushed. """
        save_config_button: sg.Button = window['save_config_button']
        self.protreim.config.save(self.config_path)
        save_config_button.update(disabled=True)


    def on_saveas_config(self, window: sg.Window) -> None:
        """ Called when saveas config. """
        input_saveas_config: sg.Input = window['saveas_config']
        self.config_path = Path(input_saveas_config.get())
        self.protreim.config.save(self.config_path)


    def _update_config(self, event: str, values: Dict[str, Any]) -> None:
        """ Called when config is changed on GUI.  
        
        Parameters
        ----------
        event : str | None
            Event. See also PySimpleGUI.Window.read().
        values : dict[str, Any] | None
            Values. See also PySimpleGUI.Window.read().
        """
        try:
            domain = event.split('.')
            key = domain.pop()

            if key in {'color', 'stroke_color'} and values[event] == 'None':
                return

            code = f'self.protreim.{".".join(domain)}.update({key}=type(self.protreim.{event})(values["{event}"]))'
            eval(code)
        except Exception as e:
            logger.debug(e, exc_info=True)
            logger.debug(code)
        # Examples of `code`
        # self._protreim.config.outline.update(color=values['config.outline.color']) 
        # self._protreim.config.text.font.update(size=int(values['config.text.font.size']))
        # self._protreim.config.background.update(color=values['config.background.color'])


    def _update_config_GUI(self, window: sg.Window, values: Dict[str, Any]) -> None:
        """ Called when config is loaded from file.
        
        Parameters
        ----------
        window : PySimpleGUI.Window
            To get widgets in the window.
        values : Dict[str, Any]
            Values. See also PySimpleGUI.Window.read().
        """
        for key in values.keys():
            if key.split('.')[0] == 'config':
                value = eval(f'self.protreim.{key}')
                window[key].update(value)