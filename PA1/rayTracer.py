#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 
class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Sphere:
    def __init__(self, center, radius, diffuse, specular = None, exponent = None):
        self.center = center
        self.radius = radius
        self.diffuse = diffuse
        self.specular = specular
        self.exponent = exponent

    def intersect(self, ray_origin, ray_dir):
        oc = ray_origin - self.center
        a = np.dot(ray_dir, ray_dir)
        b = 2.0 * np.dot(oc, ray_dir)
        c = np.dot(oc, oc) - self.radius ** 2
        disc = b * b - 4 * a * c
        if disc < 0:
            return None
        sqrt_d = np.sqrt(disc)
        t1 = (-b - sqrt_d) / (2 * a)
        t2 = (-b + sqrt_d) / (2 * a)
        if t1 > 0:
            return t1
        if t2 > 0:
            return t2
        return None

def main():


    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float64)
    viewUp=np.array([0,1,0]).astype(np.float64)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float64)  # how bright the light is.
    print(np.cross(viewDir, viewUp))

    imgSize=np.array(root.findtext('image').split()).astype(np.int32)

    for c in root.findall('camera'):
        viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float64)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float64)

        if c.findtext('projDistance'): projDistance = float(c.findtext('projDistance'))
        viewWidth  = float(c.findtext('viewWidth'))
        viewHeight = float(c.findtext('viewHeight'))

        print('viewpoint', viewPoint)

    shaders = {}
    for c in root.findall('shader'):
        name = c.get('name')
        shader_type = c.get('type')
        diffuseColor_c=np.array(c.findtext('diffuseColor').split()).astype(np.float64)
        specular = None
        exponent = None

        print('name', c.get('name'))
        print('diffuseColor', diffuseColor_c)
        
        if shader_type == "Phong":
            specular = np.array(c.findtext('specularColor').split()).astype(np.float64)
            exponent = np.array(c.findtext('exponent').split()).astype(np.float64)
        shaders[name] = (diffuseColor_c, specular, exponent)

    lights = []
    for l in root.findall('light'):
        position = np.array(l.findtext('position').split()).astype(np.float64)
        intensity = np.array(l.findtext('intensity').split()).astype(np.float64)
        lights.append((position, intensity))

    surfaces = []
    for s in root.findall('surface'):
        if s.get('type') == 'Sphere':
            center = np.array(s.findtext('center').split()).astype(np.float64)
            radius = float(s.findtext('radius'))
            ref = s.find('shader').get('ref')
            diffuse, specular, exponent = shaders[ref]
            surfaces.append(Sphere(center, radius, diffuse, specular, exponent))

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!
    w = -viewDir / np.linalg.norm(viewDir)
    u = np.cross(viewUp, w)
    u = u / np.linalg.norm(u)
    v = np.cross(w, u)

    W, H = imgSize[0], imgSize[1]
    for j in range(H):
        for i in range(W):
            su = (i + .5) / W * 2 - 1
            sv = 1 - (j + .5) / H * 2

            ray_dir = (projDistance * (-w)
                        + su * (viewWidth  / 2) * u
                        + sv * (viewHeight / 2) * v)
            ray_dir = ray_dir / np.linalg.norm(ray_dir)

            min_t = float('inf')
            hit_sphere = None
            for s in surfaces:
                t = s.intersect(viewPoint, ray_dir)
                if t is not None and t < min_t:
                    min_t = t
                    hit_sphere = s
            
            if hit_sphere is not None:
                hit_point = viewPoint + min_t * ray_dir
                n = (hit_point - hit_sphere.center) / hit_sphere.radius
    
                pixel_color = np.zeros(3)
                for pos, intensity in lights:
                    l = pos - hit_point
                    l_dist = np.linalg.norm(l)
                    l = l / l_dist

                    in_shadow = False
                    for s in surfaces:
                        li = s.intersect(hit_point, l)
                        if li is not None and li < l_dist:
                            in_shadow = True
                            break;
                    if in_shadow: continue
                    
                    diff = max(.0, np.dot(n, l))
                    pixel_color += hit_sphere.diffuse * intensity * diff

                if hit_sphere.specular is not None:
                    h = l - ray_dir
                    h = h / np.linalg.norm(h)
                    spec = max(.0, np.dot(n, h)) ** hit_sphere.exponent
                    pixel_color += hit_sphere.specular * intensity * spec

                c = Color(*pixel_color)
                c.gammaCorrect(2.2)
                img[j][i] = c.toUINT8()

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save('a.png')
    
if __name__=="__main__":
    main()
