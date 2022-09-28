import time 
import matplotlib.pyplot as plt
import argparse 
import logging
import os
logging.basicConfig(level=logging.INFO)


 
def apri(path):
    """apre il file avendo in input il path.
    """
    
    # Basic sanity check: make sure that the file_argument points to an
    # existing text file.
    assert path.endswith('.txt')
    assert os.path.isfile(path)
    
    
    logging.info(f'Sto aprendo il file {path}')
    #ora apro e leggo il libro
    with open(path) as input_file:
        libro = input_file.read()
     
    logging.info(f'Caricamento completato {len(libro)}')
     
    return libro    
     
def conta(libro):
   """conta le lettere del libro
   """
   #creo stringa alfabeto
   alfa = 'abcdefghijklmnopqrstuvwxyz'
   #creo dizionario e lo azzero 
   diz = {}
   for i in alfa:
       diz[i] = 0
         
   #devo ciclare su tutto il libro scritto in minuscolo
   for ch in libro.lower():
       if ch in alfa:
           diz[ch] += 1 
     
   #conto tutti i caratteri
   totalchar = float(sum(diz.values()))
     
   #ottengo la percentuale di ogni char
   for i in alfa:
       diz[i] /= totalchar
         
   #stampo su shell i valori del dizionario
   for ch, num in diz.items():
       print(f'{ch} {num*100:.3f}')
         
   return diz
     
def isto(diz):
   """crea istogramma occorrenze su lettere
   """
   plt.figure(1)
   plt.bar(diz.keys(), diz.values(), align = 'center')
   plt.show()
             
     
if __name__ == '__main__':    
   t0 = time.time()
   parser = argparse.ArgumentParser(description='codiche che conta le lettere di un testo')
   parser.add_argument('infile', help='path del file da leggere' )
   parser.add_argument('-isto', '--istogramma', action = 'store_true', help='stampa istogramma' )
   args = parser.parse_args()
   
   book = apri(args.infile)
   diz = conta(book) 
   
   dt= time.time()-t0
   logging.info(f'Tempo trascorso: {dt}')    
   
   if args.istogramma:
       isto(diz)
   
     
