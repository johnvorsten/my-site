## Managing packages and planning for deployment
## Using conda for development, and virtualenv, pipenv, or Docker for production
See [this article](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/) and [a blog from anaconda](https://www.anaconda.com/blog/using-pip-in-a-conda-environment) for a good discussion on common mistakes and misconceptions on using conda with pip.  The advice from this article form the instructions below:
1. Use pip ONLY after all 'other' requirements have been installed with conda
2. Additionally, pip should be run with the “--upgrade-strategy only-if-needed” argument to prevent packages installed via conda from being upgraded unnecessarily. This is the default when running pip but it should not be changed.
3. Use a purpose-built conda environment to protect other environments
4. Do NOT use pip in the root conda environment (base)
5. Store conda and pip requirements in text files

The general problem is that if pip makes changes to conda-installed packages, then conda will not know about these changes.  Conda may make changes that breaks the environment.  This is why you should first install necessary dependencies that are only available to conda (actually, conda recommends installing as many dependencies as possible with conda), and then install everything else with pip

### Workflow, development computer:
1. Create a conda environment backup (if you have an environment already) `conda env export > environment.yml`

2. Create environment through conda with --file (on development computer) like `conda create --name django --file ./path/environment.yml` 

3. OR create a new/blank environment `conda create --name django python=3.7` and install pip packages after

### Workflow, Deployment/production computer:
1. Create a pip requirements file (if you have an environment already) `pip list --format=freeze > requirements.txt` [see this](https://stackoverflow.com/questions/64500342/creating-requirements-txt-in-pip-compatible-format-in-a-conda-virtual-environmen)
    1. Clean up the pip environment backup
2. Install packages in environment with --requirement (only on deployment, conda will install pip packages from environment.yml file)