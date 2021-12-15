import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ratools",
    version="0.0.4",
    author="Lukas Raab",
    author_email="lukas.raab@contifoam.com",
    description="Ra-Toolbox to improve common tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MisterPresident/ratools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "keepassxc-browser",
        "beautifulsoup4",
        "tqdm"
    ],
)
