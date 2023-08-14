import open3d as o3d

class triangle:
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def get_centroid(self) -> list:
        """ get the centroid of a rectangle
        return the centroid
        """
        x_min = min(self.x)
        x_max = max(self.x)
        y_min = min(self.y)
        y_max = max(self.y)
        z_min = min(self.z)
        z_max = max(self.z)
        centroid = [(x_min+x_max)/2,(y_min+y_max)/2,(z_min+z_max)/2]
        return centroid

    def get_obj(self):
        """ get the vertices, edges and colors of the edges when
        visualizing the rectangles.
        return the list of above information
        """
        points = [[self.x[i],self.y[i],self.z[i]] for i in range(3)]
        lines = [[0,1],[1,2],[0,2]]
        colors = [[1, 0, 0] for i in range(len(lines))]
        return [points,lines,colors]
    
    def get_box(self):
        """ get the vertices, edges and colors of the edges of the
        boxes bounding the rectangles.
        return the list of above information
        """
        x_min = min(self.x)
        x_max = max(self.x)
        y_min = min(self.y)
        y_max = max(self.y)
        z_min = min(self.z)
        z_max = max(self.z)
        points = [[x_min,y_min,z_min],
                  [x_min,y_max,z_min],
                  [x_max,y_min,z_min],
                  [x_max,y_max,z_min],
                  [x_min,y_min,z_max],
                  [x_min,y_max,z_max],
                  [x_max,y_min,z_max],
                  [x_max,y_max,z_max]]
        lines = [[0,1],
                 [0,2],
                 [2,3],
                 [1,3],
                 [0,4],
                 [1,5],
                 [2,6],
                 [3,7],
                 [4,5],
                 [4,6],
                 [6,7],
                 [5,7]]
        colors = [[0, 0, 1] for i in range(len(lines))]
        return [points,lines,colors]

class Node:
    def __init__(self,list,left,right):
        self.list = list
        self.left = left
        self.right = right
    
    def get_x_min(self):
        """ get the minimum x-axis of all rectangles stored in this Node.
        return a double value represents the minimum x-axis
        """
        return min([min(i.x) for i in self.list])
    
    def get_x_max(self):
        """ get the maximum x-axis of all rectangles stored in this Node.
        return a double value represents the maximum x-axis
        """
        return max([max(i.x) for i in self.list])
    
    def get_y_min(self):
        """ get the minimum y-axis of all rectangles stored in this Node.
        return a double value represents the minimum x-axis
        """
        return min([min(i.y) for i in self.list])
    
    def get_y_max(self):
        """ get the maximum x-axis of all rectangles stored in this Node.
        return a double value represents the maximum x-axis
        """
        return max([max(i.y) for i in self.list])
    
    def get_z_min(self):
        """ get the minimum y-axis of all rectangles stored in this Node.
        return a double value represents the minimum y-axis
        """
        return min([min(i.z) for i in self.list])
    
    def get_z_max(self):
        """ get the minimum x-axis of all rectangles stored in this Node.
        return a double value represents the minimum x-axis
        """
        return max([max(i.z) for i in self.list])
    
    def get_x_length(self):
        return self.get_x_max() - self.get_x_min()
    
    def get_y_length(self):
        return self.get_y_max() - self.get_y_min()
    
    def get_z_length(self):
        return self.get_z_max() - self.get_z_min()
    
    def get_box(self):
        x_min = self.get_x_min()
        x_max = self.get_x_max()
        y_min = self.get_y_min()
        y_max = self.get_y_max()
        z_min = self.get_z_min()
        z_max = self.get_z_max()
        points = [[x_min,y_min,z_min],
                  [x_min,y_max,z_min],
                  [x_max,y_min,z_min],
                  [x_max,y_max,z_min],
                  [x_min,y_min,z_max],
                  [x_min,y_max,z_max],
                  [x_max,y_min,z_max],
                  [x_max,y_max,z_max]]
        lines = [[0,1],
                 [0,2],
                 [2,3],
                 [1,3],
                 [0,4],
                 [1,5],
                 [2,6],
                 [3,7],
                 [4,5],
                 [4,6],
                 [6,7],
                 [5,7]]
        colors = [[0, 0, 1] for i in range(len(lines))]
        return [points,lines,colors]

    def travel_tree(self, root):
        res = []
        
        if root:
            
            if (len(root.list) != 1):
                res.append(root.get_box()) 
        
            res = res + self.travel_tree(root.left)
            res = res + self.travel_tree(root.right)
        return res
    

