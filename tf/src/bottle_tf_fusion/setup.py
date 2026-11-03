from setuptools import find_packages, setup

package_name = "bottle_tf_fusion"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
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
            "static_cam_tf = bottle_tf_fusion.static_tf_publisher:main",
            "bottle_receiver = bottle_tf_fusion.bottle_receiver:main",
            "bottle_tf_calculator = bottle_tf_fusion.bottle_tf_calculator:main",
        ],
    },
)
