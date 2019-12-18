from setuptools import setup


setup(
    name='epub_lib',
    version='0.0.1',
    packages=['app'],
    entry_points={'console_scripts': ['load_pages = app.main:main']},
)
