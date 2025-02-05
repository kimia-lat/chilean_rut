from setuptools import setup, find_packages

setup(
    name='k-chilean-rut',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pydantic_core==2.27.2'
    ],
    extras_require={
    },
    tests_require=[
        'pytest',
        'pytest-asyncio',
        'dotenv'
    ],
    description='Simple Chilean Rut class with Pydantic validation and serialization support.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Gonzalo',
    author_email='gonzalo@kimia.lat',
    url='https://github.com/kimia-lat/chilean_rut',
    license='KSL',
    keywords = ["rut", "run", "chile", "chilean","pydantic"]
)
