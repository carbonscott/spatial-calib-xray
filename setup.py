import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spatial_calib_xray",
    version="0.1.1",
    author="Cong Wang",
    author_email="wangimagine@gmail.com",
    description="Spatial calibration of small and wide angle X-ray scattering/diffraction data by fitting circles. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carbonscott/spatial-calib-xray",
    keywords = ['Spatial calibration', 'X-ray', 'Circle', 'Fitting'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
