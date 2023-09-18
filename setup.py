from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='shortl',
    version='0.0.1',
    description='A Python module for simple link shortening.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mdonmez/shortl',
    author='mdonmez',
    license='GPL-3.0-or-later',
    package_dir={"shortl.py": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['requests', 'clipboard'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
    ],
)
