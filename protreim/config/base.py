from abc import ABC, abstractmethod
from typing import Dict, List, Any, TypeVar

import PySimpleGUI as sg


class ConfigBase(ABC):
    """ Base class of config class. 
    
    All config class must inherit this class.
    """
    def __init__(self) -> None:
        """ Set class variables as instance variables. """
        for field in self.fields:
            setattr(self, field, getattr(self, field))


    @property
    def fields(self) -> List[str]:
        """ Fields of configuration. """
        return list(self.__annotations__.keys())

    
    def update(self, *args: Any, **kwargs: Any) -> None:
        """ Update instance variables with kwargs. """
        for key, val in kwargs.items():
            if key in self.__annotations__:
                setattr(self, key, val)
    

    
    def asdict(self) -> Dict[str, Any]:
        """ Return dict of ConfigBase class. """
        return {key:getattr(self, key) for key in self.fields}

    
    @abstractmethod
    def GUI(self, parent: str='') -> sg.Frame:
        """ GUI.

        Parameters
        ----------
        parent : str
            keyword to tell apart instances in the same window.

        Returns
        -------
        PySimpleGUI.Frame
        """
        pass


ConfigType = TypeVar('ConfigType', bound=ConfigBase)
def load(config: ConfigType, d: Dict[str, Any]) -> ConfigType:
    fields = config.fields
    for field in fields:
        if field not in d:
            continue
        
        val = d[field]
        if type(val) is dict:
            kwargs = {
                field: load(getattr(config, field), val,)
            }
        elif field in {'color', 'stroke_color'}:
            kwargs = {
                field: tuple(val[:3]) if type(val) is list else val
            }
        else:
            kwargs = {
                field: val
            }
        config.update(**kwargs)
    return config