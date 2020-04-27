import math
from matrix import *
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

def distribute_constant(color, const):
    color[RED] = color[RED] * const[RED]
    color[GREEN] = color[GREEN] * const[GREEN]
    color[BLUE] = color[BLUE] * const[BLUE]

def vector_subtract(a,b):
    for i in range(len(a)):
        a[i] = a[i]-b[i]

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(light[LOCATION])
    normalize(view)
    normalize(normal)

    ret = []

    ambient=calculate_ambient(ambient,areflect)
    diffuse=calculate_diffuse(light,dreflect,normal)
    specular=calculate_specular(light,sreflect,view,normal)

    for i in range(3):
        ret.append(ambient[i]+diffuse[i]+specular[i])
    limit_color(ret)
    #print ret
    return ret



def calculate_ambient(alight, areflect):
    color = alight[:]
    distribute_constant(color, areflect)
    limit_color(color)
    return list(map(int, color))

def calculate_diffuse(light, dreflect, normal):
    color = light[COLOR][:]
    #print "Before: " + str(color)
    pos = light[LOCATION]
    dot = dot_product(normal, pos)
    if dot < 0:
        dot = 0
    scalar_mult(color, dot)
    distribute_constant(color, dreflect)
    #print "After: " + str(color)
    limit_color(color)
    return list(map(int, color))

def calculate_specular(light, sreflect, view, normal):
    color = light[COLOR][:]
    dot1 = dot_product(normal, light[LOCATION])
    if dot1 <= 0:
        return [0,0,0]
    prod1 = 2 * dot1
    scalar_mult(normal, prod1)
    vector_subtract(normal, light[LOCATION])
    dot2 = dot_product(normal, view)
    distribute_constant(color, sreflect)
    scalar_mult(color, (dot2 ** SPECULAR_EXP))
    limit_color(color)
    return list(map(int, color))

def limit_color(color):
    for i in range(len(color)):
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
            color[i] = 0

#vector functions
def normalize(vector):
    scale = (1.0)/(math.sqrt((vector[0]*vector[0]) + (vector[1]*vector[1]) + (vector[2]*vector[2])))
    scalar_mult(vector, scale)
    return vector

def dot_product(a, b):
    return (a[0]*b[0]) + (a[1]*b[1]) + (a[2]*b[2])

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
