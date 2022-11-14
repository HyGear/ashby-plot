# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 18:45:25 2022
"""
import numpy as np
import random
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from scipy import interpolate
from matplotlib import pyplot as plt
import csv
from csv import reader
from pathlib import Path

plt.figure(figsize=(18, 18))

material_type='thermoplastic'
# iterate over each line as a ordered dictionary and print only few column by column Number


def makeplot(points,material):
    hull = ConvexHull(points)
    point_indexs=hull.vertices
    cx = np.mean(hull.points[hull.vertices,0])
    cy = np.mean(hull.points[hull.vertices,1])
    
    x_list=[]
    y_list=[]
    for i in point_indexs:
        x_list.append(points[i][0])
        y_list.append(points[i][1])
    
        
    x=np.array(x_list)
    y=np.array(y_list)
    x = np.r_[x, x[0]]
    y = np.r_[y, y[0]]
    
    tck, u = interpolate.splprep([x, y], u=None, s=0.0, per=1, k=3)
    u_new = np.linspace(u.min(), u.max(), num=1000)
    x_new, y_new = interpolate.splev(u_new, tck, der=0)
    
    
    #plt.plot(points[:,0], points[:,1], 'o')
    #plt.loglog(points[:,0], points[:,1], 'o', alpha=0.5)
    #for simplex in hull.simplices:
    #    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
        
    #plt.plot(x, y, 'ro')
    #plt.loglog(x,y, 'ro')
    #plt.plot(x_new, y_new, 'b--')
    plt.loglog(x_new, y_new, 'b--', alpha=0.3)
    #plt.text(x[0],y[0], material, weight='bold', horizontalalignment='center')
    off_x=((x[0]+(x[0]-cx)))
    off_y=((y[0]+(y[0]-cy)))
    if off_x<0:
        off_x=x[0]/2
    if off_y<0:
        off_y=y[0]/2
    #print(off_x,off_y)
    plt.annotate(material, xy =(x[0], y[0]),
                xytext =(off_x,off_y),
                weight='bold',
                bbox= dict(boxstyle ='round', fc ='1'),
                arrowprops = dict(arrowstyle='-', facecolor ='black'),)
    plt.xlim([0.1, 10])
    plt.ylim([0.1, 100])
    plt.title('Young\'s Modulus - Density', weight='bold')
    plt.xlabel('Density ρ (g/cc))', weight='bold')
    plt.ylabel('Young\'s Modulus E (GPa)', weight='bold')
    plt.grid('True')
    r = lambda: random.randint(0,255)
    plt.fill(x_new, y_new, '#%02X%02X%02X' % (r(),r(),r()), alpha=0.3)
    


for p in Path(material_type).glob('*.csv'):
    material=p.stem.upper()
    #material=material.upper()
    
    print(p.name)
    
    with open(material_type + "\\" + p.name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        j=0
        for row in csv_reader:
            if j!=0:
                if j == 1:
                    points = np.array([[float(row[1]),float(row[2])]], dtype='float')
                else:
                    points=np.append(points,[[float(row[1]),float(row[2])]], axis=0)
                    
            j=j+1
            
    makeplot(points,material)
    

plt.show()
#plt.savefig('outputimage.png', dpi=300)
