import setuptools

setuptools.setup(
    name='prompt_chat',
    version='1.0',
    author='yuval cohen',
    description='terminal chat server and client ',
    long_description='you can create multiple clients and chat between then , just remember to run server',
    keywords='development, setup, setuptools',
    python_requires='>=3.7, <4',
    packages=setuptools.find_packages()
)