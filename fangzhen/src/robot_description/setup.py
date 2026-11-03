from setuptools import find_packages, setup
from glob import glob

package_name = "robot_description"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        # launch
        ("share/" + package_name + "/launch", glob("launch/*.py")),
        # world
        ("share/" + package_name + "/world", glob("world/*.sdf")),
        # ========== 只保留这一行urdf！递归复制urdf下所有子目录所有xacro/urdf ==========
        ("share/" + package_name + "/urdf", glob("urdf/**/*.xacro", recursive=True)),
        ("share/" + package_name + "/urdf", glob("urdf/**/*.urdf", recursive=True)),
        ("share/" + package_name + "/config", ["config/controllers.yaml"]),
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
        "console_scripts": [],
    },
)
