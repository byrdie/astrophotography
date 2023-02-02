from setuptools import setup, find_packages

setup(
    name='astrophotography',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'astropy',
        'opencv-python',
    ],
    url='https://github.com/byrdie/astrophotography',
    license='',
    author='Roy Smart',
    author_email='roytsmart@gmail.com',
    description='Collction of Python scripts for some simple astrophotography'
)
