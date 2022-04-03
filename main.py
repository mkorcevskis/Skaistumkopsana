from datetime import datetime
from klients import Klients
from pakalpojums import Pakalpojums

def saglabat_ka_datni(obj):
    objekta_klases_nosaukums = "klienta" if isinstance(obj, Klients) else "pakalpojuma" if isinstance(obj, Pakalpojums) else "objekta"
    eksporta_datnes_nosaukums = objekta_klases_nosaukums + "_eksports_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".json"
    # print(eksporta_datnes_nosaukums)
    try:
        with open(eksporta_datnes_nosaukums, "w", encoding="utf-8") as eksporta_datne:
            eksporta_datne.write(str(obj.__dict__))
            eksporta_datne.close()
    except OSError:
        print("Neizdevās atvērt failu datu izvadei!")


if __name__ == "__main__":
    klients_1 = Klients("Mihails", "Korčevskis", "171299-00000", "20000000")
    klients_2 = Klients("Andrejs", "Vasiļkovs", "101000-00000", "20000000")
    klients_3 = Klients("Marks", "Isajevs", "151000-00000", "20000000")

    pakalpojums_1 = Pakalpojums()

    print(klients_1)
    saglabat_ka_datni(klients_1)