def compare_x(x,y):
    return x.get_centroid()[0] - y.get_centroid()[0]
def compare_y(x,y):
    return x.get_centroid()[1] - y.get_centroid()[1]  
def compare_z(x,y):
    return x.get_centroid()[2] - y.get_centroid()[2]    
from functools import cmp_to_key  
 
def construct_bvhs(root):
    if (len(root.list) == 1):
        return
    x_length = root.get_x_length()
    y_length = root.get_y_length()
    z_length = root.get_z_length()
    if (x_length == max(x_length,y_length,z_length)):
        sorted(root.list, key=cmp_to_key(compare_x))
        med = len(root.list)//2
        root.left = Node(list = root.list[:med], left = None, right = None)
        root.right = Node(list = root.list[med:], left = None, right = None)
        construct_bvhs(root.left)
        construct_bvhs(root.right)
    if (y_length == max(x_length,y_length,z_length)):
        sorted(root.list, key=cmp_to_key(compare_y))
        med = len(root.list)//2
        root.left = Node(list = root.list[:med], left = None, right = None)
        root.right = Node(list = root.list[med:], left = None, right = None)
        construct_bvhs(root.left)
        construct_bvhs(root.right)
    if (z_length == max(x_length,y_length,z_length)):
        sorted(root.list, key=cmp_to_key(compare_z))
        med = len(root.list)//2
        root.left = Node(list = root.list[:med], left = None, right = None)
        root.right = Node(list = root.list[med:], left = None, right = None)                  
        construct_bvhs(root.left)
        construct_bvhs(root.right)
    
def create_obj_file(root, path):
    list_box = root.travel_tree(root)
    list = []
    print(len(list_box))
    '''
    for i in root.list:
        list.append([i.get_obj()[0], i.get_obj()[1]])
    '''
    
    for i in list_box:
       list.append([i[0],i[1]])
    
    f = open(path, "w")
    for i in list:
        for j in i[0]:
            f.write('v ')
            for k in j:
                f.write(str(k)+' ')
            f.write('\n')
    # for i in range(len(root.list)):
        '''
        for j in list[i][1]:
            f.write('l ')
            for k in j:
                f.write(str(k+i*len(list[i][1])+1)+' ')
            f.write('\n')
        '''
    for i in range(len(list_box)):
        for j in list[i][1]:
            f.write('l ')
            for k in j:
                f.write(str(k+i*8+1)+' ')
            f.write('\n')
    
    f.close()
    
import random as rd       
def bvhs_test():
    k = 15
    list_tri = []
    for i in range(k):
        x = [rd.random() for j in range(3)]
        y = [rd.random() for j in range(3)]
        z = [rd.random() for j in range(3)]
        tri = triangle(x,y,z)
        list_tri.append(tri)
        
    root = Node(list=list_tri,left=None,right=None)
    construct_bvhs(root)
    # create_obj_file(root, "C:\\Users\\VTO\\Documents\\3d_model\\bvh.txt")
    draw(root)

def get_vertices():
    vertices = []
    f = open("c:\\Users\\VTO\\Downloads\\Human11.txt","r")
    for x in f:
        if x[:2] != 'v ':
            continue
        vertices.append([float(i) for i in x[2:].strip().split(' ')])
    return vertices
def get_triangle():
    triangle_list = []
    f = open("c:\\Users\\VTO\\Downloads\\Human11.txt","r")
    for x in f:
        if x[:2] != 'f ':
            continue
        mesh = x[2:].strip().split(' ')
        ver = []
        for i in mesh:
            j = i.split('/')
            ver.append(int(j[0]))
        triangle_list.append(ver)
    list_tri = []
    vertices = get_vertices()
    for i in triangle_list:
        x = [vertices[i[0]-1][0],vertices[i[1]-1][0],vertices[i[2]-1][0]]
        y = [vertices[i[0]-1][1],vertices[i[1]-1][1],vertices[i[2]-1][1]]
        z = [vertices[i[0]-1][2],vertices[i[1]-1][2],vertices[i[2]-1][2]]
        tri = triangle(x,y,z)
        list_tri.append(tri)
    return list_tri
def main():
    list_tri = get_triangle()
    root = Node(list=list_tri,left=None,right=None)
    construct_bvhs(root)
    create_obj_file(root, "C:\\Users\\VTO\\Documents\\3d_model\\human.txt")
if __name__ == '__main__':
    main()

   

        
 
       
        