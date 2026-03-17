from setuptools import setup, Extension
import pybind11

ext = Extension(
    'last_deque_stl',
    sources=['deque_stl.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
    extra_compile_args=['-std=c++11', '-O2'],
    extra_link_args=[
        '-static-libgcc',
        '-static-libstdc++',
    ],
)

setup(
    name='last_deque_stl',
    version='1.0.0',
    ext_modules=[ext],
)