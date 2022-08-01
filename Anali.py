"""
Anali programa komunikatzeko pythoneko liburutegia

"""
import os
import pipes
import sys
import io
import subprocess
import shlex

ANALI_PATH = os.environ["ANALI_PATH"]
#ANALI_CONF_PATH = os.environ["ANALI_CONF_PATH"]
BUFFER_TAM = 16384

class anali:
    """ Anali programaren instantzia """

    def __init__(self): #Se inicializa una conexion con la app anali mediante un pipe
        
        """Klase honen eraikitzailea

        Returns:
            Anali: klase honen instantzia
        
        """


        self.r1, self.w1 = os.pipe()
        self.r2, self.w2 = os.pipe()
        
        self.popen = subprocess.Popen(ANALI_PATH, shell= True, stdin= self.r1, stdout= self.w2 , text=True)


    def pedirPalabra(self, palabra):

        """ hitz bat eskatzen du Anali programari eta itzultzen duena itzultzen du

        Args:
            palabra (str): Aztertu nahi den textua

        Returns:
            str. aztetu den hitzaren emaitza, Anali hitzultzen duen bezala

        """

        os.write(self.w1, (palabra + "\n").encode("latin-1"))
        line = ""
        line = os.read(self.r2, BUFFER_TAM)
        return line.decode("latin-1")