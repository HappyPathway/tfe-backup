import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tfe_backup",
    version="2.0.0",
    author="Dave Arnold",
    author_email="dave@happypathway.com",
    description="Utilties for backing up TFE Workspaces as Terraform Code",
    install_requires = ["requests", "jinja2"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HappyPathway/TFE_WorkspaceBackup",
    scripts=['tfe_backup/tfe-backup'],
    packages=["tfe_backup"],
    package_data={
      'tfe_backup': [
          "lib/templates/undefined_vars.j2",
          "lib/templates/workspace.j2",
          "lib/templates/workspace_vars.j2"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
