import PySimpleGUI as sg
from protreim.config import Config


def create_config_column(config: Config) -> sg.Column:
    """ Create config column.
    
    Returns
    -------
    PySimpleGUI.Column
    """
    return sg.Column(
        [
            [
                config.GUI()
            ]
        ],
        key='config_column',
        visible=False
    )