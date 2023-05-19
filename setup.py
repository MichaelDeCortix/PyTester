from setuptools import setup, find_packages

setup(
    name='pyTester',
    version='0.1.0',
    url='https://github.com/MichaelDeCortix/pyTester',
    author='MiDeCo',
    author_email='@gmail.com',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=[
        'ipywidgets >= 7.5.1', 
        'pyperclip >= 1.8.2', 
        'IPython >= 7.16.1',
        'psycopg2 >= 2.8.6', 
        'cx_Oracle >= 8.1.0',
        'requests >= 2.25.1', 
        'rich >= 10.1.0', 
        'curlify >= 2.2.1'
    ],  # Optional
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
