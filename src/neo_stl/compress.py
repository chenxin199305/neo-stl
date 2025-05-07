import os
import argparse
import tqdm
import open3d


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
        mesh = open3d.io.read_triangle_mesh(file_path)

        # --------------------------------------------------
        # Auto Resize Mesh Size

        # get current mesh file size
        current_mesh_file_size = os.path.getsize(file_path) / (1024 * 1024)  # in MB

        # get current mesh triangle count
        current_mesh_triangle_count = len(mesh.triangles)

        # check if mesh file is small enough, if so, skip
        if max_mesh_file_size is None:
            max_mesh_file_size = 1.  # in MB

        if current_mesh_file_size < max_mesh_file_size:
            print(f"File {file_path} is small enough, skipping...")
            continue

        # check if mesh triangle count is small enough, if so, skip
        if min_mesh_triangle_count is None:
            min_mesh_triangle_count = 1000

        if current_mesh_triangle_count < min_mesh_triangle_count:
            print(f"File {file_path} is small enough, skipping...")
            continue

        # --------------------------------------------------
        # Two Factors affect the resize process
        simplified_mesh_triangle_count = 0

        if target_reduce_ratio is None:
            target_reduce_ratio = 0.25  # default reduce ratio
        else:
            pass

        simplified_mesh_triangle_count = int(target_reduce_ratio * current_mesh_triangle_count)

        if target_triangle_count is None:
            pass
        else:
            simplified_mesh_triangle_count = int(target_triangle_count)

        print(f"Simplifying {file_path} from {current_mesh_triangle_count} to {simplified_mesh_triangle_count} triangles...")

        # --------------------------------------------------

        simplified_mesh = mesh.simplify_quadric_decimation(simplified_mesh_triangle_count)
        simplified_mesh.compute_triangle_normals()
        simplified_mesh.compute_vertex_normals()

        output_file_path = os.path.join(output_path, os.path.basename(file_path))
        open3d.io.write_triangle_mesh(output_file_path, simplified_mesh)


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
