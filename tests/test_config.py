from unittest import TestCase

import PySimpleGUI as sg
from protreim.typing import Color
from protreim.common import DEFAULT_CONFIG_PATH 
from protreim import config as c
from protreim.config.base import ConfigBase, load

class ChildConfig(ConfigBase):
    name: str = 'child'

    def GUI(self, parent: str='') -> sg.Frame:
        return sg.Frame('')


class SampleConfig(ConfigBase):
    id: int = 0
    name: str = ''
    color: Color = 'black'
    child: ChildConfig = ChildConfig()

    def GUI(self, parent: str='') -> sg.Frame:
        return sg.Frame('')



class TestConfigBase(TestCase):

    def test_update_with_id(self) -> None:
        config = SampleConfig()
        expect = 1
        config.update(id=expect)
        actual = config.id
        self.assertEqual(expect, actual)


    def test_update_with_name(self) -> None:
        config = SampleConfig()
        expect = 'name'
        config.update(name=expect)
        actual = config.name
        self.assertEqual(expect, actual)

    
    def test_asdict(self) -> None:
        config = SampleConfig()
        actual = config.asdict()
        expect = {key:getattr(config, key) for key in config.fields}
        self.assertEqual(expect, actual)
    

class TestLoad(TestCase):

    def setUp(self) -> None:
        self.config = SampleConfig()


    def test_load_with_field_id(self) -> None:
        expect = 1
        d = {'id': expect}
        actual = load(self.config, d).id
        self.assertEqual(expect, actual)


    def test_load_with_field_color_str(self) -> None:
        expect = 'white'
        d = {'color': expect}
        actual = load(self.config, d).color
        self.assertEqual(expect, actual)


    def test_load_with_field_color_list(self) -> None:
        expect = (0, 0, 0)
        d = {'color': list(expect)}
        actual = load(self.config, d).color
        self.assertEqual(expect, actual)

    
    def test_load_with_field_color_list_long(self) -> None:
        expect = (0, 0, 0)
        d = {'color': list(expect)+[0]}
        actual = load(self.config, d).color
        self.assertEqual(expect, actual)


    def test_load_with_field_child(self) -> None:
        expect = 'child_0'
        d = {'child': {'name': expect}}
        actual = load(self.config, d).child.name
        self.assertEqual(expect, actual)



class TestConfig(TestCase):
    
    def setUp(self) -> None:
        self.config = c.Config()

    
    def test_load(self) -> None:
        expect= self.config
        actual = self.config.load(DEFAULT_CONFIG_PATH)
        self.assertEqual(expect, actual)
