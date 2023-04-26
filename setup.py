from setuptools import setup, find_packages

setup(
    name="promptest",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "PyYAML",
        "pyllamacpp"
    ],
    entry_points={
        "console_scripts": [
            "promptest=promptest.main:main",
        ]
    },
)
