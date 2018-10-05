import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tfe_backup",
    version="0.0.1",
    author="Dave Arnold",
    author_email="dave@happypathway.com",
    description="Utilties for backing up TFE Workspaces as Terraform Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HappyPathway/TFE_WorkspaceBackup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
