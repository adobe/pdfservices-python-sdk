import setuptools


def parse_requirements(filename, session=None):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdfservices-sdk",
    version="2.3.0",
    author='Adobe Document Services',
    author_email='extractapi@adobe.com',
    license='Apache2',
    description="Adobe PDFServices Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.adobe.com/go/pdftoolsapi_doc",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    python_requires=">=3.6",
    install_requires=parse_requirements('requirements.txt', session=False),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
