"""
Anali liburutegiak lortzen dituen emaitzak parseatzeko liburutegia 


"""

import Anali
import time
import re

anali = None

def initializeAnalizador():

    """
    Anali ren instantzia bat sortzen du

    """
    global anali
    
    anali = Anali.anali()
    #time.sleep(20)

def analizarPalabra(inp): #Devuelve un objeto de clase analisia

    """ textu bat aztertzen du eta irteera parseatzen du

    Args:
        inp (str): aztertuko den textua

    Returns:
        analisia: objektu bat itzultzen du aztertu diren sarrera guztiekin

    """
    try:
        inp = __parseinput(inp)
        sarrerak = []
        inp = inp.split()
        for l in inp: #input-ko hitz bakoitzerako
            line = anali.pedirPalabra(l)
            line = line.split("\n")
            x = 2
            fas = line[0] #Analisiaren fasea harrapatzeko
            
            while (line[x] != ""): #Analisi bakoitzerako
                    
                aux = line[x].split("\t")[1]
                aux1 = __getSimple(aux)
                s = Sarrera()
                for l in aux1:
                    aux1splited = re.findall('\[(.*?)\]',l)
                    aux1splited = __parse(aux1splited,inp[0])
                    lema = Ezaugarriak(aux1splited)
                    s.lemaGehitu(lema)
                    
                #s = Sarrera(aux1splited)
                sarrerak.append(s)
                x += 1
                
        hitza = analisia(sarrerak,fas)
        return hitza
    except:
        return analisia([],None)

def getAnalisis(): #Imprime la palabra pedida por la salida estandar, queda a la espera de una nueva palabra
    
    """ Terminaletik irakurtzen ditu esaldiak/hitzak. Aztertu dituenean beste hitz baten esperoan gelditzen da

        Irteera estandarrera idazten ditu analisiak

        **exit** hitzarekin programak bukatzen da
    """
    inp = (input("hitz bat eskatuko dugu\n"))
        
    while inp != "exit":
        hitza = analizarPalabra(inp)
        srr =  hitza.getinformation()
        for s in srr:
            print(s)
        print()
        inp = (input("hitz bat eskatuko dugu\n"))
        inp = __parseinput(inp)

#parseamos la entrada, myusculas y Ñ
def __parseinput(inp):
    """ **PRIBATUA**

    Analik aztertzen ez dituen karaktereak moldatzen ditu

    ñ -> 8

    <MAYUS> -> 9<minus>

    **KONTUZ** zenbakiak ez pasa ez ditu irakurtzen
    
    adibidez: 14 beharran hamalau idatzi

    Args:
        inp (str): moldatu nahi den textua

    Returns:
        str : lan egiteko textua

    """
    aux = inp
    aux = aux.replace("Ñ","98")
    aux = aux.replace("ñ","8")
    for c in inp:
        if c.isupper():
            aux = aux.replace(c,f"9{c.lower()}")
    
    aux2 = aux
    for h in aux.split():
        if h.isnumeric():
            aux2 = aux2.replace(h, stringtoInt(h))
            pass
    #print(f"numero = {inp} \nconvertido = {aux2}")
    return aux2


def stringtoInt(s):

    """
        Pasatzen zaion zenbakia, zenbaki horre izenera pasatzen du:
        ADB:
            13 -------> hamahiru
        

        Args:
            s(str): textura pasako den zenbakia

        Returns:
            str : zenbakiaren izena

    """

    bat = ["zero", "bat", "bi", "hiru", "lau", "bost", "sei", "zazpi", "zortzi", "bederatzi"]

    hamar = ["", "hamaika", "hamabi", "hamairu", "hamalau", "hamabost", "hamasei", "hamazazpi", "hemezortzi", "hemeretzi"]

    hamarko = ["","hamar", "hogei", "hogeita hamar", "berrogei", "berrogehita hamar", "hirurogei", "hirurogeita hamar", "laurogei", "laurogeita hamar"]

    ehun = ["", "ehun", "berrehun", "hirurehun", "laurehun", "bostehun", "seiehun", "zazpiehun", "zortziehun", "bederatziehun"]

    pos = 0

    #aurreko zeroak kentzeko
    for n in s:
        if n == "0" and (pos + 1) < len(s):
            pos = pos + 1
        else:
            break
    
    s = s[pos:] #Ezker aldeko zeroak kenduta

    if len(s) == 1:
        return bat[int(s)]

    if len(s) == 2:
        if s[1] == "0":
            return hamarko[int(s[0])]
        else:
            if s[0] == "1":
                return hamar[int(s[1])]
            elif int(s[0]) % 2 == 1:
                return hamarko[int(s[0]) - 1] + "ta " + hamar[int(s[1])]
            elif  int(s[0]) % 2 == 0:
                return hamarko[int(s[0])] + "ta " + bat[int(s[1])]

    if len(s) == 3:
        if s[1] == "0" and s[2] == "0":
            return ehun[int(s[0])]
        else:
            return ehun[int(s[0])] + " eta " + stringtoInt(s[1:])
    
    if len(s) == 4:
        if s[1] == "0" and s[2] == "0" and s[3] == "0":
            if s[0] == "1":
                return "mila"
        if s[1] == "0":
            if s[0] == "1":
                return "mila eta " + stringtoInt(s[1:])
            else:
                return bat[int(s[0])] + " mila eta " + stringtoInt(s[1:])
        if s[2] == "0" and s[3] == "0":
            if s[0] == "1":
                return "mila eta " + stringtoInt(s[1:])
            else:
                return bat[int(s[0])] + " mila eta " + stringtoInt(s[1:])
        if s[0] == "1":
            return "mila " + stringtoInt(s[1:])
        else:        
            return bat[int(s[0])] + " mila " + stringtoInt(s[1:])

    if len(s) == 5:
        if s[2] == "0" and s[3] == "0" and s[4] == "0":
            return stringtoInt(s[:2]) + " mila"
        if s[2] == "0" or (s[3] == "0" and s[4] == "0"):
            return stringtoInt(s[:2]) + " mila eta " + stringtoInt(s[2:])

        return stringtoInt(s[:2]) + " mila " + stringtoInt(s[2:])

    if len(s) == 6:

        if s[3] == "0" and s[4] == "0" and s[5] == "0":
            return stringtoInt(s[:3]) + " mila"

        if s[3] == "0" or (s[4] == "0" and s[5] == "0"):
            return stringtoInt(s[:3]) + " mila eta " + stringtoInt(s[3:])
            
        return stringtoInt(s[:3]) + " mila " + stringtoInt(s[3:])



