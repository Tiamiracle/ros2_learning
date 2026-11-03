from setuptools import find_packages, setup
import os
from glob import glob

package_name = "face_detect"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "resource"), glob("resource/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="3197751933@qq.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "face_server = face_detect.face_server:main",
            "face_client = face_detect.face_client:main",
            "face_servertest=face_detect.face_servertest:main",
        ],
    },
)
