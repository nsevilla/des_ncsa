""" Settings for app"""
import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
if os.environ['APP_ROOT'] == '' or os.environ['APP_ROOT'] == '/':
    APP_ROOT = ''
else:
    APP_ROOT = r'/{}/'.format(os.environ['APP_ROOT'])
    # Ensure string is like "/APP_ROOT" without trailing slash :
    APP_ROOT = os.path.normpath(APP_ROOT)
STATIC_PATH = os.path.join(DIRNAME, 'static')
TEMPLATE_PATH = os.path.join(DIRNAME, 'templates')
SVA1_PATH = os.path.join(STATIC_PATH, 'files/SVA1')
import logging
# log linked to the standard error stream
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)-8s - %(message)s',
                    datefmt='%d/%m/%Y %Hh%Mm%Ss')
# console = logging.StreamHandler(sys.stderr)
