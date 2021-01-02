import glob
import os

from Geometry import *


def write_step_file(out_file, assets_path, lines, triangles, quads):
    """
    writes a .obj file containing one step
    @param out_file: file name
    @param assets_path: path to write to
    @param lines: list of lines
    @param triangles: list of triangles
    @param quads: list of quads
    """

    if out_file.endswith(".ldr"):
        out_file = out_file.replace(".ldr", ".obj")
    print("write file " + out_file)

    # lf = open(os.path.join(assets_path, out_file[:-4] + "_lines.txt"), "w")
    with open(os.path.join(assets_path, out_file), "w") as f:
        f.write("mtllib colors.mtl\n")
        # f.write("# " + str(len(lines)) + " Lines\n")
        old_color = Color(0)

        # writing line file, not efficient for unity step rn
        # for line in lines:
        #     if line.color == old_color:
        #         color = ""
        #     else:
        #         color = "usemtl " + str(line.color)
        #         old_color = line.color
        #
        #     p1 = line.p1
        #     p2 = line.p2
        #     # p3 = (p1+p2)/2.0
        #
        #     # out_line = color + "\nv " + str(p1) + "\nv " + str(p2) + "\nv " + str(p3) + \
        #     #            "\nf -1 -2 -3\nf -3 -2 -1\n\n"
        #     out_line = "v " + str(round(p1)) + "\nv " + str(round(p2)) + "\nl -1 -2\n"
        #     lf.write(out_line)
        #     lf.flush()

        # write all the triangles
        f.write("# " + str(len(triangles)) + " Triangles\n")
        for tri in triangles:
            if tri.color == old_color:
                color = "usemtl " + str(old_color)
            else:
                color = "usemtl " + str(tri.color)
                old_color = tri.color

            p1 = tri.p1
            p2 = tri.p2
            p3 = tri.p3

            out_line = color + "\nv " + str(p1) + "\nv " + str(p2) + "\nv " + str(p3) + \
                       "\nf -1 -2 -3\nf -3 -2 -1\n\n"
            f.write(out_line)
            f.flush()

        # write all the quads
        f.write("# " + str(len(quads)) + " Quads\n")
        for quad in quads:
            if quad.color == old_color:
                color = "usemtl " + str(old_color)
            else:
                color = "usemtl " + str(quad.color)
                old_color = quad.color

            p1 = quad.p1
            p2 = quad.p2
            p3 = quad.p3
            p4 = quad.p4

            out_line = color + "\nv " + str(p1) + "\nv " + str(p2) + "\nv " + str(p3) + "\nv " + str(p4) + \
                       "\nf -1 -2 -3 -4\nf -4 -3 -2 -1\n\n"
            f.write(out_line)
            f.flush()

    # lf.close()


def write_file(model_name, assets_path):
    """
    writes file that contains the whole model by merging all step files
    @param model_name: name of the mode
    @param assets_path: path to ile lovation
    @return:
    """
    step_filenames = glob.glob(os.path.join(assets_path, model_name + "_step*.obj"))
    # lines_filenames = glob.glob(os.path.join(assets_path, model_name + "_step*_lines.txt"))

    # joining .obj files
    with open(os.path.join(assets_path, model_name + ".obj"), "w") as f:
        f.write("mtllib colors.mtl\n")
        for fname in step_filenames:
            with open(fname) as infile:
                for line in infile:
                    f.write(line)

    # joining lines
    # with open(os.path.join(assets_path, model_name + "_lines.txt"), "w") as f:
    #     f.write("mtllib colors.mtl\n")
    #     for fname in lines_filenames:
    #         with open(fname) as infile:
    #             for line in infile:
    #                 f.write(line)


