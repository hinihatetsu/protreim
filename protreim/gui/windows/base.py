from abc import ABC, abstractmethod
from typing import List, Any, Optional, Tuple, Dict


import PySimpleGUI as sg

class WindowBase(ABC):
    title: str
    location: Tuple[int, int] = (100, 100)

    @property
    def icon(self) -> Optional[bytes]:
        return None

    @property
    def layout(self) -> List[Any]:
        return []

    def window(self, **kwargs: Dict[str, Any]) -> sg.Window:
        """ Create PySimpleGUI.Window instance with `kwargs`.
        
        Returns
        -------
        PySimpleGUI.Window
        """
        _kwargs: Dict[str, Any] = {
            'title': self.title,
            'layout': self.layout,
            'location': self.location,
            'icon': self.icon,
            'resizable': True
        }
        _kwargs.update(kwargs)
        return sg.Window(**_kwargs)


    def show(self) -> None:
        """ Enter event loop. """
        window = self.window()
        window.finalize()
        while True:
            event, values = window.read()
            self.on_event(window, event, values)
            if event == sg.WIN_CLOSED:
                break
        window.close()


    def bind(self, window: sg.Window) -> None:
        pass
    

    @abstractmethod
    def on_event(self, window: sg.Window, event: Optional[str], values: Optional[Dict[str, Any]]) -> None:
        """ Called when window catches an event.
        
        Parameters
        ----------
        window : PySimpleGUI.Window
            To get widgets in the window.
        event : str | None
            Event. See also PySimpleGUI.Window.read().
        values : dict[str, Any] | None
            Values. See also PySimpleGUI.Window.read().
        """
        pass