def __parse(lista,inp):
    """**PRIBATUA**

    Funtzio auxiliarra

    Analiren irteera parseatzen du "Sarrera" objektua sortu ahal izateko

    Args:
        lista(array[str]): analisi baten ezaugarria guztiak, ondorengo formarekin [Sarrera_etxea---1--+, KAT_IZN,...]

    Returns:
        array[str]: analisia parseatua [[sarrera,etxea],[KAT,IZN]]


    """
    dlista = []
    for i in range(len(lista)):
        
        lista[i] = lista[i].replace("[","")
        if "Sarrera" in lista[i] and not "ADZ" in lista[i]:
            lista[i] = lista[i][:len(lista[i])-6]
        if "OSA1" in lista[i] or "OSA2" in lista[i]:
            lista[i] = lista[i][:len(lista[i])-3]
        if "ADZ" in lista[i]:
            lista[i] = lista[i][:len(lista[i])-3]
            strADZ = ""
            for j in range(len(lista[i].split("_")[1:])):
                if j == 0:
                    strADZ = lista[i].split("_")[j] + "_"
                else:
                    if lista[i].split("_")[1:][j] != "":
                        strADZ = strADZ + lista[i].split("_")[1:][j] + " "
            lista[i] = strADZ[:len(strADZ) - 1 ]
        if "Estandarrak" in lista[i] or "Hobetsiak" in lista[i]:
            #print(f"lista = {lista[i]}")
            lista[i] = lista[i][:len(lista[i])-6]
            strADZ = ""
            for j in range(len(lista[i].split("_")[1:])):
                if j == 0:
                    strADZ = lista[i].split("_")[j] + "_"
                else:
                    if lista[i].split("_")[1:][j] != "":
                        strADZ = strADZ + lista[i].split("_")[1:][j] + " "
            lista[i] = strADZ[:len(strADZ) - 1 ]
        if "ADOIN" in lista[i]:
            strADZ = ""
            for j in range(len(lista[i].split("_"))):
                if j == 0:
                    strADZ = lista[i].split("_")[j] + "_"
                else:
                    if lista[i].split("_")[j] != "":
                        strADZ = strADZ + lista[i].split("_")[j] + " "
            lista[i] = strADZ[:len(strADZ) - 1 ]
        if "Aldaera" in lista[i]:
            lista[i] = lista[i][:len(lista[i])-6]
        if "STD" in lista[i] and "Estandarrak" not in lista[i]:
            lista[i] = lista[i][:len(lista[i])-6]
            
        if "FSL" in lista[i]:
            lista[i] = lista[i].replace("]", "")
            lista[i] = "FSL_" + lista[i][8:]
            part1 = lista[i].split("_")[0]
            part2 = lista[i].split("_")[1:]
            part2Junt = ""
            for p in part2:
                part2Junt = part2Junt + "_" + p
            parts = []
            parts.append(part1)
            parts.append(part2Junt[1:])
        if "FS" in lista[i] and not "FSL" in lista[i]:
            lista[i] = lista[i].replace("]", "")
            lista[i] = "FSL_" + lista[i][4:]
            part1 = lista[i].split("_")[0]
            part2 = lista[i].split("_")[1:]
            part2Junt = ""
            for p in part2:
                part2Junt = part2Junt + "_" + p
            parts = []
            parts.append(part1)
            parts.append(part2Junt[1:])
        #print(lista[i])

        if "FS" in lista[i]:
            dlista.append(parts)
        else:
            dlista.append(lista[i].split("_")) #Aqui mirar si es ADL o FL

    return dlista

def __getSimple(s):
    """
    Analisiaren lehenbiziko zatia hartzen du +0,+k...horiek gabe

    Args:
        s(str): testu osoa

    Returns:
       str: testuaren zati sinplea

    """

    #Con esto quitamos la primera parte La entrada (fuera de los corchetes)
    def gety(pos = 0):
        y = pos
        for c in s[pos:]:
            if c == "[":
                break
            if c == "+":
                return -1
            y = y + 1
        return y

    ret = []
    x = 0 #representa cuantas llaves lee [
    y = gety()
    pos = y
    acabado = False

    while y < len(s):
        for c in s[y:]:

            if c == "[":
                x = x + 1
            elif c == "]":
                x = x - 1

            if x == 0:
                ret.append(s[y:pos+1])
                break
            
            pos = pos + 1
        y = gety(pos)
        if y == -1:
            break
        #print(f"len de s = {len(s)} y y = {y}")
        pos = y
    #print(f" esto es lo que devuelve {ret}")    
    return ret
    
