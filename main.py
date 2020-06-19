from vector import Vector
from PIL import Image
import numpy as np
import math

def intervalConversion(a, b, c, d, x):
    return (((d-c)*(x-a)/(b-a))+c)

class Camera:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Material:
    def __init__(self, color, specular = 0.5, lambert = 1, ambient = 0.1, shininess = 50):
        self.color = color
        self.specular = specular
        self.lambert = lambert
        self.ambient = ambient
        self.shininess = shininess

class Scene:
    def __init__(self, size, camera, lights, objects, background_color, image_name):
        self.size = size
        self.camera = camera
        self.lights = lights
        self.objects = objects
        self.background_color = background_color
        self.image_name = image_name

    def addSphere(self, pos, radius, color):
        s = Sphere(pos, radius, color)
        objects.append(s)

    def render(self):
        image_size = self.size, self.size
        pixels = Image.new('RGB', image_size, color = 'black')

        for d in range (self.size):
            for c in range (self.size):
                y = float(intervalConversion(0.0, float(self.size), -50.0, +50.0, d))
                x = float(intervalConversion(0.0, float(self.size), -50.0, +50.0, c))

                ray_direction = Vector(x,y,800)-self.camera #altura da tela talvez mudar aqui
                ray = Ray(self.camera, ray_direction)

                raio = self.traceRay(ray)
                r = int(raio.x)
                g = int(raio.y)
                b = int(raio.z)
                
                pixels.putpixel((d,c), (r,g,b))
        
        pixels.save(image_name)

        pixels.show()

    def traceRay(self, ray):
        intersection = self.getIntersection(ray) # acha uma intersecao para cada raio saindo da camera
        
        if intersection is None:
            return self.background_color 

        obj, dist = intersection # achou uma intersecao com um determinado objeto

        intersection_point = ray.getPointAtDist(dist) # retorna o ponto de intersecao
        normal_at_obj_surface = obj.getNormal(intersection_point) # normal a esfera no ponto de intersecao do raio que sai da camera
        
        color = Color(0,0,0)

        color += Vector(255*obj.material.ambient,255*obj.material.ambient,255*obj.material.ambient)

        for light in self.lights:
            intersectionPoint_to_lightRay = (light - intersection_point).normalize()
            light_ray = Ray(intersection_point, intersectionPoint_to_lightRay) # raio que vai do ponto ate a direcao da fonte de luz
            if self.getIntersection(light_ray) is not None:
                lambert_intensity = normal_at_obj_surface * intersectionPoint_to_lightRay
                if lambert_intensity > 0:
                    r = lambert_intensity * obj.material.lambert * obj.material.color.x * 255
                    g = lambert_intensity * obj.material.lambert * obj.material.color.y * 255
                    b = lambert_intensity * obj.material.lambert * obj.material.color.z * 255
                    color += Vector(r,g,b)

        for light in self.lights:
            intersectionPoint_to_lightRay = (light - intersection_point).normalize()
            light_ray = Ray(intersection_point, intersectionPoint_to_lightRay)
            reflected_ray = Ray(intersection_point, light_ray.direction.reflect(normal_at_obj_surface).normalize())
           # reflected_ray_direction = ((normal_at_obj_surface * 2) - light_ray).normalize()
            if self.getIntersection(light_ray) is not None:
                specular_intensity = reflected_ray.direction * (intersection_point - self.camera).normalize()

                if specular_intensity > 0:
                    specular_intensity = specular_intensity ** obj.material.shininess
                    
                    r = specular_intensity * obj.material.specular * 255
                    g = specular_intensity * obj.material.specular * 255
                    b = specular_intensity * obj.material.specular * 255
                    if(color.x > 5 or color.y > 5 or color.z > 5):
                        color += Vector(r,g,b)
                        # color = color
        return color


    def getIntersection(self, ray):
        intersection = None
        for obj in self.objects:
            distance = obj.intersectionDistance(ray)
            if distance is not None:
                intersection = obj, distance
        return intersection

class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

    def getPointAtDist(self, dist):
        return self.origin + self.direction*dist

class Sphere:

    def __init__(self, origin, radius, material):
        self.origin = origin
        self.radius = radius
        self.material = material

    def intersectionDistance(self, ray): # returns the intersection point between a ray and a sphere
        # print("Trying to intersect object with ray direction: " + str(ray.direction.x) + " " + str(ray.direction.y) + " " + str(ray.direction.z))
        sphere_center_to_ray = ray.origin - self.origin
        b = 2 * ray.direction * sphere_center_to_ray
        c = sphere_center_to_ray**2 - self.radius**2
        discriminant = b**2 - 4*c
        
        if discriminant >= 0.0:
            dist = min((-b - math.sqrt(discriminant))/2, (-b + math.sqrt(discriminant))/2)
            return dist

    def getNormal(self, point):
        return(point - self.origin).normalize()

Point = Vector
Color = Vector

if __name__ == "__main__":
    objects = []

    for i in range (0,3):
        for j in range (0,3):
            s = Sphere(Vector(120*i-120,120*j-100,0), 50, Material(Vector(0.9,0.2,0.2),specular=0.7))
            objects.append(s)

    camera = Vector(0,0,1000)
    lights = [Vector(200,200,100)]
    background_color = Vector(0,0,0)
    image_name = 'imagem_extra.png'

    scene = Scene(1000,camera,lights,objects,background_color, image_name)
    scene.render()
