from setuptools import setup, find_packages

__version__ = "0.1"

setup(
    name="data_subscriptions",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-restful",
        "flask-migrate",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": ["data_subscriptions = data_subscriptions.manage:cli"]
    },
)
