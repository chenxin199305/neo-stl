import os
import argparse
import open3d

from neo_stl.compress_open3d import compress_open3d
from neo_stl.compress_fastsimp import compress_fastsimp


def compress(
        input_path,
        output_path,
        target_triangle_count=None,
        target_reduce_ratio=None,
        max_mesh_file_size=None,
        min_mesh_triangle_count=None,
) -> None:
    """

    :param input_path:
    :param output_path:
    :param target_triangle_count:
    :param max_mesh_file_size:
    :param min_mesh_triangle_count:
    :return None:
    """

    # check input path is folder
    if os.path.isdir(input_path):
        # If input path is a directory, get all STL files in the directory
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith(".stl")]
    else:
        raise FileNotFoundError(f"{input_path} is not a directory")

    # check output path is folder
    if os.path.isdir(output_path):
        pass
    else:
        raise FileNotFoundError(f"{output_path} is not a directory")

    # create output path if not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # get files info (len extra.)
    total_files = len(files)
    print(f"Total files: {total_files}")

    for i, file_path in enumerate(files):
        compress_open3d(
            file_path=file_path,
            output_dir_path=output_path,
            target_reduce_ratio=target_reduce_ratio,
            target_triangle_count=target_triangle_count,
        )


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description="STL Compressor")
    parser.add_argument("--input", type=str, required=True, help="Path to the input folder contains STL files.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output folder.")
    parser.add_argument("--target_triangle", type=int, default=None, help="Target number of triangles.")
    parser.add_argument("--reduce_ratio", type=float, default=None, help="Target reduce ratio.")
    parser.add_argument("--max_mesh_file_size", type=float, default=None, help="Max mesh file size in MB.")
    parser.add_argument("--min_mesh_triangle_count", type=int, default=None, help="Min mesh triangle count.")

    # parse the arguments
    args = parser.parse_args()

    # check if input and output are folder paths
    if not os.path.isdir(args.input):
        raise ValueError(f"Input path {args.input} is not a directory.")

    if not os.path.isdir(args.output):
        raise ValueError(f"Output path {args.output} is not a directory.")

    # check if the input path exists
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input path {args.input} does not exist.")

    # check if the output path exists
    # - if not exist, create the folder
    # - if exist, remove the folder content
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    else:
        # remove the folder content
        for f in os.listdir(args.output):
            file_path = os.path.join(args.output, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                raise FileNotFoundError(f"Output path {args.output} is not a directory.")

    # compress the STL files
    compress(
        input_path=args.input,
        output_path=args.output,
        target_triangle_count=args.target_triangle,
        target_reduce_ratio=args.reduce_ratio,
        max_mesh_file_size=args.max_mesh_file_size,
        min_mesh_triangle_count=args.min_mesh_triangle_count,
    )
