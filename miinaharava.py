#Tehneet: Jenna Onnela, Elina Lassi ja Janne Onnela

import haravasto
import random
import time
import pyglet
import sys

tila = {
    "kentta": None,
    "pelikentta": None,
    "leveys": 0,
    "korkeus": 0,
    "miinat": 0,
    "siirrot": 0,
    "aloitus_aika": time.time(),
    "pelin_paattyminen": False

}


def piirra_kentta():
	haravasto.tyhjaa_ikkuna()
	haravasto.piirra_tausta()
	haravasto.aloita_ruutujen_piirto()
	for x, lista in enumerate(tila["pelikentta"]):
		for y, ruutu in enumerate(lista):
			haravasto.lisaa_piirrettava_ruutu(ruutu, x * 40, y * 40)           
	haravasto.piirra_ruudut()
    
def kasittele_hiiri(x_sijainti,y_sijainti,painike,muokkausnappaimet):
    """koko pelin keskus"""
    if tila["pelin_paattyminen"] == True:
        return
    kentta = tila["kentta"]
    pelikentta = tila["pelikentta"]
    aloitus_aika = time.time()
    if painike == 2:
        painike = "keski"
    elif painike == 4:
        painike = "oikea"
        for x, lista in enumerate(tila["pelikentta"]):
            for y, ruutu in enumerate(lista):
                if pelikentta[x][y] == " ":
                    if x_sijainti - 40 <= x * 40 and x_sijainti - 40 >= x * 40 - 40 and y_sijainti - 40 <= y * 40 and y_sijainti - 40 >= y * 40 - 40 :
                        pelikentta[x][y] = "f"
                        tila["siirrot"] = tila["siirrot"] + 1
                elif pelikentta[x][y] == "f":
                    if x_sijainti - 40 <= x * 40 and x_sijainti - 40 >= x * 40 - 40 and y_sijainti - 40 <= y * 40 and y_sijainti - 40 >= y * 40 - 40 :
                        pelikentta[x][y] = " "
                        tila["siirrot"] = tila["siirrot"] + 1
                        
    elif painike == 1:
        painike = "vasen"
        for x, lista in enumerate(tila["pelikentta"]):
            for y, ruutu in enumerate(lista):
                if x_sijainti - 40 <= x * 40 and x_sijainti - 40 >= x * 40 - 40 and y_sijainti - 40 <= y * 40 and y_sijainti - 40 >= y * 40 - 40 :
                    if pelikentta[x][y] == "f":
                        kasittele_hiiri(x_sijainti,y_sijainti,painike,muokkausnappaimet)
                    elif kentta[x][y] == "x" and pelikentta[x][y] == " ":
                        pelikentta[x][y] = kentta[x][y]
                        tila["siirrot"] = tila["siirrot"] + 1
                        tappio()
                    elif kentta[x][y] == "0":
                        tila["siirrot"] = tila["siirrot"] + 1
                        tulvataytto(x, y, kentta, pelikentta)
                    else:
                        pelikentta[x][y] = kentta[x][y]
                        tila["siirrot"] = tila["siirrot"] + 1
    """Voittaminen"""
    voitto = True
    liput = 0
    for x, lista in enumerate(tila["pelikentta"]):
        for y, ruutu in enumerate(lista):
            if pelikentta[x][y] == " ":
                voitto = False
            elif pelikentta[x][y] == "f":
                liput = liput + 1
    if voitto and liput == tila["miinat"]:
        voittaminen()            
    
    return painike

def pelin_aloitus():
    """Aloitetaan peli"""
    print("Hei ja tervetuloa miinojen ihmeelliseen maailmaan!")
    print("Mitä haluat tehdä?")
    print("Aloita uusi peli, paina A")
    print("Katso tilastoja, paina T")
    print("Lopeta peli, paina L")
    
    syote = ""
    while True:
        syote = input("Syötä kirjain: ").upper()
        if syote == "A":
            tila["pelin_paattyminen"] = False
            tila["siirrot"] = 0
            maarita_kentta()
            kentta = []
            for rivi in range(tila["leveys"]):
                kentta.append([])
                for sarake in range(tila["korkeus"]):
                    kentta[-1].append(" ")
            tila["kentta"] = kentta
            pelikentta = []
            for rivi in range(tila["leveys"]):
                pelikentta.append([])
                for sarake in range(tila["korkeus"]):
                    pelikentta[-1].append(" ")
            tila["pelikentta"] = pelikentta
            jaljella = []
            for x in range(tila["leveys"]):
                for y in range(tila["korkeus"]):
                    jaljella.append((x-1, y-1))
            maarita_miinat()
            aseta_miinat(kentta, jaljella, tila["miinat"])
            aseta_numerot(kentta)
            main()
        elif syote == "T":
            try:
                avaa_tulokset()
            except FileNotFoundError:
                print("Eihän niitä pelitietoja voi olla, kun et ole vielä kertaakaan pelannut!")
        elif syote == "L":
            print("Joko sinä lähdet? Nähdään myöhemmin!")
            break
        
       
def maarita_kentta():
    """Kysyy pelaajalta kentän korkeuden ja leveyden"""
    while True:
        try:
            leveys = int(input("Anna kentän leveys: "))
            korkeus = int(input("Anna kentän korkeus: "))
            if leveys <= 1 or korkeus <= 1:
                print("Pitäähän sillä kentällä olla edes vähän kokoa... Kokeile isompia lukuja!")
                continue
            elif leveys > 30 or korkeus > 20:
                print("Oletko aivan varma? Jos kumminkin hiukan pienemmällä kentällä pelaisit.")
                continue
            tila["leveys"] = leveys
            tila["korkeus"] = korkeus
            break
        except ValueError:
            print("Kentän tulee muodostua kokonaisista ruuduista. Käytä siis kokonaislukuja") 

