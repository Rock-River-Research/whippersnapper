from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    author="Kyle Johnson",
    author_email="gkjohns@gmail.com",
    description="An AI-powered data analysis tool that lets you talk to pandas",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Rock-River-Research/whippersnapper/e",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        # List your package dependencies here, e.g., "numpy>=1.18.0",
    ],
    python_requires='>=3.8',
)
