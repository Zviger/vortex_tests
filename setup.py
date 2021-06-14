import setuptools

import app

setuptools.setup(
    name=app.app_name,
    version=app.__version__,
    author="Budzich Maxim",
    url="https://github.com/Zviger/vortex_tests",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["vortex_ts=app.vortex_ts:main"],
    }
)
