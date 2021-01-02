from math import sin, cos, radians


class Line:

    def __init__(self, color, p1, p2):
        self.color = color
        self.p1 = p1
        self.p2 = p2

    def __add__(self, other):
        return Line(self.color, self.p1+other.p1, self.p2+other.p2)


class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, other):
        return Point(self.x/other, self.y/other, self.z/other)

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __round__(self, n=None):
        return Point(round(self.x, n), round(self.y, n), round(self.z, n))

    def __repr__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)

    def translate(self, tm):
        """
        @param tm: transformation matrix
        @return: transformed point
        """
        u = tm.a * self.x + tm.b * self.y + tm.c * self.z + tm.x
        v = tm.d * self.x + tm.e * self.y + tm.f * self.z + tm.y
        w = tm.g * self.x + tm.h * self.y + tm.i * self.z + tm.z

        self.x = u
        self.y = v
        self.z = w

        return Point(u, v, w)


class Matrix4x4:

    def __init__(self, _11, _12, _13, _14, _21, _22, _23, _24, _31, _32, _33, _34, _41, _42, _43, _44):
        self.a = _11
        self.b = _12
        self.c = _13
        self.x = _14

        self.d = _21
        self.e = _22
        self.f = _23
        self.y = _24

        self.g = _31
        self.h = _32
        self.i = _33
        self.z = _34

        self.j = _41
        self.k = _42
        self.l = _43
        self.w = _44

    @classmethod
    def identity(self):
        return Matrix4x4(1.0, 0.0, 0.0, 0.0,
                         0.0, 1.0, 0.0, 0.0,
                         0.0, 0.0, 1.0, 0.0,
                         0.0, 0.0, 0.0, 1.0)

    def __mul__(self, other):
        return Matrix4x4(self.a*other.a + self.b*other.d + self.c*other.g + self.x*other.j,
                         self.a*other.b + self.b*other.e + self.c*other.h + self.x*other.k,
                         self.a*other.c + self.b*other.f + self.c*other.i + self.x*other.l,
                         self.a*other.x + self.b*other.y + self.c*other.z + self.x*other.w,

                         self.d*other.a + self.e*other.d + self.f*other.g + self.y*other.j,
                         self.d*other.b + self.e*other.e + self.f*other.h + self.y*other.k,
                         self.d*other.c + self.e*other.f + self.f*other.i + self.y*other.l,
                         self.d*other.x + self.e*other.y + self.f*other.z + self.y*other.w,

                         self.g*other.a + self.h*other.d + self.i*other.g + self.z*other.j,
                         self.g*other.b + self.h*other.e + self.i*other.h + self.z*other.k,
                         self.g*other.c + self.h*other.f + self.i*other.i + self.z*other.l,
                         self.g*other.x + self.h*other.y + self.i*other.z + self.z*other.w,

                         self.j*other.a + self.k*other.d + self.l*other.g + self.w*other.j,
                         self.j*other.b + self.k*other.e + self.l*other.h + self.w*other.k,
                         self.j*other.c + self.k*other.f + self.l*other.i + self.w*other.l,
                         self.j*other.x + self.k*other.y + self.l*other.z + self.w*other.w)

    def rotate(self, yaw=180.0, pitch=90.0, roll=0.0):
        """
        rotates a matrix with yaw, pitch and roll
        @param yaw: degrees for rotation over x axis
        @param pitch: degrees for rotation over y axis
        @param roll: degrees for rotation over z axis
        @return: the rotated matrix
        """
        psi = radians(yaw)
        rotation_matrix_x = Matrix4x4(1.0, 0.0, 0.0, 0.0,
                                      0.0, cos(psi), -sin(psi), 0.0,
                                      0.0, sin(psi), cos(psi), 0.0,
                                      0.0, 0.0, 0.0, 1.0)

        psi = radians(pitch)
        rotation_matrix_y = Matrix4x4(cos(psi), 0.0, sin(psi), 0.0,
                                      0.0, 1.0, 0.0, 0.0,
                                      -sin(psi), 0.0, cos(psi), 0.0,
                                      0.0, 0.0, 0.0, 1.0)

        psi = radians(roll)
        rotation_matrix_z = Matrix4x4(cos(psi), -sin(psi), 0.0, 0.0,
                                      sin(psi), cos(psi), 0.0, 0.0,
                                      0.0, 0.0, 1.0, 0.0,
                                      0.0, 0.0, 0.0, 1.0)

        new = (rotation_matrix_z * rotation_matrix_y * rotation_matrix_x) * self

        self.a = new.a
        self.b = new.b
        self.c = new.c
        self.x = new.x
        self.d = new.d
        self.e = new.e
        self.f = new.f
        self.y = new.y
        self.g = new.g
        self.h = new.h
        self.i = new.i
        self.z = new.z
        self.j = new.j
        self.k = new.k
        self.l = new.l
        self.w = new.w

        return new


class Triangle:

    def __init__(self, color, p1, p2, p3):
        self.color = color
        self.normal = calc_normal(p1, p2, p3)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


class Quad:

    def __init__(self, color, p1, p2, p3, p4):
        self.color = color
        self.normal = calc_normal(p1, p2, p3)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4


class Color:

    def __init__(self, color):
        self.c = color
        self.c_name = self.translate_color_name()

    def __eq__(self, other):
        return self.c == other.c

    def __repr__(self):
        return str(self.c_name)

    def translate_color_name(self):
        """
        translates a color code to a string for writing color file
        @return: string representation of this color
        """
        colors = {0: "zero",
                  1: "one",
                  2: "two",
                  3: "three",
                  4: "four",
                  5: "five",
                  6: "six",
                  7: "seven",
                  8: "eight",
                  9: "nine",
                  10: "ten",
                  11: "eleven",
                  12: "twelve",
                  13: "thirteen",
                  14: "fourteen",
                  15: "fifteen",
                  17: "seventeen",
                  18: "eighteen",
                  19: "nineteen",
                  20: "twenty",
                  21: "twentyone",
                  22: "twentytwo",
                  23: "twentythree",
                  25: "twentyfive",
                  26: "twentysix",
                  27: "twentyseven",
                  28: "twentyeight",
                  29: "twentynine",
                  30: "thirty",
                  31: "thirdone",
                  32: "thirtytwo",
                  33: "thirtythree",
                  34: "thirtyfour",
                  35: "thirtyfive",
                  36: "thirtysix",
                  37: "thirtyseven",
                  38: "thirtyeight",
                  39: "thirdynine",
                  40: "forty",
                  41: "fortyone",
                  42: "fortytwo",
                  43: "fortythree",
                  44: "fortyfour",
                  45: "fortyfive",
                  46: "fortysix",
                  47: "fortyseven",
                  71: "seventyone",
                  383: "threeeighttree"
                  }

        self.c_name = colors.get(self.c, "default")
        return self.c_name


def calc_normal(p1, p2, p3):
    """
    calculates to normal of a face given by 3 points
    @param p1: point 1 of face
    @param p2: point 2 of face
    @param p3: point 3 of face
    @return: vector of the normal
    """
    u = p2 - p1
    v = p3 - p1

    nx = u.y * v.z - u.z * v.y
    ny = u.z * v.x - u.x * v.z
    nz = u.x * v.y - u.y * v.x

    return Point(nx, ny, nz)
