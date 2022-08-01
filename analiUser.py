"""
Erabiltzaileak terminaletik liburutegia erabiltzeko menua
"""

from subprocess import STDOUT
from Analisis import *
import sys



def menu():

    """
        Menu bat stdout, imprimtzen du eta erabiltzailearen input-a hartzen du    
    """


    inp = (input("hitz bat eskatuko dugu\n\n\n\n"))
    print("="*40)

    inp = separarInpParam(inp)
    if len(inp) > 1:
        params = inp[1:]
    else:
        params = []
    inp = inp[0]
        
    while "exit" not in params:

        anum = 0
        hitza = analizarPalabra(inp)
        print(f"Analisia burutua\nAnalisis kopurua: {len(hitza.analisia)}\nAnalisiaren fasea: {hitza.analiFasea}")
        print("="*40)
        print()

        while "berria" not in params and inp != "":

            if "eg" in params:
                params = []

            if "i" in params:
                anumaux= anum
                try:
                    anum = int(input("ikusi nahi den analisiaren indizea: "))
                except:
                    anum = anumaux

                if anum >= len(hitza.analisia) or anum<0:
                    print("indize okerra")
                    anum = anumaux
                params.remove("i")

            if params == []: #Kasu basikoa == lehenbiziko anaisiaren ezaugarri guztiak
                print(hitza.getinformationIndex(anum))
                #print(hitza.analisia[0].getKategoria())

            if "help" in params:
                printLaguntza()
                params = []
            if "hurrengoa" in params:
                anum = anum + 1
                if anum >= len(hitza.analisia):
                    anum = 0
                params.remove("hurrengoa")
                print(f"indizea = {anum}")
                continue
            if "ezb" in params and len(params) == 1:
                auxezb = []
                for i in range(len(hitza.analisia)):
                    if hitza.getinformationIndex(i) not in auxezb:
                        auxezb.append(hitza.getinformationIndex(i))
                for c in auxezb:
                    print(c)
            if "ezb" in params and len(params) > 1:
                if "Sarrera" not in params:
                    params.append("Sarrera")
                auxezb = []
                for i in range(len(hitza.analisia)):
                    if hitza.getinformationIndex(i) not in auxezb:
                        auxezb.append(hitza.getinformationIndex(i))
                for c in auxezb:
                    print(c)
            if "g" in params and len(params) == 1:
                for i in range(len(hitza.analisia)):
                    print(hitza.getinformationIndex(i))
                    anum = 0
            #ir haciendo una lista de todos los keys y quitarlos de params y depues llamar a la funcion con esa lista de keys
            if "g" in params and len(params) > 1:
                params.remove("g")
                if "Sarrera" not in params:
                    params.append("Sarrera")
                for i in range(len(hitza.analisia)):
                    print(hitza.getinformationIndexKeys(i,params))
                    anum = 0
            elif len(params) > 0 and "g" not in params and "ezb" not in params:
                if "Sarrera" not in params:
                    params.append("Sarrera")
                print(hitza.getinformationIndexKeys(anum,params))
                    
            #si es hurrengo SOLO hurrengoa, guardar los parametros
            print("="*40)
            print()
            paramsAnt = params
            params = (input("aginduen zain: "))
            params = params.replace(" ","")
            if params.count("$") == 0:
                params = []
                continue
            params = params.split("$")
            try:
                params.remove("")
            except:
                pass

           

            if "hurrengoa" in params and len(params) == 1:
                params = ["hurrengoa"] + paramsAnt

            print("\n")

        #depende de los parametroshacemos una cosa u otra
        inp = (input("hitz bat eskatuko dugu: "))

        inp = separarInpParam(inp)
        if len(inp) > 1:
            params = inp[1:]
        else:
            params = []
        inp = inp[0]

def separarInpParam(inp): #devuelve un array [inp, param1, param2, ... , paramn]
    """
    Sarrera et parametroak banatzen ditu

        Args:
       inp(str): Erabitzaileak sartutako testua

        Returns:
        array[str]: parametro guztiak diturn zerrenda
    """
    auxinp = []
    inp = inp.split("$")
    for c in range(len(inp)):
        if c > 0:
            auxinp.append(c.replace(" ",""))
        else:
            if inp[c][len(inp[c]) - 1] == " ":
                inp[c] = inp[c][:len(c) -1]
            auxinp.append(inp[c]) 
    return auxinp

