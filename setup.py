from setuptools import setup, find_packages

setup(
    name = "BBSWM",
    version = "v0.3.1",
    description = "BBSWM-_B_lock für _B_lock _S_erver _W_ork _M_anager. Now with UI styling(extended support following)!",
    author = "Konrad",
    author_email = "konrad.spicker@gmx.de",
    url = "https://github.com/konrad/BBSWM",
    packages = find_packages(),
    install_requires = ["tk",
                        "desktop-notifier" ],
    python_requires = ">=3.6",
    entry_points = {"main": ["BBSWM = BBSWM.main:main"]},
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: All Rights Reserved",
        "Intended Audience :: Minecraft admins"
    ]
    )