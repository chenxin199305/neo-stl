import numpy
import open3d
import trimesh

from open3d import geometry, utility


def simplify(
        mesh,
        target_triangles,
):
    """
    :param mesh:
    :param target_triangles:
    :return:
    """
    simplified = mesh.simplify_quadric_decimation(
        target_number_of_triangles=target_triangles,
        maximum_error=0.1,  # 较小的值保留更多细节
        boundary_weight=10.0  # 增加边界权重
    )
    simplified.compute_triangle_normals()
    simplified.compute_vertex_normals()

    return simplified


# ----------------------------------------------------------------------------------------------------

def progressive_simplify(mesh, target, steps=3):
    current = len(mesh.triangles)

    for _ in range(steps):
        ratio = 1 - (1 - (target / current)) / (steps - _)
        step_target = max(target, int(current * ratio))
        mesh = mesh.simplify_quadric_decimation(step_target)

    return mesh


def filter_smooth(mesh):
    mesh = mesh.filter_smooth_taubin(
        number_of_iterations=5,  # 迭代次数
    )

    return mesh


def fill_holes(mesh):
    """
    :param mesh:
    :return:
    """
    tri_mesh = trimesh.Trimesh(
        vertices=numpy.asarray(mesh.vertices),
        faces=numpy.asarray(mesh.triangles)
    )
    tri_mesh.fill_holes()
    simplified = geometry.TriangleMesh(
        utility.Vector3dVector(tri_mesh.vertices),
        utility.Vector3iVector(tri_mesh.faces)
    )

    return simplified


def simplify_smooth(
        mesh,
        target_triangles,
):
    """
    :param mesh:
    :param target_triangles:
    :return:
    """
    # 预处理
    mesh.remove_non_manifold_edges()
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.remove_unreferenced_vertices()

    simplified = mesh

    # 分阶段简化
    simplified = progressive_simplify(simplified, target_triangles)

    # 后处理平滑
    # simplified = filter_smooth(simplified)

    # 填充孔洞
    # simplified = fill_holes(simplified)

    simplified.compute_triangle_normals()
    simplified.compute_vertex_normals()

    return simplified
