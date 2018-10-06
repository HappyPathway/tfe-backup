import setuptools
import json

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tfe-backup",
    version="10.0.1",
    author="HappyPathway",
    author_email="info@happypathway.com",
    description="Utilties for backing up TFE Workspace Configurations as Terraform Code",
    install_requires = [
        "requests", 
        "jinja2",
        "pyhcl"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HappyPathway/tfe-backup",
    scripts=[
        'scripts/tfe-backup',
        'scripts/tfe-oauth-tokens'
    ],
    packages=[
        "tfe_backup"
    ],
    py_modules=[
        "tfe_backup.workspace",
        "tfe_backup.workspace_variables"
    ],
    package_data={
      'tfe_backup': [
          "templates/undefined_vars.j2",
          "templates/workspace.j2",
          "templates/workspace_vars.j2",
          "templates/team_access.j2"
        ],
    },
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
