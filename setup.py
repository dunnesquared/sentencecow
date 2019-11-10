import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="sentencecow",
        version="0.1.0",
        author="Alexander Dunne",
        author_email="alexdunne@gmail.com",
        description="Sentence extractor and word counter",
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="MIT",
        url="https://github.com/dunnesquared/sentencecow",
        packages=setuptools.find_packages(),
    	install_requires=["flask",],
    	test_suite='nose.collector',
    	tests_require=['nose'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        include_package_data=True,
    )
