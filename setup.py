from setuptools import setup, find_packages

setup(
    name="my-python-app",          # Name of your app
    version="1.0",                 # Version number
    packages=find_packages(where="src"),  # Automatically find all packages in `src`
    package_dir={"": "src"},       # Define `src` as the package root
    py_modules=["main"],           # Include `main.py` as a module
    install_requires=[             # Dependencies for your app
        "supabase",
    ],
    entry_points={
        "console_scripts": [
            "aktien-datenbank = main:main",  # Maps `myapp` command to `main()` in `src/main.py`
        ],
    },
)
