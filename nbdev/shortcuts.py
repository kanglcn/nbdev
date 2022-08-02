# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/16_shortcuts.ipynb.

# %% auto 0
__all__ = ['BASE_QUARTO_URL', 'install_quarto', 'install', 'docs', 'preview', 'deploy', 'pypi', 'conda', 'release', 'prepare',
           'chelp']

# %% ../nbs/16_shortcuts.ipynb 2
import sys, shutil
from os import system
from fastcore.utils import *
from fastcore.script import *

from .read import get_config
from .test import nbdev_test
from .clean import nbdev_clean
from .doclinks import nbdev_export
from .cli import *

BASE_QUARTO_URL='https://www.quarto.org/download/latest/'

def _dir(): return get_config().path("lib_path").parent
def _c(f, *args, **kwargs): return f.__wrapped__(*args, **kwargs)

# %% ../nbs/16_shortcuts.ipynb 4
def _install_linux():
    system(f'curl -LO {BASE_QUARTO_URL}quarto-linux-amd64.deb')
    system('sudo dpkg -i *64.deb && rm *64.deb')
    
def _install_mac():
    system(f'curl -LO {BASE_QUARTO_URL}quarto-macos.pkg')
    system('sudo installer -pkg quarto-macos.pkg -target /')

def install_quarto():
    "Install latest Quarto on macOS or Linux, prints instructions for Windows"
    system('sudo echo "...installing Quarto"')
    if 'darwin' in sys.platform: _install_mac()
    elif 'linux' in sys.platform: _install_linux()
    else: print('Please visit https://quarto.org/docs/get-started/ to install quarto')
    
def install():
    "Install Quarto and the current library"
    install_quarto()
    if (get_config().path('lib_path')/'__init__.py').exists():
        system(f'pip install -e "{_dir()}[dev]"')

# %% ../nbs/16_shortcuts.ipynb 7
def _quarto_installed(): return bool(shutil.which('quarto'))

@call_parse
def docs(
    path:str=None, # Path to notebooks
    doc_path:str=None, # Path to output docs
    symlinks:bool=False, # Follow symlinks?
    folder_re:str=None, # Only enter folders matching regex
    skip_file_glob:str=None, # Skip files matching glob
    skip_file_re:str=None, # Skip files matching regex
    preview:bool=False # Preview the site instead of building it
):
    "Generate docs"
    if not _quarto_installed(): install()
    nbdev_quarto.__wrapped__(path=path, doc_path=doc_path, symlinks=symlinks, folder_re=folder_re,
                 skip_file_glob=skip_file_glob, skip_file_re=skip_file_re, preview=preview)

# %% ../nbs/16_shortcuts.ipynb 9
def preview():
    "Start a local docs webserver"
    if not _quarto_installed(): install()
    _c(nbdev_sidebar)
    _c(nbdev_quarto, preview=True)

# %% ../nbs/16_shortcuts.ipynb 11
def deploy():
    "Deploy docs to GitHub Pages"
    docs()
    _c(nbdev_ghp_deploy)

# %% ../nbs/16_shortcuts.ipynb 13
def _dist(): system(f'cd {_dir()}  && rm -rf dist && python setup.py sdist bdist_wheel')
    
def pypi(ver_bump=True):
    "Create and upload Python package to PyPI"
    _dist()
    system(f'twine upload --repository pypi {_dir()}/dist/*')
    if ver_bump: _c(nbdev_bump_version)
    
def conda(ver_bump=True): 
    "Create and upload a conda package"
    system(f'fastrelease_conda_package --mambabuild --upload_user fastai')
    if ver_bump: _c(nbdev_bump_version)
    
def release():
    "Release both conda and PyPI packages"
    pypi(ver_bump=False)
    conda(ver_bump=False)
    _c(nbdev_bump_version)

# %% ../nbs/16_shortcuts.ipynb 15
def prepare():
    "Export, test, and clean notebooks"
    _c(nbdev_export)
    nbdev_test.__wrapped__()
    _c(nbdev_clean)

# %% ../nbs/16_shortcuts.ipynb 17
@call_parse
def chelp():
    "Show help for all console scripts"
    from fastcore.xtras import console_help
    console_help('nbdev')
