from setuptools import setup, find_packages

 # Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
     long_description = fh.read()

 # Read the contents of the requirements.txt file
with open('requirements.txt') as f:
     requirements = f.read().splitlines()

setup(
     name="sql_database_utils",
     version="0.2.0",
     author="Sim Yi Xuan",
     description="Utility functions for reading tables from SQL Server",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="",
     project_urls={},
     classifiers=[
         "Development Status :: Development",
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
         "Topic :: Benchmarking",
         "License :: OSI Approved :: MIT License",
     ],
     python_requires=">=3.10",
     install_requires=requirements
 )