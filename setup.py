import setuptools


def parse_requirements(filename, session=None):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdfservices-extract-sdk",
    version="1.0.0-beta1",
    author='Adobe Document Services',
    author_email='extractapi@adobe.com',
    license='Apache2',
    description="Adobe Document Services Extract PDF API Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://opensource.adobe.com/pdftools-sdk-docs/beta/extract/index.html#",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    python_requires=">=3.6",
    install_requires=parse_requirements('requirements.txt', session=False),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
