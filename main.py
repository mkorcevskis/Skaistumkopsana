from datetime import datetime
from klients import Klients
from pakalpojums import Pakalpojums

def eksportet(obj):
    objekta_klases_nosaukums = "klienta_{}".format(obj.klienta_id) if isinstance(obj, Klients) else \
        "pakalpojuma_{}".format(obj.pakalpojuma_id) if isinstance(obj, Pakalpojums) else "objekta"
    eksporta_datnes_nosaukums = objekta_klases_nosaukums + "_eksports_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".json"
    try:
        with open(eksporta_datnes_nosaukums, "w", encoding="utf-8") as eksporta_datne:
            eksporta_datne.write(str(obj.__dict__))
            eksporta_datne.close()
    except OSError:
        print("Neizdevās izveidot datni datu eksportam!")


if __name__ == "__main__":
    klients_1 = Klients("Mihails", "Korčevskis", "171299-00000", "20000000")
    klients_2 = Klients("Andrejs", "Vasiļkovs", "101000-00000", "20000000")
    klients_3 = Klients()
    klienti = [klients_1, klients_2, klients_3]
    print("Klienti:")
    for klients in klienti:
        print(klients)
        eksportet(klients)

    pakalpojums_1 = Pakalpojums("Solārijs", "Solārijs", 0.2, 50, datetime.strptime("08.04.2022.", "%d.%m.%Y.").date(),
                                datetime.strptime("12:30", "%H:%M").time(), datetime.strptime("12:45", "%H:%M").time())
    pakalpojums_2 = Pakalpojums()
    pakalpojumi = [pakalpojums_1, pakalpojums_2]
    print("Pakalpojumi:")
    for pakalpojums in pakalpojumi:
        print(pakalpojums)
        print("Pakalpojuma kopsumma: " + str(pakalpojums.pakalpojuma_kopsumma()) + " EUR")
        ilgums_minutes = pakalpojums.pakalpojuma_ilgums() / 60
        if ilgums_minutes % 10 == 1:
            print("Pakalpojuma ilgums: {:.0f} minūte\n".format(ilgums_minutes))
        else:
            print("Pakalpojuma ilgums: {:.0f} minūtes\n".format(ilgums_minutes))
        eksportet(pakalpojums)