def keyToString(s1,s2):
        """ Analik itzultzen duen kodeak itzultzen ditu

        Args:
            s1(str): pythoneko hiztegiko KEY
            s2(str): pythoneko hiztegiko ITEM

        Returns:
            str. KEY eta ITEM horien string-a

            **BESTENAZ** ez badu aurkiten errors karpetan fitxategi bat sorten du aurkitu ez duen [key, item] dupla batekin

        """
        if s1 == "Sarrera":
            return "Sarrera = {}, ".format(s2)

        if s1 == "KAT":
            if s2 == "IZE":
                return "Kategoria = izena, "
            if s2 == "ADJ":
                return "Kategoria = adjektiboa, "    
            if s2 == "ADI":
                return "Kategoria = aditza, "
            if s2 == "ADB":
                return "Kategoria = adberbioa, "
            if s2 == "DET":
                return "Kategoria = determinatzailea, "
            if s2 == "IOR":
                return "Kategoria = izenordaina, "
            if s2 == "LOT":
                return "Kategoria = lotura, "
            if s2 == "PRT":
                return "Kategoria = partikula, "
            if s2 == "ITJ":
                return "Kategoria = interjekzioa, "
            if s2 == "BST":
                return "Kategoria = bestelakoa, "
            if s2 == "ADL":
                return "Kategoria = aditz laguntzaile, "
            if s2 == "ADT":
                return "Kategoria = aditz sintetikoa, "
            if s2 == "HAOS":
                return "Kategoria = haul osagaia, "
            if s2 == "LAB":
                return "Kategoria = laburdura, "
            if s2 == "SIG":
                return "Kategoria = sigla, "
            if s2 == "SNB":
                return "Kategoria = sinboloa, "
            if s2 == "MAR":
                return "Kategoria = elkarketa marra,"
            if s2 == "AMM":
                return "Kategoria = aditz-mota morfema, "
            if s2 == "ASP":
                return "Kategoria = aspektu-morfena, "
            if s2 == "ATZ":
                return "Kategoria = atzizki lexikala, "
            if s2 == "AUR":
                return "Kategoria = aurrizki lexikala, "
            if s2 == "DEK":
                return "Kategoria = deklinabide-morfena, "
            if s2 == "ELI":
                return "Kategoria = elipsia, "
            if s2 == "ERL":
                return "Kategoria = erlazio-morfena, "
            if s2 == "GRA":
                return "Kategoria = graduatzailea, "
            if s2 == "HAOS":
                return "Kategoria = hitz-anitzeko osagaia, "
      


        if s1 == "AZP" or s1 == "ERAAZP":
                
            if s1 == "AZP":
                aux = ""
            else:
                aux = "Eratorriaren "

            if s2 == "ARR":
                return aux + "azpikategoria = arrunta, "
            if s2 == "IZB":
                return aux + "azpikategoria = pertsona-izen berezia, " 
            if s2 == "LIB": 
                return aux + "azpikategoria = leku-izen berezia, "
            if s2 == "IZO": 
                return aux + "azpikategoria = izenondoa, "
            if s2 == "IZL": 
                return aux + "azpikategoria = izenlaguna, "
            if s2 == "SIN": 
                return aux + "azpikategoria = sinplea, "
            if s2 == "ADK": 
                return aux + "azpikategoria = konposatua, "
            if s2 == "ADP":
                return aux + "azpikategoria = perifrastikoa, "
            if s2 == "FAK":
                return aux + "azpikategoria = faktitiboa, "
            if s2 == "GAL": 
                return aux + "azpikategoria = galdetzailea, "
            if s2 == "IND": 
                return aux + "azpikategoria = indartua, "
            if s2 == "DZH": 
                return aux + "azpikategoria = zehaztua, "
            if s2 == "DZG":
                return aux + "azpikategoria = zehaztugabea, "
            if s2 == "ORO":
                return aux + "azpikategoria = orokorra, "
            if s2 == "MGB":
                return aux + "azpikategoria = mugagabea, "
            if s2 == "ELK":
                return aux + "azpikategoria = elkarkaria, "
            if s2 == "LOK":
                return aux + "azpikategoria = lokailua, "
            if s2 == "JNT":
                return aux + "azpikategoria = juntagailua, "
            if s2 == "BIH":
                return aux + "azpikategoria = bihurkaria, "
            if s2 == "BAN":
                return aux + "azpikategoria = banatzailea, "
            if s2 == "ELK":
                return aux + "azpikagoria = elkarkaria, "
            if s2 == "ERKARR":
                return aux + "azpikagoria = erakusle arrunta, "
            if s2 == "ERKIND":
                return aux + "azpikagoria = erakusle indartua, "
            if s2 == "IZGGAL":
                return aux + "azpikagoria = zehaztugabea galdetzailea, "
            if s2 == "IZGMGB":
                return aux + "azpikagoria = zehatzugabe mugagabea, "
            if s2 == "MEN":
                return aux + "azpikagoria = menderagailua, "
            if s2 == "NOLARR":
                return aux + "azpikagoria = nolakotzaile arrunta, "
            if s2 == "NOLGAl":
                return aux + "azpikagoria = nolakotzaile galdetzailea, "
            if s2 == "ORD":
                return aux + "azpikagoria = zenbatzaile zehaztu ordinala, "
            if s2 == "PERARR":
                return aux + "azpikagoria = pertsona-izenordain arrunta, "
            if s2 == "PERIND":
                return aux + "azpikagoria = pertsona-izenordain indartua, "
            if s2 == "ZKI":
                return aux +     "azpikagoria = izen zenbakia, "
       
        if s1 == "BIZ":

            if s2 == "-":
                return "Bizigabea = Bai, "
            if s2 == "+":
                return "Biziduna = Bai, "
        
        if s1 == "ADOIN":
            return f"aditz oina = {s2}, "

        if s1 == "LAGM":
            return f"laguntzaile mota = {s2}, "
        
        if s1 == "ERR":
            return f"erroa = {s2}, "

        if s1 == "NOR":
            return f"nor = {s2}, "
        
        if s1 == "NORI":
            return f"nori = {s2}, "
        
        if s1 == "NORK":
            return f"nork = {s2}, "
        
        if s1 == "MDN":
            if s2 == "A1":
                return f"Modu-Denbora = Indikatibozko orainaldia, "
            if s2 == "A2":
                return f"Modu-Denbora = Indikatibozko geroaldia, "
            if s2 == "A3":
                return f"Modu-Denbora = subjuntibuzko orainaldia, "
            if s2 == "A4":
                return f"Modu-Denbora = Indikatibozko baldintza, "
            if s2 == "B1":
                return f"Modu-Denbora = Indikatibozko lehenaldia, "
            if s2 == "B2":
                return f"Modu-Denbora = Indikatibozko baldintza (ondorioa, orain-gero), "
            if s2 == "B3":
                return f"Modu-Denbora = Indikatibozko baldintza (ondorioa, lehen), "
            if s2 == "B4":
                return f"Modu-Denbora = Indikatibozko baldintza (aurrekoa), "
            if s2 == "B5":
                return f"Modu-Denbora = Subjuntibuzko baldintza eta alegiazkoa, "
            if s2 == "B6":
                return f"Modu-Denbora = subjuntibozko baldintza (lehenaldia), "
            if s2 == "B7":
                return f"Modu-Denbora = Ahalezko lehenaldia, "
            if s2 == "B8":
                return f"Modu-Denbora = Ahalezko lehenaldi urruna, "
            if s2 == "B5A":
                return f"Modu-Denbora = Subjuntibozko ahalegiazkoa, "
            if s2 == "B5B":
                return f"Modu-Denbora = Subjuntubozko lehenaldia, "
            
        if s1 == "ASP":
                
            if s2 == "EZBU":
                return f"Aspektua = ez-burutua, "
            if s2 == "GERO":
                return f"Aspektua = etorkizuna, "
            if s2 == "BURU":
                return f"Aspektua = partizipioa, "
            if s2 == "PNT":
                return f"Aspektua = Puntukaria, "
        
        if s1 == "OSA1":
            return f"lehenbiziko osagarria = {s2}, "
        
        if s1 == "OSA2":
            return f"Bigarren osagarria = {s2}, "
        
        if s1 == "PLU":
            if s2 == "+":
                return "plurala = Bai, "
            if s2 == "-":
                return "plurala = Ez, "

        if s1 == "IZAUR":
            if s2 == "+":
                return "izenaren aurretik = Bai, "
            if s2 == "-":
                return "izenaren aurretik = Ez, "

        if s1 == "PER":
            return f"Pertsona = {s2}, "

        if s1 == "NUM":
            if s2 == "S":
                return "Numeroa = singularra, "
            if s2 == "P":
                return "Numeroa = plurala, "
            if s2 == "PH":
                return "Numeroa = Plural hurbila, "
        
        if s1 == "RARE":
            if s2 == "ANB":
                return "Arraroa = kategoria honetan, "
            if s2 == "ABT":
                return "Arraroa = absolutoa (hitz laburrak), "
            if s2 == "LEX":
                return "Arraroa = lexikala, "

        if s1 == "ADBM":
            if s2 == "DENB":
                return "Adberbio mota = denborazkoa, "
            if s2 == "MOD":
                return "Adberbio mota = moduzkoa, "
            if s2 == "GRAD":
                return "Adberbio mota = graduatzailea, "
            if s2 == "LEK":
                return "Adberbio mota = lekuzkoa, "
            
        if s1 == "ADM":
            if s2 == "ADOIN":
                return "Aditz mota = aditz-oina, "
            if s2 == "PART":
                return "Aditz mota = partizipioa, "
            if s2 == "ADOIN":
                return "Aditz mota = aditz-izena, "
            
        if s1 == "ADZ":
            return f"adierazia = {s2}, "

        if s1 == "ATZL":
            return f"atzizki lista = {s2}, "

        if s1 == "AUR":
            return f"aurrizki = {s2}, "
        
        if s1 == "AZPERD":
            return f"Azpikategorizazio-eredua = {s2}, "
        
        if s1 == "ELK":
            if s2 == "I+I":
                return "elkarketa mota = izena + izena, "
            if s2 == "I+ADJ":
                return "elkarketa mota = izena + adjektiboa, "
            if s2 == "ADI+ADI":
                return "elkarketa mota = aditza + aditza, "
        
        if s1 == "ERAKAT":
            return f"Eratorriaren kategoria = {s2}, "
        
        if s1 == "ERL":
            if s2 == "BALD":
                return f"Erlazioa = bakdintza, "
            if s2 == "DENB":
                return f"Erlazioa = denborazkoa, "
            if s2 == "ESPL":
                return f"Erlazioa = esplikatiboa, "
            if s2 == "HELB":
                return f"Erlazioa = helburuzkoa, "
            if s2 == "KAUS":
                return f"Erlazioa = kausala, "
            if s2 == "KONT":
                return f"Erlazioa = kontzesiboa, "
            if s2 == "MOD":
                return f"Erlazioa = moduzkoa, "
            if s2 == "ERLT":
                return f"Erlazioa = erlatibozkoa, "
            if s2 == "ZHG":
                return f"Erlazioa = zehargaldera, "
            if s2 == "MOS":
                return f"Erlazioa = menderagailu-osagaia, "
            if s2 == "MOD/DENB":
                return f"Erlazioa = modu-Denborazkoa, "
            if s2 == "EMEN":
                return f"Erlazioa = emendiozkoa, "
            if s2 == "ONDO":
                return f"Erlazioa = ondoriozkoa, "
            if s2 == "AURK":
                return f"Erlazioa = aurkarizkoa, "
            if s2 == "KONPL":
                return f"Erlazioa = konpletiboa, "
            if s2 == "HAUT":
                return f"Erlazioa = hautakaria, "
            if s2 == "MOTIB":
                return f"Erlazioa = motibatiboa, "
        
        if s1 == "Estandarrak":
            return f"estandarrak = {s2}, "
        
        if s1 == "HIT":
            return f"Hitanoa = {s2}, "
        
        if s1 == "HOBETSI1":
            return f"Hobetstako sarrera = {s2}, "
        
        if s1 == "Hobetsiak":
            return f"Hobetsiak = {s2}, "
        
        if s1 == "HURB":
            return f"Hurbiltasun maila = {s2},"

        if s1 == "KAS":
            if s2 == "ABL":
                return "Kasua = ablatiboa, "
            if s2 == "ABU":
                return "Kasua = adlatibo bukatuzkoa, "
            if s2 == "ABZ":
                return "Kasua = adlatibo bide zuzenezkoa, "
            if s2 == "ALA":
                return "Kasua = adlatiboa, "
            if s2 == "SOZ":
                return "Kasua = soziatiboa, "
            if s2 == "DAT":
                return "Kasua = datiboa, "
            if s2 == "DES":
                return "Kasua = destinatiboa, "
            if s2 == "ERG":
                return "Kasua = ergatiboa, "
            if s2 == "GEL":
                return "Kasua = genitiboa (leku denborazkoa), "
            if s2 == "GEN":
                return "Kasua = genitiboa, "
            if s2 == "INE":
                return "Kasua = inesiboa, "
            if s2 == "INS":
                return "Kasua = instrumetala, "
            if s2 == "MOT":
                return "Kasua = motibatiboa, "
            if s2 == "ABS":
                return "Kasua = absolutiboa, "
            if s2 == "PAR":
                return "Kasua = partitiboa, "
            if s2 == "PRO":
                return "Kasua = prolatiboa, "
            if s2 == "BNK":
                return "Kasua = banakaria, "
            if s2 == "DESK":
                return "Kasua = deskribatzailea, "

        if s1 == "KLM":
            if s2 == "HAS":
                return "Klausula-muga = klausula hasiera, "
            if s2 == "AM":
                return "Klausula-muga = klausula amaia, "
            if s2 == "HA":
                return "Klausula-muga = klausula hasiera/amaia, "

        if s1 == "MAI":
            if s2 == "KONP":
                return "Gradu maila = konparatiboa, "
            if s2 == "SUP":
                return "Gradu maila = superlatiboa, "
            if s2 == "GEHI":
                return "Gradu maila = gehiegizkoa, "
            if s2 == "IND":
                return "Gradu maila = indargarria, "

        if s1 == "MOD":
            if s2 == "ZIU":
                return "mModaltasuna = ziurtasunezkoa, "
            if s2 == "EGI":
                return "Modaltasuna = egiatasunezkoa, "

        if s1 == "MTKAT":
            if s2 == "LAB":
                return "Metakategoria = laburtzapena, "
            if s2 == "SIG":
                return "Metakategoria = sigla, "
            if s2 == "SNB":
                return "Metakategoria = sinboloa, "

        if s1 == "MUG":
            if s2 == "M":
                return "Mugatasuna = mugatua, "
            if s2 == "MG":
                return "Mugatasuna = mugatugabea, "

        if s1 == "NEUR":
            if s2 == "+":
                return "Neurgarria = Bai, "
            if s2 == "-":
                return "Neurgarria = Ez, "    

        if s1 == "NMG":
            if s2 == "S":
                return "Numeroa-mugatasuna = singularra, "        
            if s2 == "P":
                return "Numeroa-mugatasuna = plurala, "
            if s2 == "MG":
                return "Numeroa-mugatasuna = mugagabea, "  

        if s1 == "OIN":
            return f"Oinarria = {s2}, "

        if s1 == "POS":
            if s2 == "NN":
                return "Posizioa = nonahi, "
            if s2 == "ATZE":
                return "Posizioa = atzetik, "
            if s2 == "AURRE":
                return "Posizioa = aurretik, "
        
        if s1 == "ZENB":
            if s2 == "+":
                return "Zenbakarria = Bai, "
            if s2 == "-":
                return "Zenbakarria = Ez, "

        if s1 == "Aldaera":
            return f"Aldaera = {s2}, "

        if s1 == "FSL":
            return f"FSL = {s2}, "
        
        if s1 == "ERROR-KODE":
            return f"ERROR-KODE = {s2}, "

        fa = open("errors/FaltaDirenLexemak", "a")
        fa.write(f"[{s1},{s2}]")
        fa.close()
        return ""

