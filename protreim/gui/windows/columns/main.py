import PySimpleGUI as sg

def create_main_column() -> sg.Column:
    """ Create main column.

    Returns
    -------
    PySimpleGUI.Column
    """
    return sg.Column(
        [
            [
                sg.Text('加工する画像を選択してください')
            ],
            [
                sg.Text('ファイル'),
                sg.Input(key='file', readonly=True, enable_events=True),
                sg.FileBrowse('ファイルを選択', file_types=(('JPEG', '*.jpg'), ('JPEG', '*.jpeg'), ('PNG', '*.png')))

            ],
            [
                sg.Text('タイトル'),
                sg.Input(key='title'),
            ],
            [
                sg.Text('テキスト'),
                sg.Input(key='text')
            ],
            [
                sg.Text('保存先　'),
                sg.Input(key='save_file'),
                sg.SaveAs('保存先を選択', default_extension='.jpg', file_types=(('JPEG', '*.jpg'), ('PNG', '*.png')))
            ],
            [
                sg.Button('設定', key='config_button'),
                sg.Button('加工', key='process_button', disabled=True, bind_return_key=True),
                sg.Button('保存', key='save_button', disabled=True),
            ],
            [
                sg.Image(key='processed_image'),
            ]
        ],
        key='main_column',
        vertical_alignment='top'
    )