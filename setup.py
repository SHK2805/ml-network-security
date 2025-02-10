from setuptools import setup, find_packages
from typing import List

# Reading the README file for the long description
def read_readme():
    with open("README.md", "r") as f:
        return f.read()


def read_requirements(file_path: str)->List[str]:
    """
    Reads a requirements.txt file and returns a list of strings,
    each representing a requirement.

    :param file_path: str - Path to the requirements.txt file
    :return: list - List of requirements as strings
    """
    requirements = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and ignore comments
                cleaned_line = line.strip()
                if cleaned_line and not cleaned_line.startswith('#'):
                    requirements.append(cleaned_line)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    h_e = '-e .'
    if h_e in requirements:
        requirements.remove(h_e)

    return requirements

# this will look for __init__ in every folder and install that as a local package
setup(
    name="Network Security",  # project name
    version="0.1.0",  # Initial version of a project
    author="Sri",  # Your name author_email="your.email@example.com", # Your email
    description="This is an end to end machine learning network security project.",  # Short description
    long_description=read_readme(),  # Long description from README file
    long_description_content_type="text/markdown",  # Format of the long description
    packages=find_packages(),  # Automatically find packages in the project
    python_requires='>=3.10',  # Minimum required Python version
    install_requires=read_requirements('requirements.txt')
)