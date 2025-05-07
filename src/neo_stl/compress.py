import os
import argparse
import tqdm
import open3d


def compress(input_path, output_path, target_triangles):
    # check input path is folder or file
    if os.path.isdir(input_path):
        # If input path is a directory, get all STL files in the directory
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith(".stl")]
    else:
        # If input path is a file, use it directly
        files = [input_path]

    # check output path exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # get files info (len extra.)
    total_files = len(files)
    print(f"Total files: {total_files}")

    progress_per_file = 100 / total_files

    for i, file_path in enumerate(files):
        mesh = open3d.io.read_triangle_mesh(file_path)

        simplified_mesh = mesh.simplify_quadric_decimation(target_triangles)
        simplified_mesh.compute_triangle_normals()
        simplified_mesh.compute_vertex_normals()

        output_file_path = os.path.join(output_path, os.path.basename(file_path))
        open3d.io.write_triangle_mesh(output_file_path, simplified_mesh)


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description="STL Compressor")
    parser.add_argument("--input", type=str, required=True, help="Path to the input STL files.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output directory.")
    parser.add_argument("--target_triangles", type=int, default=1000, help="Target number of triangles.")

    # parse the arguments
    args = parser.parse_args()

    # check if the input path exists
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input path {args.input} does not exist.")

    # check if the output path exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # compress the STL files
    compress(args.input, args.output, args.target_triangles)
