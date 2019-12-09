import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math


# suppose 80 student present
n = 10  
d = 10

n = int(input("Number of rows: "))
d = int(input("Number of columns: "))

# each student as a pixel
crl = np.zeros((n,d))

# raspberry Pi address matrix
adr = np.zeros((n,d),dtype= int)



######################################################################
############################### classes ##############################
######################################################################
class shape(object) :

    """
    shape interface.
    """

    def sh_name(self):
        raise NotImplementedError()

    def sh_trans(self,row,col,arr):
        raise NotImplementedError()


class edge(shape) :
    
    def sh_name(self):
        print("light on edges")

    def sh_trans(self,row,col,arr):
        for i in range(row):
            for j in range(col):
                if i == 0 or i == row-1:
                    arr[i][j] = 1
                if j == 0 or j == col-1:
                    arr[i][j] = 1
        return arr


class random_shape(shape) :
    def sh_name(self):
        print("random shape")
    
    def sh_trans(self,row,col, arr):
        arr = np.random.randint(0, 2, size=(row, col))
        return arr



class u_tri(shape) :
    def sh_name(self):
        print("upper triangular")
    
    def sh_trans(self,row,col, arr):
        arr = np.ones((row,col))
        return np.triu(arr)


class l_tri(shape) :
    def sh_name(self):
        print("Lower triangular")
    
    def sh_trans(self,row,col, arr):
        arr = np.ones((row,col))
        return np.tril(arr)       


class letter_U(shape) :
    def sh_name(self):
        print("letter U")
    
    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        for i in range(row):
            for j in range(col):
                if j == 0 or j == col - 1:
                    arr[i][j] = 1
                if i == row - 2:
                    arr[i][j] = 1
                if i == 0 or i == row -1:
                    arr[i][j] = 0
        return arr


class letter_C(shape) :
    def sh_name(self):
        print("letter C")
    
    def sh_trans(self,row,col,arr):
        ob_O = edge()
        O = ob_O.sh_trans(row,col,arr)
        C = lhalf_shape(row,col,O)
        C = right_shfit(C,int(col/3))
        return C


class letter_L(shape) :
    def sh_name(self):
        print("letter L")
    
    def sh_trans(self,row,col,arr):
        ob_U = letter_U()
        U = ob_U.sh_trans(row,col,arr)
        L = lhalf_shape(row,col,U)
        L = right_shfit(L,int(col/3))
        return L

class cross_up(shape) :
    def sh_name(self):
        print("cross up")
    
    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        r = row 
        c = 0
        while(r > 0 and c < col):
            arr[r-1][c] = 1
            r = r - 1
            c = c + 1
        return arr

class cross_down(shape) :
    def sh_name(self):
        print("cross down")
    
    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        r = row
        c = col
        while(r>0 and c>0):
            arr[r-1][c-1] = 1
            r = r - 1 
            c = c - 1
        return arr

class letter_A_left(shape):

    def sh_name(self):
        print("letter A left")
    
    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        r = row
        c = 0
        while(r > 1 and c < col):
            arr[r-1][c] = 1
            arr[r-2][c] = 1
            r = r - 2
            c = c + 1
        
        return arr
        
class letter_A_right(shape):

    def sh_name(self):
        print("letter A right")
    
    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        r = row
        c = col
        while(r>0 and c>0):
            arr[r-1][c-1] = 1
            arr[r-2][c-1] = 1
            r = r - 2
            c = c - 1
        return arr

class letter_A(shape):

    def sh_name(self):
        print("letter A")
    
    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        m_1,m_2 = ortho_devide_matrix(row,col,arr)
        A_l = letter_A_left()
        A_r = letter_A_right()
        m_1 = A_l.sh_trans(np.shape(m_1)[0], np.shape(m_1)[1],m_1)
        m_2 = A_r.sh_trans(np.shape(m_2)[0], np.shape(m_2)[1],m_2)
        arr = ortho_comb_matrix(m_1,m_2)
        row_mid = int(row/2)
        start_c = 0
        for i in range(col):
            if arr[row_mid][i] == 1:
                start_c = i
                break
        end_c = 0
        for i in range(col):
            if arr[row_mid][i] == 1:
                end_c = i
        
        for i in range(col):
            if (i>= start_c and i <= end_c):
                arr[row_mid][i] = 1

        return arr


class letter_E(shape):

    def sh_name(self):
        print("letter E")
    
    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        row_mid = int(row/2)
        arr[:,[0]] = 1
        arr[[0],:] = 1
        arr[[row-1],:] = 1
        arr[[row_mid-1],:] = 1
        arr = lhalf_shape(row,col,arr)
        arr = right_shfit(arr,int(col/3))
        return arr



class triangle(shape) :
    
    def sh_name(self):
        print("Triangle shape comes in") 

    def sh_trans(self,row,col,arr):
        step = 1
        arr = f_triangle(arr,step)
        return arr