def printLaguntza():

    """
        Sarrera baten analisi baten informazioa itzultzen du

        Komando guztiak imprimatzen ditu
    """
    print("Erabiltzen ahal diren komando guztiak:")
    print("\t$hurrengoa-> Hitzaren hurrengo analisia erakusten du\n\tEzin da $g-rekin erabili\nBeste komandoren bat idazten ez bada lehengo informazio berdina erakutsiko du\nAdibidez:\n etxea $KAT %AZP \n $hurrengoa \n bigarren analisiaren kategoria eta azpikategoria idatziko da. Aldatu nahi bada $hurrengoa-az gain nahi diren parametroak idatzi")
    print("\t$berria-> Hitz berri baten analisia nahi bada")
    print("\t$eg-> Analisiaren ezaugarri guztiak erakusten ditu")
    print("\t$i-> Ikusi nahi den analisiaren indizea eskatzen da")
    print("\t$ezb-> Ezberdinak diren analisia bakarrik erakusten dira")
    print("\t$g-> Analisi eta ezaugarri guztiak erakusten dira")
    print("\nOndoren, ikusi nahi diren ezaugarriak erakusteko hurrengo parametroak idatzi daitezke.\nADB:$KAT $AZP\n parametro hauek, analizatzen ari den hitzaren kategoria (KAT) eta azpikategoria erakutsiko ditu") 
    print("\t$KAT :Katergoria")
    print("\t$AZP :Azpikategoria")
    print("\t$ERAAZP :Eratorriaren azpikategoria")
    print("\t$BIZ : Biziduna/bizigabea")
    print("\t$ADOIN :Aditz oina")             
    print("\t$LAGM :Laguntzaile mota")
    print("\t$ERR :Erroa")
    print("\t$NOR :Nor")
    print("\t$NORI :Nori")
    print("\t$NORK :Nork")
    print("\t$MDN :Modu denbora")
    print("\t$ASP :Aspektua")
    print("\t$OSA1 :lehenbiziko osagarria")
    print("\t$OSA2 :bigarren osagarria")
    print("\t$PLU :Plurala")
    print("\t$IZAUR :Izenaren aurretik")
    print("\t$PER :Pertsona")                           
    print("\t$NUM :Numeroa")
    print("\t$RARE :Arraroa")
    print("\t$ADBM :Adberbio mota")
    print("\t$ADM :Aditz mota")
    print("\t$ADZ :Adierazia")
    print("\t$ATZL:Atzizki lista")
    print("\t$AUR :Aurrizkia")
    print("\t$AZPERD :Azpikategorizazio-eredua")
    print("\t$ELK :Elkarketa mota")
    print("\t$ERAKAT :Eratorriaren kategoria")
    print("\t$ERL :Erlazioa")
    print("\t$Estandarrak :Estandarrak")
    print("\t$HIT :Hitanoa")
    print("\t$HOBETSI1 :Hobetsitako sarrerak")
    print("\t$Hobetsiak :Hobetsiak")
    print("\t$HURB :Hurbiltasun maila")
    print("\t$KAS :Kasua")
    print("\t$KLM :Klausula-muga")
    print("\t$MAI :Gradu maila")
    print("\t$MOD :Modaltasuna")
    print("\t$MTKAT :Metakategoria")
    print("\t$MUG :Mugatasuna")
    print("\t$NEUR :Neurgarria")
    print("\t$NMG :Numeroa-mugatasuna")
    print("\t$OIN :Oinarria")
    print("\t$POS :Posizioa")
    print("\tZENB :Zenbakarria")
    print("\tAldaera :Aldaera")
    print("\tFSL :Analisiaren kodeak")
    print("\tERROR-KODE :Analisian gertatu diren erroreak")                                                                                    

if __name__ == "__main__":
    initializeAnalizador()
    while True:
        try:
            menu()
        except KeyboardInterrupt:
            print()
            sys.exit()
        except:
            continue