class analisia:
    """ Testu baten sarrera guztiak dituen objektua"""

    def __init__(self,sarrerak,f):
        """analisia -ren instantzia bat sortzen du

        Args:
            sarrerak (list): Sarrera guztiak dituen array bat
            f (str): fasearen fasea
        """
        self.analisia = sarrerak
        self.analiFasea = f

    def getinformation(self):
        """Analisi baten sarrera guztien informazioa itzultzen du

        Return:
        list[str]. sarrera guztiak parseatuak itzultzen ditu array batean

        """
        strSar = []
        x = 0
        for s in self.analisia:
            x = x + 1
            strSar.append(f"{x}") #Esto despues se quita
            for l in s.sarrera:  
                str = ""
                for key in l.ezaugarriak:
                    if l.ezaugarriak[key] != None:
                        str = str + self.keyToString(key,l.ezaugarriak[key])
                strSar.append(str)
        return strSar

    def getinformationIndex(self, index):

        """
        Sarrera baten analisi baten informazioa itzultzen du

        Args:
        index(int): Itzuliko den analisiaren zenbakia

        Returns:
        str : analisiaren informazio guztia
        """

        str = ""
        for l in self.analisia[index].sarrera:  
            for key in l.ezaugarriak:
                if l.ezaugarriak[key] != None:
                    str = str + keyToString(key,l.ezaugarriak[key])
            str = str +"\n"
        return str

    def getinformationKeys(self,k):
        """Analisi baten sarrera guztien informazioa itzultzen du

        Args:
        k (array[str]): itzuli nahi diren ezaugarriak

        Returns:
        list[str]. sarrera guztiak parseatuak itzultzen ditu array batean

        """
        strSar = []
        x = 0
        for s in self.analisia:
            x = x + 1
            strSar.append(f"{x}") #Esto despues se quita
            for l in s.sarrera:  
                str = ""
                for key in l.ezaugarriak:
                    if l.ezaugarriak[key] != None and key in k:
                        str = str + self.keyToString(key,l.ezaugarriak[key])
                strSar.append(str)
        return strSar

    def getinformationIndexKeys(self, index, k):

        """
        Sarrera baten analisi baten informazioa itzultzen du

        Args:
        index(int): Itzuliko den analisiaren zenbakia
        k (list[str]): Itzuli nahi diren ezaugaien gakoak

        Returns:
        str : analisiaren eskatutako informazioa
        """

        str = ""
        for l in self.analisia[index].sarrera:  
            for key in l.ezaugarriak:
                if l.ezaugarriak[key] != None and key in k:
                    str = str + keyToString(key,l.ezaugarriak[key])
            str = str +"\n"
        return str

        

    def keyToString(self,s1,s2):
        """ Analik itzultzen duen kodeak itzultzen ditu

        Args:
            s1(str): pythoneko hiztegiko KEY
            s2(str): pythoneko hiztegiko ITEM

        Returns:
            str. KEY eta ITEM horien string-a

            **BESTENAZ** ez badu aurkiten errors karpetan fitxategi bat sorten du aurkitu ez duen [key, item] dupla batekin

        """
        if s1 == "Sarrera":
            return "Sarrera = {}, ".format(s2)

        if s1 == "KAT":
            if s2 == "IZE":
                return "Kategoria = izena, "
            if s2 == "ADJ":
                return "Kategoria = adjektiboa, "    
            if s2 == "ADI":
                return "Kategoria = aditza, "
            if s2 == "ADB":
                return "Kategoria = adberbioa, "
            if s2 == "DET":
                return "Kategoria = determinatzailea, "
            if s2 == "IOR":
                return "Kategoria = izenordaina, "
            if s2 == "LOT":
                return "Kategoria = lotura, "
            if s2 == "PRT":
                return "Kategoria = partikula, "
            if s2 == "ITJ":
                return "Kategoria = interjekzioa, "
            if s2 == "BST":
                return "Kategoria = bestelakoa, "
            if s2 == "ADL":
                return "Kategoria = aditz laguntzaile, "
            if s2 == "ADT":
                return "Kategoria = aditz sintetikoa, "
            if s2 == "HAOS":
                return "Kategoria = haul osagaia, "
            if s2 == "LAB":
                return "Kategoria = laburdura, "
            if s2 == "SIG":
                return "Kategoria = sigla, "
            if s2 == "SNB":
                return "Kategoria = sinboloa, "
            if s2 == "MAR":
                return "Kategoria = elkarketa marra,"
            if s2 == "AMM":
                return "Kategoria = aditz-mota morfema, "
            if s2 == "ASP":
                return "Kategoria = aspektu-morfena, "
            if s2 == "ATZ":
                return "Kategoria = atzizki lexikala, "
            if s2 == "AUR":
                return "Kategoria = aurrizki lexikala, "
            if s2 == "DEK":
                return "Kategoria = deklinabide-morfena, "
            if s2 == "ELI":
                return "Kategoria = elipsia, "
            if s2 == "ERL":
                return "Kategoria = erlazio-morfena, "
            if s2 == "GRA":
                return "Kategoria = graduatzailea, "
            if s2 == "HAOS":
                return "Kategoria = hitz-anitzeko osagaia, "
      


        if s1 == "AZP" or s1 == "ERAAZP":
                
            if s1 == "AZP":
                aux = ""
            else:
                aux = "Eratorriaren "

            if s2 == "ARR":
                return aux + "azpikategoria = arrunta, "
            if s2 == "IZB":
                return aux + "azpikategoria = pertsona-izen berezia, " 
            if s2 == "LIB": 
                return aux + "azpikategoria = leku-izen berezia, "
            if s2 == "IZO": 
                return aux + "azpikategoria = izenondoa, "
            if s2 == "IZL": 
                return aux + "azpikategoria = izenlaguna, "
            if s2 == "SIN": 
                return aux + "azpikategoria = sinplea, "
            if s2 == "ADK": 
                return aux + "azpikategoria = konposatua, "
            if s2 == "ADP":
                return aux + "azpikategoria = perifrastikoa, "
            if s2 == "FAK":
                return aux + "azpikategoria = faktitiboa, "
            if s2 == "GAL": 
                return aux + "azpikategoria = galdetzailea, "
            if s2 == "IND": 
                return aux + "azpikategoria = indartua, "
            if s2 == "DZH": 
                return aux + "azpikategoria = zehaztua, "
            if s2 == "DZG":
                return aux + "azpikategoria = zehaztugabea, "
            if s2 == "ORO":
                return aux + "azpikategoria = orokorra, "
            if s2 == "MGB":
                return aux + "azpikategoria = mugagabea, "
            if s2 == "ELK":
                return aux + "azpikategoria = elkarkaria, "
            if s2 == "LOK":
                return aux + "azpikategoria = lokailua, "
            if s2 == "JNT":
                return aux + "azpikategoria = juntagailua, "
            if s2 == "BIH":
                return aux + "azpikategoria = bihurkaria, "
            if s2 == "BAN":
                return aux + "azpikategoria = banatzailea, "
            if s2 == "ELK":
                return aux + "azpikagoria = elkarkaria, "
            if s2 == "ERKARR":
                return aux + "azpikagoria = erakusle arrunta, "
            if s2 == "ERKIND":
                return aux + "azpikagoria = erakusle indartua, "
            if s2 == "IZGGAL":
                return aux + "azpikagoria = zehaztugabea galdetzailea, "
            if s2 == "IZGMGB":
                return aux + "azpikagoria = zehatzugabe mugagabea, "
            if s2 == "MEN":
                return aux + "azpikagoria = menderagailua, "
            if s2 == "NOLARR":
                return aux + "azpikagoria = nolakotzaile arrunta, "
            if s2 == "NOLGAl":
                return aux + "azpikagoria = nolakotzaile galdetzailea, "
            if s2 == "ORD":
                return aux + "azpikagoria = zenbatzaile zehaztu ordinala, "
            if s2 == "PERARR":
                return aux + "azpikagoria = pertsona-izenordain arrunta, "
            if s2 == "PERIND":
                return aux + "azpikagoria = pertsona-izenordain indartua, "
            if s2 == "ZKI":
                return aux +     "azpikagoria = izen zenbakia, "
       
        if s1 == "BIZ":

            if s2 == "-":
                return "Bizigabea = Bai, "
            if s2 == "+":
                return "Biziduna = Bai, "
        
        if s1 == "ADOIN":
            return f"aditz oina = {s2}, "

        if s1 == "LAGM":
            return f"laguntzaile mota = {s2}, "
        
        if s1 == "ERR":
            return f"erroa = {s2}, "

        if s1 == "NOR":
            return f"nor = {s2}, "
        
        if s1 == "NORI":
            return f"nori = {s2}, "
        
        if s1 == "NORK":
            return f"nork = {s2}, "
        
        if s1 == "MDN":
            if s2 == "A1":
                return f"Modu-Denbora = Indikatibozko orainaldia, "
            if s2 == "A2":
                return f"Modu-Denbora = Indikatibozko geroaldia, "
            if s2 == "A3":
                return f"Modu-Denbora = subjuntibuzko orainaldia, "
            if s2 == "A4":
                return f"Modu-Denbora = Indikatibozko baldintza, "
            if s2 == "B1":
                return f"Modu-Denbora = Indikatibozko lehenaldia, "
            if s2 == "B2":
                return f"Modu-Denbora = Indikatibozko baldintza (ondorioa, orain-gero), "
            if s2 == "B3":
                return f"Modu-Denbora = Indikatibozko baldintza (ondorioa, lehen), "
            if s2 == "B4":
                return f"Modu-Denbora = Indikatibozko baldintza (aurrekoa), "
            if s2 == "B5":
                return f"Modu-Denbora = Subjuntibuzko baldintza eta alegiazkoa, "
            if s2 == "B6":
                return f"Modu-Denbora = subjuntibozko baldintza (lehenaldia), "
            if s2 == "B7":
                return f"Modu-Denbora = Ahalezko lehenaldia, "
            if s2 == "B8":
                return f"Modu-Denbora = Ahalezko lehenaldi urruna, "
            if s2 == "B5A":
                return f"Modu-Denbora = Subjuntibozko ahalegiazkoa, "
            if s2 == "B5B":
                return f"Modu-Denbora = Subjuntubozko lehenaldia, "
            
        if s1 == "ASP":
                
            if s2 == "EZBU":
                return f"Aspektua = ez-burutua, "
            if s2 == "GERO":
                return f"Aspektua = etorkizuna, "
            if s2 == "BURU":
                return f"Aspektua = partizipioa, "
            if s2 == "PNT":
                return f"Aspektua = Puntukaria, "
        
        if s1 == "OSA1":
            return f"lehenbiziko osagarria = {s2}, "
        
        if s1 == "OSA2":
            return f"Bigarren osagarria = {s2}, "
        
        if s1 == "PLU":
            if s2 == "+":
                return "plurala = Bai, "
            if s2 == "-":
                return "plurala = Ez, "

        if s1 == "IZAUR":
            if s2 == "+":
                return "izenaren aurretik = Bai, "
            if s2 == "-":
                return "izenaren aurretik = Ez, "

        if s1 == "PER":
            return f"Pertsona = {s2}, "

        if s1 == "NUM":
            if s2 == "S":
                return "Numeroa = singularra, "
            if s2 == "P":
                return "Numeroa = plurala, "
            if s2 == "PH":
                return "Numeroa = Plural hurbila, "
        
        if s1 == "RARE":
            if s2 == "ANB":
                return "Arraroa = kategoria honetan, "
            if s2 == "ABT":
                return "Arraroa = absolutoa (hitz laburrak), "
            if s2 == "LEX":
                return "Arraroa = lexikala, "

        if s1 == "ADBM":
            if s2 == "DENB":
                return "Adberbio mota = denborazkoa, "
            if s2 == "MOD":
                return "Adberbio mota = moduzkoa, "
            if s2 == "GRAD":
                return "Adberbio mota = graduatzailea, "
            if s2 == "LEK":
                return "Adberbio mota = lekuzkoa, "
            
        if s1 == "ADM":
            if s2 == "ADOIN":
                return "Aditz mota = aditz-oina, "
            if s2 == "PART":
                return "Aditz mota = partizipioa, "
            if s2 == "ADOIN":
                return "Aditz mota = aditz-izena, "
            
        if s1 == "ADZ":
            return f"adierazia = {s2}, "

        if s1 == "ATZL":
            return f"atzizki lista = {s2}, "

        if s1 == "AUR":
            return f"aurrizki = {s2}, "
        
        if s1 == "AZPERD":
            return f"Azpikategorizazio-eredua = {s2}, "
        
        if s1 == "ELK":
            if s2 == "I+I":
                return "elkarketa mota = izena + izena, "
            if s2 == "I+ADJ":
                return "elkarketa mota = izena + adjektiboa, "
            if s2 == "ADI+ADI":
                return "elkarketa mota = aditza + aditza, "
        
        if s1 == "ERAKAT":
            return f"Eratorriaren kategoria = {s2}, "
        
        if s1 == "ERL":
            if s2 == "BALD":
                return f"Erlazioa = bakdintza, "
            if s2 == "DENB":
                return f"Erlazioa = denborazkoa, "
            if s2 == "ESPL":
                return f"Erlazioa = esplikatiboa, "
            if s2 == "HELB":
                return f"Erlazioa = helburuzkoa, "
            if s2 == "KAUS":
                return f"Erlazioa = kausala, "
            if s2 == "KONT":
                return f"Erlazioa = kontzesiboa, "
            if s2 == "MOD":
                return f"Erlazioa = moduzkoa, "
            if s2 == "ERLT":
                return f"Erlazioa = erlatibozkoa, "
            if s2 == "ZHG":
                return f"Erlazioa = zehargaldera, "
            if s2 == "MOS":
                return f"Erlazioa = menderagailu-osagaia, "
            if s2 == "MOD/DENB":
                return f"Erlazioa = modu-Denborazkoa, "
            if s2 == "EMEN":
                return f"Erlazioa = emendiozkoa, "
            if s2 == "ONDO":
                return f"Erlazioa = ondoriozkoa, "
            if s2 == "AURK":
                return f"Erlazioa = aurkarizkoa, "
            if s2 == "KONPL":
                return f"Erlazioa = konpletiboa, "
            if s2 == "HAUT":
                return f"Erlazioa = hautakaria, "
            if s2 == "MOTIB":
                return f"Erlazioa = motibatiboa, "
        
        if s1 == "Estandarrak":
            return f"estandarrak = {s2}, "
        
        if s1 == "HIT":
            return f"Hitanoa = {s2}, "
        
        if s1 == "HOBETSI1":
            return f"Hobetstako sarrera = {s2}, "
        
        if s1 == "Hobetsiak":
            return f"Hobetsiak = {s2}, "
        
        if s1 == "HURB":
            return f"Hurbiltasun maila = {s2},"

        if s1 == "KAS":
            if s2 == "ABL":
                return "Kasua = ablatiboa, "
            if s2 == "ABU":
                return "Kasua = adlatibo bukatuzkoa, "
            if s2 == "ABZ":
                return "Kasua = adlatibo bide zuzenezkoa, "
            if s2 == "ALA":
                return "Kasua = adlatiboa, "
            if s2 == "SOZ":
                return "Kasua = soziatiboa, "
            if s2 == "DAT":
                return "Kasua = datiboa, "
            if s2 == "DES":
                return "Kasua = destinatiboa, "
            if s2 == "ERG":
                return "Kasua = ergatiboa, "
            if s2 == "GEL":
                return "Kasua = genitiboa (leku denborazkoa), "
            if s2 == "GEN":
                return "Kasua = genitiboa, "
            if s2 == "INE":
                return "Kasua = inesiboa, "
            if s2 == "INS":
                return "Kasua = instrumetala, "
            if s2 == "MOT":
                return "Kasua = motibatiboa, "
            if s2 == "ABS":
                return "Kasua = absolutiboa, "
            if s2 == "PAR":
                return "Kasua = partitiboa, "
            if s2 == "PRO":
                return "Kasua = prolatiboa, "
            if s2 == "BNK":
                return "Kasua = banakaria, "
            if s2 == "DESK":
                return "Kasua = deskribatzailea, "

        if s1 == "KLM":
            if s2 == "HAS":
                return "Klausula-muga = klausula hasiera, "
            if s2 == "AM":
                return "Klausula-muga = klausula amaia, "
            if s2 == "HA":
                return "Klausula-muga = klausula hasiera/amaia, "

        if s1 == "MAI":
            if s2 == "KONP":
                return "Gradu maila = konparatiboa, "
            if s2 == "SUP":
                return "Gradu maila = superlatiboa, "
            if s2 == "GEHI":
                return "Gradu maila = gehiegizkoa, "
            if s2 == "IND":
                return "Gradu maila = indargarria, "

        if s1 == "MOD":
            if s2 == "ZIU":
                return "Modaltasuna = ziurtasunezkoa, "
            if s2 == "EGI":
                return "Modaltasuna = egiatasunezkoa, "

        if s1 == "MTKAT":
            if s2 == "LAB":
                return "Metakategoria = laburtzapena, "
            if s2 == "SIG":
                return "Metakategoria = sigla, "
            if s2 == "SNB":
                return "Metakategoria = sinboloa, "

        if s1 == "MUG":
            if s2 == "M":
                return "Mugatasuna = mugatua, "
            if s2 == "MG":
                return "Mugatasuna = mugatugabea, "

        if s1 == "NEUR":
            if s2 == "+":
                return "Neurgarria = Bai, "
            if s2 == "-":
                return "Neurgarria = Ez, "    

        if s1 == "NMG":
            if s2 == "S":
                return "Numeroa-mugatasuna = singularra, "        
            if s2 == "P":
                return "Numeroa-mugatasuna = plurala, "
            if s2 == "MG":
                return "Numeroa-mugatasuna = mugagabea, "  

        if s1 == "OIN":
            return f"Oinarria = {s2}, "

        if s1 == "POS":
            if s2 == "NN":
                return "Posizioa = nonahi, "
            if s2 == "ATZE":
                return "Posizioa = atzetik, "
            if s2 == "AURRE":
                return "Posizioa = aurretik, "
        
        if s1 == "ZENB":
            if s2 == "+":
                return "Zenbakarria = Bai, "
            if s2 == "-":
                return "Zenbakarria = Ez, "

        if s1 == "Aldaera":
            return f"Aldaera = {s2}, "

        if s1 == "FSL":
            return f"FSL = {s2}, "
        
        if s1 == "ERROR-KODE":
            return f"ERROR-KODE = {s2}, "

        fa = open("errors/FaltaDirenLexemak", "a")
        fa.write(f"[{s1},{s2}]")
        fa.close()
        return ""