class heart_(shape):

    def sh_name(self):
        print("Heart shape")
    
    def sh_trans(self,row,col,arr):
        arr_up,arr_down = hori_devide_matrix(row,col,arr)

        # form an fliped triangle on the bottom part
        tri = triangle()
        arr_down = tri.sh_trans(np.shape(arr_down)[0], np.shape(arr_down)[1], arr_down)
        arr_down = up_side_down(arr_down)

        # form two triangle on the top left by right
        arr_up_l, arr_up_r = ortho_devide_matrix(np.shape(arr_up)[0], np.shape(arr_up)[1], arr_up)
        arr_up_l = tri.sh_trans(np.shape(arr_up_l)[0], np.shape(arr_up_l)[1],arr_up_l)
        arr_up_r = tri.sh_trans(np.shape(arr_up_r)[0], np.shape(arr_up_r)[1],arr_up_r)

        arr_up = ortho_comb_matrix(arr_up_l,arr_up_r)
        arr = hori_comb_matrix(arr_up,arr_down)

        return arr

class tree(shape) :
    
    def sh_name(self):
        print("star shape") 

    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        arr_up, arr_down = hori_devide_matrix(row,col,arr)
        tri = triangle()
        arr_up = tri.sh_trans(np.shape(arr_up)[0], np.shape(arr_up)[1], arr_up)
        arr = hori_comb_matrix(arr_up, arr_down)
        mid_col = int(col/2)
        arr[:,[mid_col]] = 1
        arr[:,[mid_col-1]] = 1
        return arr

class letter_I(shape) :
    
    def sh_name(self):
        print("Letter I shape") 

    def sh_trans(self,row,col,arr):
        arr = np.zeros((row,col))
        mid_col = int(col/2)
        arr[:,[mid_col]] = 1
        arr[[0],:] = 1
        arr[[row-1],:] = 1
        
        return arr
    

######################################################################
############################# functions ##############################
######################################################################
def Pi_address(arr):
    print(adr)

def show_(row, col, arr):
    "Show the matrix as a diagram"
    fig, ax = plt.subplots()
    ax.matshow(arr, cmap=plt.cm.Blues)

    for i in range(row):
        for j in range(col):
            c = arr[i][j]
            ax.text(j, i, str(c), va='center', ha='center')

    plt.show()

def flip_(row, col, arr):
    "flip the matrix"
    if row == col:
        arr = np.transpose(arr)
    else:
        print("Array is not square can't be flipped")
    return arr

def lhalf_shape(row, col, arr):
    "Take the left half of the shape"
    mid_col = int(col/2)
    for i in range(row):
        for j in range(col):
            if j >= mid_col:
                arr[i][j] = 0
    return arr

def ortho_devide_matrix(row, col, arr):
    "Divide the matrix into two equal left and right smaller matrix"
    mid_col = int(col/2)
    m_1 = np.zeros((row,mid_col))
    m_2 = np.zeros((row,col-mid_col))
    for i in range(mid_col):
        m_1[:,[i]] = arr[:,[i]]
    for j in range(col-mid_col):
        m_2[:,[j]] = arr[:,[mid_col+j]]
    return m_1, m_2

def ortho_comb_matrix(m1,m2):
    total_col = np.shape(m1)[1] + np.shape(m2)[1]
    t_m = np.zeros((np.shape(m1)[0],total_col))
    for i in range(np.shape(m1)[1]):
        t_m[:,[i]] = m1[:,[i]] 
    for j in range(np.shape(m2)[1]):
        t_m[:,[np.shape(m1)[1]+j]] = m2[:,[j]] 
    return t_m

def hori_devide_matrix(row, col, arr):
    "Divide the matrix into two equal up and down smaller matrix"
    mid_row = int(row/2)
    m_1 = np.zeros((mid_row,col))
    m_2 = np.zeros((row-mid_row,col))
    for i in range(mid_row):
        m_1[[i],:] = arr[[i],:]
    for j in range(row-mid_row):
        m_2[[j],:] = arr[[mid_row+j],:]
    return m_1, m_2

def hori_comb_matrix(m1,m2):
    total_row = np.shape(m1)[0] + np.shape(m2)[0]
    t_m = np.zeros((total_row,np.shape(m1)[1]))
    for i in range(np.shape(m1)[0]):
        t_m[[i],:] = m1[[i],:] 
    for j in range(np.shape(m2)[0]):
        t_m[[np.shape(m1)[0]+j],:] = m2[[j],:] 
    return t_m

def right_shfit(arr,k):
    "The fucntion would right shift the matrix by k horizontally"
    arr = np.roll(arr, k)
    return arr 
            
def f_triangle(arr,step):
    "Draw the triangle, it's stepness depends on step"
    r,c = np.shape(arr)
    arr = np.ones((r,c))

    short = 0
    while (r > 0):
        for i in range(int(short)):
            arr[r-1][i] = 0
            arr[r-1][(c-1)-i] = 0
        short = short + 1/step
        r = r - 1 
    return arr 

def up_side_down(arr):
    arr = np.flipud(arr)
    return arr

def sh_window(start_row, end_row, arr):
    arr = arr[start_row:end_row,:]
    return arr

def show_window(size,arr):
    ite = np.shape(arr)[0]
    for i in range(ite):
        if (i + size < ite):
            arr_temp = sh_window(i,i+size,arr)
            show_(np.shape(arr_temp)[0],np.shape(arr_temp)[1],arr_temp)

