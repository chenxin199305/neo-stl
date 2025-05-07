# neo-stl

STL tool, command tool of the Neo project

## Setup

Setup the environment

```bash
# Create a conda environment
conda create -n neo-stl python=3.11

# Activate the conda environment
conda activate neo-stl

# Install the requirements
pip install -e .
```

## Usage

Use the neo-stl tool to compress certain STL file or files.

```bash
python -m neo_stl.compress \
--input <input_file / intput_folder> \
--output <output_file / output_folder> \
[--target_triangles <target_triangles>] 
```

## Thanks

- [stl_compressor](https://github.com/fan-ziqi/stl_compressor)