from distutils.core import setup
import os.path
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ViralApi",
    packages=setuptools.find_packages(),
    version="8.0.0",
    license="MIT",
    description="Viral API: unofficial TikTok.com wrapper for Python.",
    author="Viralway",
    url="https://github.com/Viralway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/Viralway",
    keywords=["viral-api", "tiktok", "python3", "api", "unofficial"],
    install_requires=[
        "requests>=2.31.0,<3.0",
        "playwright>=1.36.0,<2.0",
        "httpx>=0.27.0,<1.0",
        "proxyproviders>=0.2.1,<0.3.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.9",
)
