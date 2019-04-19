# Universidad del Valle de Guatemala
# Graficas por Computadora - Seccion 10
# Maria Fernanda Estrada 14198
# Funciones para crear un escritor de imagenes BMP
# Codigo base en ejemplo visto en clase
# Multiplicar matrices y generar el pipeline de graficas





import struct
from collections import namedtuple
from random import randint


# Vectores
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])


def char(c): # Funcion vista en clase
    return struct.pack("=c", c.encode('ascii'))


def word(c): # Funcion vista en clase
    return struct.pack("=h", c)


def dword(c): # Funcion vista en clase
    return struct.pack("=l", c)


def color(r, g, b): # Funcion vista en clase, para tener en bytes el color ingresado
    return bytes([b, g, r])


# Operaciones de vector (Visto en clase)

# Suma
def suma(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

# Resta
def resta(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

# Multiplicar por escalar
def mul(v0, k):
    return V3(v0.x * k, v0.y * k, v0.z * k)

# Producto punto
def punto(v0, v1):
    return (v0.x * v1.x) + (v0.y * v1.y) + (v0.z * v1.z)

# Producto cruz
def cruz(v0, v1):
    return V3(
        v0.y * v1.z - v0.z * v1.y,
        v0.z * v1.x - v0.x * v1.z,
        v0.x * v1.y - v0.y * v1.x
    )

# Largo de vector
def largov(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

# Normalizar vector
def norm(v0):
    l = largov(v0)
    if not l:
        return V3(0, 0, 0)
    return V3(v0.x/l, v0.y/l, v0.z/l)


# Funcion de multiplicacion de matrices (tomado de https://www.programiz.com/python-programming/examples/multiply-matrix)
def matrixMult(X, Y):
    result = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
    # Iterar filas de X
    for i in range(len(X)):
        # Iterar columnas de Y
        for j in range(len(Y[0])):
            # Iterar filas de Y
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]
    return result



# Clase Bitmap, para generar la imagen
class Bitmap(object):

    # Constructor del bitmap
    def __init__(self, width, height):
        # Valores iniciales
        self.width = width
        self.height = height
        self.color_clear = color (0, 0, 0)
        self.color_point = color (0, 0, 0)
        self.vp_x = 0 # Para viewport => vp
        self.vp_y = 0
        self.vp_width = 0
        self.vp_height = 0
        self.framebuffer = []
        self.clear()
    
    # Funcion dentro de Bitmap para modificar alto y ancho, solo cambia los valores actuales
    def cambioWidthHeight(self, width, height):
        self.width = width
        self.height = height

    # Funcion para colorear de un color toda la pantalla
    def clear(self):
        self.framebuffer = [
            [self.color_clear for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]
    
    # Funcion para modificar color del clear
    def clearcolor(self, r, g, b):
        self.color_clear = color(r, g, b)

    # Funcion para generar Viewport, area de imagen sobre la cual se dibujara
    def viewport(self, x, y, width, height):
        self.vp_x = x
        self.vp_y = y
        self.vp_width = width-1 # Se le resta 1 porque se sale por uno del index si no se coloca
        self.vp_height = height-1

    # Funcion para generar el archivo de imagen, vista en clase
    def write(self, filename):
        f = open(filename, 'bw')
        # File Header 14
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + (self.width*self.height*3)))
        f.write(dword(0))
        f.write(dword(14 + 40))
        # Image Header 40
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width*self.height*3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
        
        f.close()
    
    # Funcion para cambiar el color del punto a dibujar en el viewport
    def colorPoint(self, r, g, b):
        self.color_point = color(r, g, b)

    # Funcion para crear un punto dentro del viewport
    def point(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        else:
            self.framebuffer[y][x] = self.color_point



# Funciones "globales"
bm = Bitmap(0,0)


# Inicializar Bitmap con valores default
def glInit():
    global bm 
    bm = Bitmap(600,400)


# Crear ventana con width y height como parametros
def glCreateWindow(width, height):
    bm.cambioWidthHeight(width, height) # Usando funcion Bitmap para cambiar el ancho y alto


# Crear area sobre la cual se dibujara
def glViewPort(x, y, width, height):
    bm.viewport(x, y, width, height)


# Limpiar ventana, usando funcion en Bitmap
def glClear():
    bm.clear()


# Cambiar color de clear
def glClearColor(r, g, b):
    bm.clearcolor(int(r*255), int(g*255), int(b*255))


# Generar un punto en el viewport
def glVertex(x, y):
    equis = (((x+1)/2)*(bm.vp_width)) + (bm.vp_x)
    ye = (((y+1)/2)*(bm.vp_height)) + (bm.vp_y)
    bm.point(equis, ye)


# Cambiar el color de un punto
def glColor(r, g, b):
    bm.colorPoint(int(r*255), int(g*255), int(b*255))


# Generar la imagen en un archivo
def glFinish():
    bm.write("out.bmp")


# Funcion bbox (visto en clase)
def bbox(A, B, C):
    xs = sorted([A.x, B.x, C.x])
    ys = sorted([A.y, B.y, C.y])
    return V2(xs[0], ys[0]), V2(xs[2], ys[2])


# Funcion barycentric (visto en clase)
def barycentric(A, B, C, P):
    cx, cy, cz = cruz(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    if cz == 0:
        return -1, -1, -1
    
    # Coordenadas baricentricas
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    return w, v, u


# Rellenar triangulos (visto en clase)
def triangle(A, B, C, nA, nB, nC, TAcord = 0, TBcord = 0, TCcord = 0, texture = None):
    bbox_min, bbox_max = bbox(A, B, C)

    for x in range(bbox_min.x, bbox_max.x + 1):
        for y in range(bbox_min.y, bbox_max.y + 1):
            w, v, u = barycentric(A, B, C, V2(x, y))

            # Si estan fuera del triangulo, no pintar
            if w < 0 or v < 0 or u < 0:
                continue
            
            # Ver el color del pixel de textura
            if texture:
                tA, tB, tC = TAcord, TBcord, TCcord
                tx = tA.x * w + tB.x * v + tC.x * u
                ty = tA.y * w + tB.y * v + tC.y * u
                #color = texture.get_Color(tx, ty, intensity)

            z = A.z * w + B.z * v + C.z * u

            if texture:
                continue
                #bm.colorPoint(*color)
            else:
                color = shader(A,B,C,w,u,v,nA,nB,nC)
                bm.colorPoint(*color)

            # Si z es mayor que el z buffer, pintar y cambiar valor zbuffer
            # Esto sirve para saber que z esta mas arriba y cual mas atras
            if (x>0) and (x<bm.width) and (y>0) and (y<bm.height):
                if z > bm.zbuffer[x][y]:
                    bm.point(x, y)
                    bm.zbuffer[x][y] = z

def shader(A,B,C,w,u,v,nA,nB,nC):
    nx = nA.x * w + nB.x * u + nC.x * v
    ny = nA.y * w + nB.y * u + nC.y * v
    nz = nA.z * w + nB.z * u + nC.z * v

    x = A.x * w + B.x * u + C.x * v
    y = A.y * w + B.y * u + C.y * v
    z = A.z * w + B.z * u + C.z * v

    vn = V3(nx, ny, nz)

    luz = V3(0,0,1)

    intensity = punto(vn, luz)
    
    if intensity < 0:
        intensity = 0
    elif intensity > 1:
        intensity = 1

    if y>0 and y<260:
        return color(
            int(85 * intensity),
            int(91 * intensity),
            int(92 * intensity)
        )
    elif y>=260 and y<280:
        return color(
            int(95 * intensity),
            int(107 * intensity),
            int(119 * intensity)
        )
    elif y>=280 and y<305:
        return color(
            int(126 * intensity),
            int(137 * intensity),
            int(158 * intensity)
        )
    elif y>=305 and y<310:
        return color(
            int(130 * intensity),
            int(146 * intensity),
            int(166 * intensity)
        )
    elif y>=310 and y<320:
        return color(
            int(177 * intensity),
            int(184 * intensity),
            int(203 * intensity)
        )
    elif y>=320 and y<340:
        return color(
            int(255 * intensity),
            int(255 * intensity),
            int(255 * intensity)
        )
    elif y>=340 and y<350:
        return color(
            int(143 * intensity),
            int(159 * intensity),
            int(186 * intensity)
        )
    elif y>=350 and y<360:
        return color(
            int(106 * intensity),
            int(140 * intensity),
            int(187 * intensity)
        )
    elif y>=360 and y<380:
        return color(
            int(43 * intensity),
            int(79 * intensity),
            int(128 * intensity)
        )
    elif y>=380 and y<400:
        return color(
            int(67 * intensity),
            int(113 * intensity),
            int(192 * intensity)
        )
    elif y>=400 and y<420:
        return color(
            int(112 * intensity),
            int(146 * intensity),
            int(193 * intensity)
        )
    elif y>=420 and y<430:
        return color(
            int(84 * intensity),
            int(109 * intensity),
            int(136 * intensity)
        )
    elif y>=430 and y<450:
        return color(
            int(64 * intensity),
            int(94 * intensity),
            int(153 * intensity)
        )
    elif y>=450 and y<460:
        return color(
            int(67 * intensity),
            int(107 * intensity),
            int(158 * intensity)
        )
    elif y>=460 and y<480 and y>480 and y<500:
        return color(
            int(255 * intensity),
            int(255 * intensity),
            int(255 * intensity)
        )
    elif y==480:
        return color(
            int(226 * intensity),
            int(227 * intensity),
            int(224 * intensity)
        )
    elif y>=500 and y<515:
        return color(
            int(106 * intensity),
            int(132 * intensity),
            int(164 * intensity)
        )
    elif y==515:
        return color(
            int(255 * intensity),
            int(255 * intensity),
            int(255 * intensity)
        )
    elif y>=516 and y<545:
        return color(
            int(107 * intensity),
            int(127 * intensity),
            int(151 * intensity)
        )
    elif y>=545 and y<575:
        return color(
            int(104 * intensity),
            int(118 * intensity),
            int(137 * intensity)
        )
    elif y>=575:
        return color(
            int(79 * intensity),
            int(93 * intensity),
            int(107 * intensity)
        )
    else:
        return color(
            int(255 * intensity),
            int(255 * intensity),
            int(255 * intensity)
        )