def write_step_info(out_file, assets_path, bricks):
    """
    writes the brick names used per step to a file
    @param out_file: name of file
    @param assets_path: path of file
    @param bricks: list of bricks per step
    """
    steps = len(bricks)

    with open(os.path.join(assets_path, out_file), "w") as f:
        f.write("# STEPS " + str(steps))
        i = 0
        for step in bricks:
            f.write("\ns " + str(i))
            for brick in step:
                f.write("\nb " + brick)
            i += 1


def write_color_mtl(assets_path):
    """
    writes a .mtl file containing the rgb values about all the colors used (based on ldraw)
    @param assets_path: path to write the file to
    """
    filename = os.path.join(assets_path, "colors.mtl")

    # if os.path.isfile(filename):
    #     return 0

    colors = {("default", 0.0, 0.0, 0.0),
              ("zero", 0.11, 0.16, 0.2),
              ("one", 0.12, 0.35, 0.66),
              ("two", 0.0, 0.52, 0.17),
              ("three", 0.02, 0.62, 0.62),
              ("four", 0.71, 0.0, 0.0),
              ("five", 0.83, 0.21, 0.62),
              ("six", 0.33, 0.2, 0.14),
              ("seven", 0.54, 0.57, 0.55),
              ("eight", 0.33, 0.35, 0.33),
              ("nine", 0.59, 0.8, 0.85),
              ("ten", 0.35, 0.67, 0.25),
              ("eleven", 0.0, 0.67, 0.64),
              ("twelve", 0.94, 0.43, 0.38),
              ("thirteen", 0.96, 0.66, 0.73),
              ("fourteen", 0.98, 0.78, 0.04),
              ("fifteen", 0.96, 0.96, 0.96),
              ("seventeen", 0.68, 0.85, 0.66),
              ("eighteen", 1.0, 0.84, 0.5),
              ("nineteen", 0.69, 0.63, 0.44),
              ("twenty", 0.69, 0.75, 0.84),
              ("twentyone", 0.88, 1.0, 0.69),
              ("twentytwo", 0.4, 0.12, 0.51),
              ("twentythree", 0.05, 0.24, 0.6),
              ("twentyfive", 0.84, 0.47, 0.14),
              ("twentysix", 0.56, 0.12, 0.46),
              ("twentyseven", 0.65, 0.79, 0.09),
              ("twentyeight", 0.54, 0.49, 0.38),
              ("twentynine", 1.0, 0.62, 0.8),
              ("thirty", 0.63, 0.43, 0.73),
              ("thirdone", 0.8, 0.64, 0.87),
              ("thirtytwo", 0.0, 0.0, 0.0),
              ("thirtythree", 0.0, 0.13, 0.63),
              ("thirtyfour", 0.14, 0.47, 0.25),
              ("thirtyfive", 0.34, 0.9, 0.27),
              ("thirtysix", 0.79, 0.1, 0.04),
              ("thirtyseven", 0.87, 0.4, 0.58),
              ("thirtyeight", 1.0, 0.5, 0.05),
              ("thirdynine", 0.76, 0.87, 0.94),
              ("forty", 0.39, 0.37, 0.32),
              ("fortyone", 0.33, 0.6, 0.72),
              ("fortytwo", 0.75, 1.0, 0.0),
              ("fortythree", 0.68, 0.91, 0.94),
              ("fortyfour", 0.59, 0.44, 0.62),
              ("fortyfive", 0.99, 0.59, 0.67),
              ("fortysix", 0.96, 0.8, 0.18),
              ("fortyseven", 0.99, 0.99, 0.99),
              ("seventyone", 0.59, 0.59, 0.59),
              ("threeeighttree", 0.81, 0.81, 0.81)
              }

    with open(filename, "w") as f:
        for color in colors:
            f.write("newmtl " + str(color[0]) + "\n")
            f.write("Ka " + str(color[1]) + " " + str(color[2]) + " " + str(color[3]) + "\n")
            f.write("Kd " + str(color[1]) + " " + str(color[2]) + " " + str(color[3]) + "\n")
            f.write("illum 1\n\n")
            f.flush()
