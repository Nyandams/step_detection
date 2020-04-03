import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="escalator-nyandams",
    version="0.0.1",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Damien Lecha",
    author_email="lecha.damien@gmail.com",
    description="A small package to detect stagnation in the values of a signal, sort of horizontal steps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nyandams/step_detection",
    packages=setuptools.find_packages(exclude=['tests', 'images']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
