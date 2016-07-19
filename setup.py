from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='neverbounce',
    version='0.1.0',
    author='Martin Kosír',
    author_email='martin@martinkosir.net',
    packages=['neverbounce'],
    url='https://github.com/martinkosir/neverbounce-python',
    license='MIT',
    description='NeverBounce Python API client',
    long_description=readme,
    install_requires=['requests>=2.9.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
