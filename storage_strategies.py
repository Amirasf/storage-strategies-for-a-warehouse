#!/usr/bin/python
import random  
import pandas as pd     
import numpy as np  
import csv

class Command:
    def __init__(self,df):
        Num_comm=df.iloc[:,1]
        quantity=df.iloc[:,4]
        self.Num_comm=Num_comm  #command number
        self.quantity=quantity #product quantity
      
    #function that used to display all the products in your file
    def all_products(self):
        a=[]
        with open('client_command.csv') as csv_file:
            #Numero_commande=input ('entrez le numero de la commande que vous cherchez :' )
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:   
                a.append([row[2],row[4]])
        a.remove(a[0])
        a.sort()
                       
        j=1       
        while (j<len(a)):
            if (a[j-1][0] == a[j][0]):
                quant= int(a[j-1][1])
                quantt=int(a[j][1])
                quantt+= quant
                #a[j][0]=(f'{z} fois la commande :' , a[j][0])
                a[j][1]=quantt
                
                a.remove(a[j-1])                      
            else:
                j+=1
        return(a)

    #displaying not all products but products per command 
    def products_per_command(self,Numero_commande):
        a=[]
        with open('commande_client.csv') as csv_file:
            Numero_commande=input ('which command are you looking at?  :' )
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if (row[1]==str(Numero_commande)):
                         a.append([row[2],row[4]])
                         #return(a) 
        a.sort()
        j=1            
        while (j<len(a)):
            if (a[j-1][0] == a[j][0]):
                quant= int(a[j-1][1])
                quantt=int(a[j][1])
                quantt+= quant
                #a[j][0]=(f'{z} fois la commande :' , a[j][0])
                a[j][1]=quantt
                
                a.remove(a[j-1])                      
            else:
                j+=1
        return(a)
#the warehouse modelisation
class Warehouse:
    def __init__(self,L_R,L_A,pos_porte,nbre_cases,long_case,nbrelignes,nbrecol,couloir,capacité_init):
        self.L_R=L_R
        self.capacité_init=capacité_init
        self.L_A=L_A
        self.pos_porte=pos_porte  #door position
        self.long_case=long_case  
        self.nbre_cases=nbre_cases
        self.nbrelignes=nbrelignes
        self.nbrecol=nbrecol
        self.couloir=couloir
        #self.A=self.init_matrice()
    
    def matrix_with_sorted_dist(self,pos_porte):
         matrix=[]
         ref=[]
         #self.pos=pos
         #matrix = [[0 for x in range(w)] for y in range(2)] 
         for i in range (1,self.nbrelignes+1):
             for j in range(1,self.nbrecol+1):
                 if (i %(2)==0):
                        x=abs(self.pos_porte[1] -((i-1)*self.L_R+((i-1)*0.5*self.L_A )  ))
                 else:
                        x=abs(self.pos_porte[1] -(i*self.L_R+((i*0.5*self.L_A )  )))
                 matrix.append([(i,j),(self.couloir/2 +x+j*self.long_case),self.capacité_init,ref])
            
         matrix.sort(key=lambda x: x[1])
         return (matrix)

     #♥def nbre_cases(self,)
        
