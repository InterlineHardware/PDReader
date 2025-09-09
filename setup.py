from setuptools import setup
setup(
    name="pdreader",
    version="1.0",
    description="A product data reader tool",
    author="Your Name",
    packages=["src"],
    entry_points={
        'console_scripts': [
            'pdreader = src.main:main'
        ]
    },

)