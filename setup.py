from setuptools import find_packages, setup

setup(
    name="Lupr",
    version="v1.4",
    description="Lup recorder",
    long_description=README,
    long_description_content_type='text/markdown',
    author="azzamsa",
    author_email="azzam@azzamsa.com",
    url="https://gitlab.com/azzamsa/lupr",
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['lupr=lupr.__main__'],
    },
    install_requires=["GitPython==2.1.8", "PyQt5==5.11.3"],
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