def right_scroll(arr,ite):
    for i in range(ite):
        arr = right_shfit(arr,i)
        show_(np.shape(arr)[0],np.shape(arr)[1],arr)

def clockwise_rotate(arr):
    arr = list(zip(*reversed(arr)))
    return arr

def shape_series(arr):

    shape_I = letter_I()
    i = shape_I.sh_trans(np.shape(arr)[0],np.shape(arr)[1],arr)

    shape_heart = heart_()
    h = shape_heart.sh_trans(n,d,crl)

    shape_U = letter_U()
    u = shape_U.sh_trans(np.shape(arr)[0],np.shape(arr)[1],arr)

    shape_C = letter_C()
    c = shape_C.sh_trans(np.shape(arr)[0],np.shape(arr)[1],arr)

    shape_L = letter_L()
    l = shape_L.sh_trans(np.shape(arr)[0],np.shape(arr)[1],arr)

    shape_A = letter_A()
    a = shape_A.sh_trans(np.shape(arr)[0],np.shape(arr)[1],arr)

    shape_cross_down = cross_down()
    cd = shape_cross_down.sh_trans(np.shape(arr)[0],np.shape(arr)[1],arr)

    shape_E = letter_E()
    e = shape_E.sh_trans(np.shape(arr)[0],np.shape(arr)[1],arr)

    arr = ortho_comb_matrix(i,h)
    arr = ortho_comb_matrix(arr,u)
    arr = ortho_comb_matrix(arr,c)
    arr = ortho_comb_matrix(arr,l)
    arr = ortho_comb_matrix(arr,a)
    arr = ortho_comb_matrix(arr,cd)
    arr = ortho_comb_matrix(arr,e)
    arr = ortho_comb_matrix(arr,e)

    show_(np.shape(arr)[0],np.shape(arr)[1],arr)


    



def main():
    # #test for edge shape
    # shape_edge = edge()
    # print(shape_edge.sh_name())
    # shape_edge.sh_trans(n,d,crl)
    # show_window(3,crl)

    # # test for random shape
    # shape_ran = random_shape()
    # print(shape_ran.sh_name())
    # a = shape_ran.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for upper tri shape
    # shape_utri = u_tri()
    # print(shape_utri.sh_name())
    # a = shape_utri.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for lower tri shape
    # shape_ltri = l_tri()
    # print(shape_ltri.sh_name())
    # a = shape_ltri.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for letter U shape
    # shape_U = letter_U()
    # print(shape_U.sh_name())
    # a = shape_U.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for letter C shape
    # shape_C = letter_C()
    # print(shape_C.sh_name())
    # a = shape_C.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for letter L shape
    # shape_L = letter_L()
    # print(shape_L.sh_name())
    # a = shape_L.sh_trans(n,d,crl)
    # show_window(3,a)

    # # # test for cross up
    # # shape_cross_up = cross_up()
    # # print(shape_cross_up.sh_name())
    # # a = shape_cross_up.sh_trans(n,d,crl)
    # # show_(n,d,a)

    # # # test for cross down 
    # # shape_cross_down = cross_down()
    # # print(shape_cross_down.sh_name())
    # # a = shape_cross_down.sh_trans(n,d,crl)
    # # show_(n,d,a)

    # # # test for ortho devide & comb 
    # # m1 = ortho_devide_matrix(n,d,a)[0]
    # # m2 = ortho_devide_matrix(n,d,a)[1]
    # # m = ortho_comb_matrix(m1,m2)

    # # test for letter A shape
    # shape_A_left = letter_A_left()
    # print(shape_A_left.sh_name())
    # a = shape_A_left.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for letter A shape
    # shape_A_right = letter_A_right()
    # print(shape_A_right.sh_name())
    # a = shape_A_right.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for letter A shape
    # shape_A = letter_A()
    # print(shape_A.sh_name())
    # a = shape_A.sh_trans(n,d,crl)
    # #show_(np.shape(a)[0],np.shape(a)[0],a)

    # # test for letter E shape
    # shape_E = letter_E()
    # print(shape_E.sh_name())
    # e = shape_E.sh_trans(n,d,crl)
    # temp = ortho_comb_matrix(a,e)
    # show_(np.shape(temp)[0],np.shape(temp)[1],temp)

    shape_series(crl)

    # # test for triangle shape
    # shape_tri = triangle()
    # print(shape_tri.sh_name())
    # a = shape_tri.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for heart shape
    # shape_heart = heart_()
    # print(shape_heart.sh_name())
    # a = shape_heart.sh_trans(n,d,crl)
    # show_window(5,a)

    # # test for star shape
    # shape_tree = tree()
    # print(shape_tree.sh_name())
    # a = shape_tree.sh_trans(n,d,crl)
    # show_window(3,a)

    # # test for letter I shape
    # shape_I = letter_I()
    # print(shape_I.sh_name())
    # a = shape_I.sh_trans(n,d,crl)
    # show_window(5,a)
    

   


    
if __name__ == "__main__":
    main()




