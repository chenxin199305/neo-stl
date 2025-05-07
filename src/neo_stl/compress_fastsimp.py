import os

import pyvista
import fast_simplification


def compress_fastsimp(
        file_path,
        output_dir_path,
        target_reduce_ratio=None,
        target_triangle_count=None,
        max_mesh_file_size=None,
        min_mesh_triangle_count=None,
) -> None:
    print(f"Compressing {file_path}...")

    # .STL -> .stl
    file_path = file_path.replace(".STL", ".stl")

    # 确认文件路径
    input_file_path = file_path
    output_file_path = os.path.join(output_dir_path, os.path.basename(file_path))

    # 确定压缩比
    if target_reduce_ratio is None:
        target_reduce_ratio = 0.30  # default reduce ratio
    else:
        pass

    # 加载原始网格
    mesh = pyvista.read(input_file_path)

    # 简化网格
    simplified_mesh = fast_simplification.simplify_mesh(
        mesh,
        target_reduction=(1 - target_reduce_ratio)
    )

    # 保存简化后的网格
    simplified_mesh.save(output_file_path)