def maarita_miinat():
    """kysyy pelaajalta miinojen lkm"""
    while True:
        try:
            miinat = int(input("Anna miinojen lukumäärä: "))
            if miinat > tila["leveys"] * tila["korkeus"]:
                print("Eihän miinoja voi olla enemmän kuin ruutuja!")
                continue
            elif miinat < 1:
                print("Ilonpilaaja! Kyllä miinoja kuuluu miinaharavassa olla...")
                continue
            tila["miinat"] = miinat
            break
        except ValueError:
            print("Anna miinojen lukumäärä kokonaislukuna!")
            

def tulvataytto(x_koord, y_koord, kentta, pelikentta):
    """ skannaa siis seuraavat ruudut jos ruutu on tyhjä ja tuo näkyviin kaikki tyhjät ruudut jotka koskettavat toisiaan sekä reunimmaisimmat numeroruudut"""
    koord = (x_koord, y_koord)
    lista = [koord]
    while lista:
        x_koord, y_koord = lista.pop()
        pelikentta[x_koord][y_koord] = kentta [x_koord][y_koord]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if koordinaatti_tarkistus(x_koord + i, y_koord +j,tila["leveys"], tila["korkeus"]):
                    if pelikentta [x_koord + i][y_koord + j] == " " and kentta [x_koord][y_koord] == "0":
                        koord = (x_koord + i, y_koord + j)
                        lista.append(koord)
    return True
    
              

def miinoitus(kentta, tyhjat):
    """Mielivaltaisesti valitsee miinojen paikat kentältä"""
    mielivaltainen = random.choice(tyhjat)
    x = int(mielivaltainen[0])
    y = int(mielivaltainen[1])
    kentta[x][y] = "x"
    tyhjat.remove(mielivaltainen)
    return mielivaltainen

def aseta_miinat(kentta, tyhjat, miinat):
    """asettaa miinat paikoilleen"""
    for i in range(miinat):
        miinoitus(kentta, tyhjat)

def koordinaatti_tarkistus(x, y, leveys, korkeus):
    if x < 0 or x > leveys - 1 or y < 0 or y > korkeus - 1:
        return False
    else:
        return True

def aseta_numerot(kentta):
    """"Asettaa kentälle numerot"""
    for x, lista in enumerate(tila["kentta"]):
        for y, ruutu in enumerate(lista):
            lukumaara = 0
            for rivi in range(x - 1, x + 2):
                for sarake in range(y - 1, y + 2): 
                    if koordinaatti_tarkistus(rivi, sarake, tila["leveys"], tila["korkeus"]):
                        if kentta[rivi][sarake] == "x":
                            lukumaara += 1
            if kentta[x][y] != "x":
                kentta[x][y] = str(lukumaara)
			        
    
def tappio():
    tila["pelin_paattyminen"] = True
    pelin_kesto = ((time.time() - tila["aloitus_aika"]) / 60)
    paivays = time.strftime("%d %b %Y %H:%M:%S")
    print("Onneksi olkoon! Löysit miinan... Hävisit pelin :/")
    print("Teit {} siirtoa ja peli kesti {:.2f} minuuttia".format(tila["siirrot"], pelin_kesto))
    print("Päiväys: {}".format(paivays))
    print("Kentän koko: {} x {}".format(tila["leveys"], tila["korkeus"]))
    print("Miinojen lukumäärä: {}".format(tila["miinat"]))
    tulokset = "\nHävitty peli:\n"
    tulokset += "Päiväys: {}\nPeliaika: {:.2f} minuuttia\nMiinojen lukumäärä: {}\nKentän koko: {} x {} ruutua\nSiirrot: {}\n".format(paivays, pelin_kesto, tila["miinat"], tila["leveys"], tila["korkeus"], tila["siirrot"])
    vie_tiedostoon(tulokset)
    
def voittaminen():
    tila["pelin_paattyminen"] = True   
    pelin_kesto = ((time.time() - tila["aloitus_aika"]) / 60)
    paivays = time.strftime("%d %b %Y %H:%M:%S")
    print("Hurraa! Onnistuit välttämään kaikki miinat! Voitit pelin! :3")
    print("Teit {} siirtoa ja peli kesti {:.2f} minuuttia".format(tila["siirrot"], pelin_kesto))
    print("Päiväys: {}".format(paivays))
    print("Kentän koko: {} x {}".format(tila["leveys"], tila["korkeus"]))
    print("Miinojen lukumäärä: {}".format(tila["miinat"]))
    tulokset = "\nVoitettu peli:\n"
    tulokset += "Päiväys: {}\nPeliaika: {:.2f} minuuttia\nMiinojen lukumäärä: {}\nKentän koko: {} x {} ruutua\nSiirrot: {}\n".format(paivays, pelin_kesto, tila["miinat"], tila["leveys"], tila["korkeus"], tila["siirrot"])
    vie_tiedostoon(tulokset)
        
def vie_tiedostoon(tulokset):
    """Tallentaa pelin tiedot"""
    with open("pelien_tulokset.txt", "a") as tiedosto:
        tiedosto.write(tulokset)
        
def avaa_tulokset():
    """Näyttää tulokset"""
    with open("pelien_tulokset.txt", "r") as lukeminen:
        print(lukeminen.read())
    		
def main():
    """Kentän piirtämistä"""
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna()
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()
	
if __name__ == "__main__":
    try:
        pelin_aloitus()

    except ():
        print("Kiva kun kävit!")
   
        
        
