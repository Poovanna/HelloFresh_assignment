# Table of contents: 
1. [Description](#recepies)
2. [Project Organization](#project_organization)
3. [Usage](#usage)

# Recepies
This repository contains a script to download data from the given URL holding recipe data. 
It then filters it based on a givien ingredient - chilies by default for now
It then can parse the total time taken for the preparations of the filtered recipes,
and then rate the difficulty based on the time taken for both the prep as well as the cooking.
This filtered and labelled data is then stpored in a file.
Next, the average time for each classification of difficulty is calculated and saved in a separate file.

# Project Organization
    ├── hf_bi_python_exercise
    |   └── recipes_etl             <- Base folder of the source code in this project
    |   |   └── recipeFilter.py     <- Source code for Recipe match and filtering
    |   |   └── __init__.py         <- Makes the folder a Python module
    |   |   └── utils.py            <- Common utility methods 
    |   └── tests                   <- Unitests directory
    |   └── main.py                 <- Entry point to the project             
    ├── Pipfile                     <- Specification for the project
    └── Pipfile.lock                <- Package information and version log

# Usage

### Initial setup

1. Clone the repository to a local directory.
    
    ```
    git clone <repository link>
    ```

2. Install pipenv virtual environment, setup dependencies and activate the environment.
    The pipenv virtual environment tool has been used to setup this project. 
    It helps create a separate enviromnet with the specified python version as well as
    all the packages with given versions for consistent performance across systems.

    This project uses Python 3.12 version and is specified in the pipfile
    This will ensure that the environment created will be 3.12.

    ```
    pip install --user pipenv
    ```   
    This command installs the pipenv tool 
3. Install dependencies.

    ```
    pipenv install
    ```    
    This command installs all dependencies form the piplock file, as per the specified versions.
4. Activate the environment.

    ```
    pipenv shell
    ```    
    Activates the defined python virtual environment


### Run
1. Now that you have a suitable Python environment,run the code:

    ```
    python hf_bi_python_excercise/main.py
    ```

### Tests
1. With the pytest setup in the project, all the defined tests can be run with the command:

    ```
    pytest
    ```
    This command must be run from the root directory of the project.

