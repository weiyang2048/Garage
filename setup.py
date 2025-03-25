from setuptools import setup, find_packages

setup(
    name="AppliedDataScience",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "sweetviz",
        "ydata-profiling",
    ],
    author="Wei Yang",
    author_email="weiyang2048@gmail.com",
    description="A collection of applied data science projects and analyses",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/applied_data_science",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 