class Product(Warehouse): #not suuuuuuuure
    def __init__(self, L_R,L_A,pos_porte,nbre_cases,long_case,nbrelignes,nbrecol,couloir,capacité_init,référence,position):
        super().__init__(L_R,L_A,pos_porte,nbre_cases,long_case,nbrelignes,nbrecol,couloir,capacité_init)
        #df=pd.read_csv('commande_client.csv',sep=";",encoding = "ISO-8859-1")
 
        self.référence=référence
        self.position=position
        self.capacité_init=capacité_init
        
        
        '''matrix=self.matrix_with_sorted_dist(self,longueur,largeur)
        listeprod=self.products_per_command()
        for i in range(len(listeprod)):'''
            
    def nearest_position(self,matrix,liste):
        list_of_positions=[]
        first=liste[0]
        if (int(first[1])<matrix[0][2]):
            list_of_positions.append([first[0],matrix[0][0]])
            matrix[0][3].append(first[0])
        else:
            list_of_positions.append([first[0],matrix[0][0]])
            first[1]=int(first[1])-matrix[0][2]
            liste.insert(0,first)
            matrix[0][3].append(first[0])
            matrix.remove(matrix[0])
        liste.remove(first)
            
        w=1
        for a in liste:
            coord=list_of_positions[w-1][0]
            matrix= self.matrix_with_sorted_dist(coord)
            if (matrix[w][2]==self.capacité_init ): 
                if (int(a[1])<matrix[w][2]):
                    list_of_positions.append([a[0],matrix[w][0]])
                        #matrix.remove(matrix[w])
                    matrix[w][3].append(a[0])
                    matrix[w][2]=matrix[w][2]-int(a[1])
                else:
                    list_of_positions.append([a[0],matrix[w][0]])
                    a[1]=int(a[1])-matrix[w][2]
                    liste.insert(w,a)
                    matrix[w][3].append(a[0])
                    matrix.remove(matrix[w])
                    #w+=1 
            else:
                k=0
                while (k<len(matrix)):
                    if ((matrix[w][3]==a[0]) & (int(a[1]) < matrix[w][2])):
                        
                        list_of_positions.append([a[0],matrix[w][0]])
                    elif ((matrix[w][3]==a[0]) & (int(a[1])>matrix[w][2])):
                        list_of_positions.append([a[0],matrix[w][0]])
                        a[1]=int(a[1])-matrix[w][2]
                        liste.insert(w,a)
                        matrix.remove(matrix[w])
                    k+=1
            w+=1
        
        return(list_of_positions)
        
    def random_storage(self,lista,matrix):
        list_of_positions=[]
        qtite_produits_restante=[]
        w=0
        for a in lista:
            w+=1
            randrow=random.randint(0,self.nbrelignes)
            randcol=random.randint(0,self.nbrecol)
            if (int(a[1])<matrix[w][2]):
                
                matrix[w][0]=(randrow,randcol)
                list_of_positions.append([a[0],matrix[w][0]])
                matrix.remove(matrix[w])
                a[1]=matrix[w][2]-int(a[1])
                #qtite_produits_restante.append([a[0],a[1]])

            else:
                matrix[w][0]=(randrow,randcol)
                list_of_positions.append([a[0],matrix[w][0]])
                a[1]=int(a[1])-matrix[w][2]
                lista.append(a)
                matrix.remove(matrix[w])
                
                     
        
        return (list_of_positions)

    
    def stockage_dedie(self,commande,listofprod): 
        matrix=[]

        for i in range (1,self.nbrelignes+1):
            for j in range (1,self.nbrecol+1):
                matrix.append((i,j))
        
        qtite_totale=0
        for i in range (len(listofprod)):
            qtite_totale=qtite_totale+int(listofprod[i][1])
            
        start=0
        dictio=[]
        for k in range (len(listofprod)):
            Qproduct=int(listofprod[k][1])
            nbre_cases_occupées=(Qproduct /qtite_totale)*self.nbre_cases
            if type(nbre_cases_occupées)==float :
                nbre_cases_occupées+=1
            last_position=start+nbre_cases_occupées
            dictio.append([listofprod[k][0],[]+[matrix[int(start):int(last_position)]]])
            start=last_position
        print(dictio)
        list_of_positions=[]
        while i < (len(commande)):
          if commande[i][0] in dictio :
             for j in range (len(dictio[i][0])):
                 if (int(commande[i][1])>self.capacité_init):
                     list_of_positions.append(dictio[commande[i][0]][j])
                     commande[i][1]=int(commande[i][1])-self.capacité_init
                     liste.insert(i,commande[i])
                 else:
                     list_of_positions.append(dictio[commande[i][0]][j])
          i+=1
        return (list_of_positions)
       
    #mrigla
    def sales_volume_storage(self,liste,df2,matrix):
        VV=df2.iloc[:,0]
        aa=[]
        i=0
        for i in range (len(VV)):
             for a in liste:
               
                   if (VV[i]==a[0]):
                        aa.append(a)
        return(self.nearest_position(matrix,aa))
               
         
                    
    
def main():
    
    df=pd.read_csv('client_command.csv',sep=";",encoding = "ISO-8859-1")  #enter your client comand as a csv file
    df2=pd.read_csv('sales_volumes.csv',sep=";",encoding = "ISO-8859-1") 
    cmd=Command(df)
    products=cmd.all_products()
    entrepot=Warehouse(1,1,(0,5),300,1,20,10,2,600)
    prod = Product(1,1,(0,5),300,1,20,10,2,600, 'ab12',[])
    matrice=entrepot.matrix_with_sorted_dist((0,5))
    #to test sales volume storage strategy
    print(prod.sales_volume_storage(products,df2,matrice))
    #to test random strategy :
    print(prod.random_storage(products,matrice))
    # nearest position strategy
    print(prod.nearest_position(matrice,products))
    
if __name__ == '__main__':
    main()                 

    