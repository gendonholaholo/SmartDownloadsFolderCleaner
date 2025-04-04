from setuptools import setup, find_packages

setup(
    name="dropclear",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
        "tqdm>=4.65.0",
        "thefuzz>=0.19.0",
        "python-Levenshtein>=0.21.1",
        "pyinstaller>=5.13.0"
    ],
    entry_points={
        'console_scripts': [
            'dropclear=dropclear:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Smart CLI Cleaner for Windows Downloads Folder",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="file-management, cleanup, downloads, windows",
    url="https://github.com/yourusername/dropclear",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
) 