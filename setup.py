from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="starpay-ethiopia",
    version="0.1.2",
    description="Unofficial Python client for the StarPay API (Ethiopia)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="StarPay Ethiopia / Community",
    author_email="developer@starpayethiopia.com",
    url="https://github.com/dinkadereje/starpay-python",
    packages=find_packages(),
    install_requires=[],
    keywords=["starpay", "payment", "ethiopia", "api", "gateway"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
