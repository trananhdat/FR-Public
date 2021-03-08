import numpy as np 
from scipy.spatial import distance

# mapping object using distance from 1 object -> 1 object other

def new2old(list_old, face):

    coordinates_old = [( (f.rect[0] + f.rect[2]) // 2 , (f.rect[1] + f.rect[3])//2 ) for f in list_old]
    x, y = (face[0] + face[2]) // 2, (face[1] +  face[3]) // 2
    coordinates_new = [(x, y) ]
    dis = distance.cdist(coordinates_new, coordinates_old, 'euclidean')[0]
    if np.min(dis) > 60:
        return False, -1
    return True, np.argmin(dis)

def old2new(list_new, f_old):

    coordinates_new = [( (face[0] + face[2]) // 2 , (face[1] + face[3]) // 2 )for face in list_new]
    x, y = (f_old.rect[0] + f_old.rect[2]) // 2 , (f_old.rect[1] + f_old.rect[3])//2 
    coordinates_old = [(x, y)]
    dis = distance.cdist(coordinates_old, coordinates_new, 'euclidean')[0]
    
    if np.min(dis) > 60:
        return False, -1
    return True, np.argmin(dis)


if __name__ == '__main__':
    a= [[685, 122, 769, 229], [440, 142, 530, 232]]

    class Test:

        def __init__(self):
            rect = []
            
    t = Test()
    t.rect = [440, 142, 530, 232]

    print(old2new(a, t))