class Sarrera:
    """ Analisi batek dituen ezaugarri guztiak gordetzen dituen egitura"""

    def __init__(self):
        """
        Sarrera objetuktuaren insstantzia bat sortzen du
        """
        self.sarrera = []
    
    def lemaGehitu(self,l):
        """
        Ezaugarri bat gehitzen du memoria egiturara

        Args:
        l(Ezaugarriak): Ezaugarriak-ren instantzia bat

        """
        self.sarrera.append(l)

    def getKategoria(self):
        str = ""
        for e in self.sarrera:
            print(e.ezaugarriak["Sarrera"])
            if e.ezaugarriak["Sarrera"] != None:
                str =str + keyToString("Sarrera",e.ezaugarriak["Sarrera"]) + keyToString("KAT", e.ezaugarriak["KAT"]) + "\n"
            else:
                return None
        return str

    
    def getGuztia(self):

        str = ""
        for l in self.sarrera:  
            for key in l.ezaugarriak:
                if l.ezaugarriak[key] != None:
                    str = str + keyToString(key,l.ezaugarriak[key])
            str = str + "\n"
        return str

class Ezaugarriak:

    """Ezaugarriak gordetzeko memoria egitura"""

    def __init__(self, entrada): #entrada = [[SARRERA, etxeratu][KAT,IZE ]]
        """Ezugarriak -ren instantzia bat sortzen du

        Args:
            entrada(str): Honako forma edukiko du:
                #entrada = [[SARRERA, etxeratu][KAT,IZE ]]
                Analik bueltatzen duen modua
        
        """
        
        self.ezaugarriak = {"Sarrera": None,"KAT" : None, "AZP":None, "BIZ": None, "ERR":None, "NOR":None, "NORI":None, "NORK":None, "ASP":None, "PER":None, 
        "Num":None, "RARE": None, "ADOIN":None, "LAGM":None, "IZAUR": None, "BIZ": None, "OSA1":None, "OSA2":None, "PLU": None, "ADBM":None, "ADM": None, "ADZ":None,
        "ERAAZP": None, "ATZL": None, "AUR": None, "AZPERD": None, "ELK": None, "ERAKAT": None, "ERL": None, "Estandarrak": None, "FSL": None, "HIT": None, "HOBETSI1": None,
        "Hobetsiak": None, "HURB" : None, "KAS": None, "KLM": None, "MAI": None, "MDN": None, "MOD": None, "MTKAT": None, "MUG": None, "NEUR": None, "NMG": None, "OIN": None, "POS": None,
        "STD1": None, "STD2M": None, "ZENB": None, "Aldaera": None, "FSL": None, "ERROR-KODE": None}
        
        for s in entrada:
            if s[1] == "":
                self.ezaugarriak[s[0]] = '-'
            elif "STD" in s[0]:
                if self.ezaugarriak["Estandarrak"] == None:
                    self.ezaugarriak["Estandarrak"] = s[1]
                else:
                    self.ezaugarriak["Estandarrak"] = self.ezaugarriak["Estandarrak"] + "/" + s[1]
            elif "FSL" in s[0]:
                if  self.ezaugarriak["FSL"] == None:
                    self.ezaugarriak["FSL"] = s[1]
                else:
                    self.ezaugarriak["FSL"] = self.ezaugarriak["FSL"] + "/" + s[1] 
            else:
                self.ezaugarriak[s[0]] = s[1]
