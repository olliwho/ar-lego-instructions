import os
import sys

import fileParser


class Brick:

    def __init__(self, color, position, orientation, model_file):
        """
        creates a brick object
        @param color: color, in .ldr integer values
        @param position: position of the brick
        @param orientation: translation matrix for all points of the brick
        @param model_file: path to file that holds all lines triangles quads and bricks of that brick
        """
        self.color = color
        self.position = position        # 3x1 vector
        self.orientation = orientation  # 4x4 matrix
        self.file = model_file          # string

        self.bricks = []
        steps, lines, triangles, quads, bricks = [], [], [], [], []
        # really hacky fix for .mpd files
        if model_file.lower().endswith("ldr"):
            steps = fileParser.parse_manual(os.path.join(os.path.dirname(sys.argv[1]), model_file.lower()), orientation)
        else:
            lines, triangles, quads, bricks = fileParser.parse_brick(model_file, orientation, color)
        self.steps = steps
        self.lines = lines
        self.triangles = triangles
        self.quads = quads
        self.bricks = bricks

    def __repr__(self):
        return self.file

    def get_bricks_rec(self):
        """
        gets all files associated with that brick
        @return: possibly nested list of all brick files associated with this one
        """
        bricks = [b.get_bricks_rec() for b in self.bricks]
        return [self] + bricks
