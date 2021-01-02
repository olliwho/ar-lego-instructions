import os
import re

from Brick import Brick
from Geometry import *


def parse_manual(path, translation=None):
    """
    parses a file that consists of step for step adding of new bricks
    @param translation: translation matrix in case we are dealing with an mpd file
    @param path: path to instruction file
    @return: nested lists of bricks that get added step per step
    """
    bricks_per_step = []
    bricks = []

    with open(path) as f:
        fline = f.readline().replace('\t', ' ')
        while fline:
            fline = re.sub(' +', ' ', fline).strip()
            if fline.startswith('0'):
                # comments or meta comments, like a new step
                val = [i for i in fline.split(' ')]
                if val[1] == 'STEP':
                    bricks_per_step.append(bricks)
                    bricks = []
            elif fline.startswith('1'):
                # checks for brick files and makes bricks out of it
                val = [float(i) for i in fline.split(' ')[:14]]
                model_file = " ".join(fline.split(' ')[14:]).replace('\\', '/')
                color = Color(int(val[1]))
                position = Point(val[2], val[3], val[4])
                orientation = Matrix4x4(val[5], val[6], val[7], position.x,
                                     val[8], val[9], val[10], position.y,
                                     val[11], val[12], val[13], position.z,
                                     0.0, 0.0, 0.0, 1.0)
                if translation:
                    # in case we are dealing with .mpd files
                    orientation = translation * orientation
                else:
                    # all the models are weirdly upside down so we fix that
                    orientation = orientation.rotate()
                new_brick = Brick(color, position, orientation, model_file)
                bricks.append(new_brick)
            fline = f.readline().replace('\t', ' ')

    bricks_per_step.append(bricks)

    if not bricks_per_step[-1]:
        bricks_per_step.pop(-1)
    return bricks_per_step


def parse_brick(m_path, translation_matrix, old_color):
    """
    parses a brick file
    @param m_path: path to file
    @param translation_matrix: translation matrix for all points, from given orientation
    @param old_color: color defined in the file line
    @return: list of lines, triangles, quads and bricks that where parsed from the file
    """
    print("parse brick " + m_path)
    lines = []
    triangles = []
    quads = []
    bricks = []

    # checking if file path to parse is ok
    if not m_path.endswith(".ldr"):
        m_path = m_path.lower()
    path = "../parts/" + m_path
    if not os.path.isfile(path):
        path = "../models/" + m_path
    if not os.path.isfile(path):
        print("Error, could not find file " + m_path)
        return lines, triangles, quads, bricks

    with open(path) as f:
        fline = f.readline().replace('\t', ' ')
        while fline:
            fline = re.sub(' +', ' ', fline).strip()

            if fline.startswith('0') or not fline:
                # comments or meta comments
                pass
            elif fline.startswith('1'):
                # checks for new bricks
                val = [float(i) for i in fline.split(' ')[:14]]
                model_file = " ".join(fline.split(' ')[14:]).replace('\\', '/')
                color = int(val[1])
                if color == 16:
                    color = old_color
                else:
                    color = Color(color)
                position = Point(val[2], val[3], val[4])
                orientation = Matrix4x4(val[5], val[6], val[7], position.x,
                                        val[8], val[9], val[10], position.y,
                                        val[11], val[12], val[13], position.z,
                                        0.0, 0.0, 0.0, 1.0)
                orientation = translation_matrix * orientation
                new_brick = Brick(color, position, orientation, model_file)
                bricks.append(new_brick)

            else:
                # checks for other geometry
                val = [float(i) for i in fline.split(' ')]
                color = int(val[1])
                if color == 16:
                    color = old_color
                else:
                    color = Color(color)
                p1 = Point(val[2], val[3], val[4]).translate(translation_matrix)
                p2 = Point(val[5], val[6], val[7]).translate(translation_matrix)

                if fline.startswith('2'):
                    line = Line(color, p1, p2)
                    lines.append(line)

                elif fline.startswith('3'):
                    p3 = Point(val[8], val[9], val[10]).translate(translation_matrix)
                    tri = Triangle(color, p1, p2, p3)
                    triangles.append(tri)

                elif fline.startswith('4'):
                    p3 = Point(val[8], val[9], val[10]).translate(translation_matrix)
                    p4 = Point(val[11], val[12], val[13]).translate(translation_matrix)
                    quad = Quad(color, p1, p2, p3, p4)
                    quads.append(quad)

                elif fline.startswith('5'):
                    # help lines, i dont care about them for now
                    pass
                else:
                    pass

            fline = f.readline().replace('\t', ' ')
    return lines, triangles, quads, bricks
