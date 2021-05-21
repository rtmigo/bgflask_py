from pathlib import Path
from typing import Dict, Any

from setuptools import setup


def load_constants(pattern='*/_constants.py') -> Dict[str, Any]:
    """Finds in the parent dir a single file by the pattern and imports module
    from it. Returns the dictionary of globals defined in the module."""
    import importlib.util as ilu

    # finding the _constants.py (or anything defined by the pattern)
    candidates = list(Path(__file__).parent.glob(pattern))
    assert len(candidates) == 1, f"Candidates: {candidates}"
    filename = candidates[0]

    # importing module from `filename`
    spec = ilu.spec_from_file_location('', filename)
    module = ilu.module_from_spec(spec)
    # noinspection Mypy
    spec.loader.exec_module(module)
    return module.__dict__


constants = load_constants()

readme = (Path(__file__).parent / 'README.md').read_text()
name="runwerk"

setup(
    name=name,
    version=constants['__version__'],

    author="Artёm IG",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/runwerk_py#readme',

    packages=[name],
    install_requires=["bgprocess"],
    python_requires=">=3.7",

    description="Runs Werkzeug server locally in a background process, so in can "
                "be tested with HTTP requests",

    long_description=readme,
    long_description_content_type='text/markdown',

    license='MIT',

    keywords="""werkzeug flask unit testing test  unit-test wsgi process timeout""".split(),

    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Documentation',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX",
    ],
)
