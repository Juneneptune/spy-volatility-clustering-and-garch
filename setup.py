from setuptools import setup, find_packages

setup(
    name="spy-volatility",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "yfinance",
        "pyyaml",
        "matplotlib",
        "seaborn",
        "scipy",
    ],
    python_requires=">=3.8",
)

