from setuptools import setup, find_namespace_packages

setup(
   # name="clean_folder",
    #version="0.1",
    #url="https://github.com/Gaveloshpom/Sort.py.git0",
    #author="Ruslan Kyiv",
    #author_email="examplePost1@example.com",
    #license="MIT",
    #packages=find_namespace_packages(),
    #install_requires=[],
    #entry_points= {'console_scripts': ['start_PLS = clean_folder:start_function']}
    name="clean_folder",
    version="1.0",
    entry_points={"console_scripts": ["clean-folder=clean_folder.clean:main"],},
    zip_safe=False,
    packages=find_namespace_packages(),
    include_package_data=True,
    description="Test",

)

