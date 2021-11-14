import argparse
from pathlib import Path
import logging
from typing import Sequence, Optional

from PIL import Image

from protreim import __version__
from protreim.interface import Protreim
from protreim.common import (
    PROJECT_NAME,
    DEFAULT_CONFIG_PATH,
    PROCESSED_FLAG
)

rootlogger = logging.getLogger()
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)-5s: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
rootlogger.addHandler(handler)

class Namespace:
    file: Path = Path()
    output: Path = file.parent / (file.stem + PROCESSED_FLAG + file.suffix)
    title: str = ''
    text: str = ''
    config_path: Path = DEFAULT_CONFIG_PATH
    version: bool = False
    log_level: str = 'info'


parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog=PROJECT_NAME,
    description=f'{PROJECT_NAME} v{__version__}'
)

parser.add_argument(
    '--file',
    '-f',
    type=Path,
    default=Namespace.file,
    metavar='PATH',
    dest='file',
    help='filepath of image to process'
)
parser.add_argument(
    '-o',
    '--output',
    type=Path,
    dest='output',
    metavar='PATH',
    help='filepath of output'
)
parser.add_argument(
    '--title',
    type=str,
    dest='title',
    metavar='TEXT',
    help='title text to put on image'
)
parser.add_argument(
    '--text',
    type=str,
    dest='text',
    metavar='TEXT',
    help='text to put on image'
)
parser.add_argument(
    '-c',
    '--config',
    type=Path,
    default=Namespace.config_path,
    dest='config_path',
    metavar='PATH',
    help='path to config.json [default: %(default)s]'
)
parser.add_argument(
    '--log-level',
    type=str,
    choices=['critial', 'error', 'warning', 'info', 'debug'],
    default=Namespace.log_level,
    metavar='LEVEL',
    dest='log_level',
    help='set logging level [default: %(default)s]'
)
parser.add_argument(
    '--version',
    '-v',
    action='store_true',
    dest='version',
    help='print version'
)


def parse_args(args: Optional[Sequence[str]]=None) -> Namespace:
    return parser.parse_args(args, Namespace())


def execute() -> None:
    args = parse_args()
    logger.setLevel(args.log_level.upper())
    if args.version:
        print(PROJECT_NAME, __version__)
        return

    if not args.file.name:
        parser.print_help()
        return

    protreim = Protreim()
    
    try:
        protreim.load_config(args.config_path)
    except Exception as e:
        logger.error(f'Cannot load {args.config_path}.')
        logger.debug(e, exc_info=True)
        return
    
    try:
        logger.debug(f'Processing...')
        im: Image.Image = Image.open(args.file)
        im = protreim.\
            extract_foreground().\
            draw_outline().\
            draw_title(args.title).\
            draw_text(args.text).\
            do(im)
        logger.debug(f'Processed.')
    except Exception as e:
        logger.error(f'Cannot process.')
        logger.debug(e, exc_info=True)
        return

    try:
        logger.debug(f'Saving...')
        if not args.output.parent.exists():
            args.output.parent.mkdir(parents=True)
        im.save(args.output)
        logger.debug(f'Saved as {args.output}.')
    except Exception as e:
        logger.error(f'Cannot save image.')
        logger.debug(e, exc_info=True)
        return

    

