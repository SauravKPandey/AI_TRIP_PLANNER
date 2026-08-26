from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """this fn will return the list of requirements."""
    requirement_list = []

    try:
        with open('requirements.txt') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    return requirement_list
#print(get_requirements('requirements.txt'))
setup(
    name="AI_TRIP_PLANNER",
    version="0.0.1",
    author="Saurav Pandey",
    author_email="sauravpandey.sag@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')   
) 