import royalpack.version
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = [line for line in f.readlines() if not line.startswith("#")]

setuptools.setup(
    name="royalpack",
    version=royalpack.version.semantic,
    author="Stefano Pigozzi",
    author_email="ste.pigozzi@gmail.com",
    description="A Royalnet Pack for the Royal Games community",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/royalpack",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Database",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License"
    ],
    dependency_links=["https://github.com/Rapptz/discord.py/tarball/master"],
    include_package_data=True,
    zip_safe=False
)
