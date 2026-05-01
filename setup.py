from setuptools import setup, find_packages

setup(
    name="Raven",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "raven.data": ["samples.json", "templates.json"],
    },
    install_requires=["numpy", "scikit-learn"],
    entry_points={
        "console_scripts": [
            "raven=raven.cli:main",
        ],
    },
    description="Command synthesis from intent",
    author="0xf0xy",
    license="MIT",
)
