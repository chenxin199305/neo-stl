import os
import open3d

from neo_stl.simplify_open3d import (
    simplify,
    simplify_smooth,
)


def compress_open3d(
        file_path,
        output_dir_path,
        target_reduce_ratio=None,
        target_triangle_count=None,
        max_mesh_file_size=None,
        min_mesh_triangle_count=None,
) -> None:
    mesh = open3d.io.read_triangle_mesh(file_path)

    # --------------------------------------------------
    # Auto Resize Mesh Size

    # get current mesh file size
    current_mesh_file_size = os.path.getsize(file_path) / (1024 * 1024)  # in MB

    # get current mesh triangle count
    current_mesh_triangle_count = len(mesh.triangles)

    # check if mesh file is small enough, if so, skip
    if max_mesh_file_size is None:
        max_mesh_file_size = 1.0  # in MB

    if current_mesh_file_size < max_mesh_file_size:
        print(f"File {file_path} is small enough, larger the reduction ratio...")
        target_reduce_ratio = 0.75

    if current_mesh_file_size < 1.0:  # 1MB
        print(f"File {file_path} is small enough, larger the reduction ratio...")
        target_reduce_ratio = 1.0

    # check if mesh triangle count is small enough, if so, skip
    if min_mesh_triangle_count is None:
        min_mesh_triangle_count = 1000

    if current_mesh_triangle_count < min_mesh_triangle_count:
        print(f"File {file_path} is small enough, larger the reduction ratio...")
        target_reduce_ratio = 1.0

    # --------------------------------------------------
    # Two Factors affect the resize process
    simplified_mesh_triangle_count = 0

    if target_reduce_ratio is None:
        target_reduce_ratio = 0.30  # default reduce ratio
    else:
        pass

    simplified_mesh_triangle_count = int(target_reduce_ratio * current_mesh_triangle_count)

    if target_triangle_count is None:
        pass
    else:
        simplified_mesh_triangle_count = int(target_triangle_count)

    print(f"Simplifying {file_path} from {current_mesh_triangle_count} to {simplified_mesh_triangle_count} triangles...")

    # --------------------------------------------------

    simplified_mesh = simplify(
        mesh=mesh,
        target_triangles=simplified_mesh_triangle_count,
    )

    # --------------------------------------------------
    # Store the simplified mesh

    output_file_path = os.path.join(output_dir_path, os.path.basename(file_path))
    open3d.io.write_triangle_mesh(output_file_path, simplified_mesh)
