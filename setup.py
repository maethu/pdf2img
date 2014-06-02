from setuptools import setup

setup(
    name='pdf2img',
    version='1.0.0',
    author="Mathias Leimgruber",
    author_email="mathias.leimgruber@gmail.com",
    license='Beerware',
    long_description=open('README.md', 'rb').read(),
    packages=['pdf2img'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[]
)
