import json
from datetime import datetime, time, date
from klients import Klients
from pakalpojums import Pakalpojums


class SpecialaisJSONKodetajs(json.JSONEncoder):
    def default(self, obj):
        return obj.strftime("%d.%m.%Y.") if isinstance(obj, date) else obj.strftime("%H:%M") if \
            isinstance(obj, time) else obj.__dict__


def eksportet(obj):
    objekta_klases_nosaukums = "klienta_{}".format(obj.klienta_id) if isinstance(obj, Klients) else \
        "pakalpojuma_{}".format(obj.pakalpojuma_id) if isinstance(obj, Pakalpojums) else "objekta"
    eksporta_datnes_nosaukums = objekta_klases_nosaukums + "_eksports_" \
                                + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".json"
    try:
        with open(eksporta_datnes_nosaukums, "w", encoding="utf-8") as eksporta_datne:
            json.dump(obj, eksporta_datne, ensure_ascii=False, cls=SpecialaisJSONKodetajs)
    except OSError:
        print("Neizdevās izveidot datni datu eksportam!")
    except Exception:
        print("Izvades kļūda!")


def importet():
    try:
        with open(importa_datnes_nosaukums, encoding="utf-8") as importa_datne:
            return json.load(importa_datne)
    except OSError:
        print("Neizdevās atvērt datni datu importam!")
    except json.decoder.JSONDecodeError:
        print("Datnes satura formāts neatbilst JSON formātam!")
    except Exception:
        print("Ievades kļūda!")
    return list()


if __name__ == "__main__":
    klienti = list()
    pakalpojumi = list()

    while True:
        print()
        importa_datnes_nosaukums = input("Lūdzu, ievadiet datnes nosaukumu datu ievadei: ")
        datnes_saturs = importet()
        if isinstance(datnes_saturs, list) and len(datnes_saturs) > 0:
            if "klienta_id" in datnes_saturs[0]:
                for item in datnes_saturs:
                    klienti.append(Klients(item["klienta_vards"], item["klienta_uzvards"],
                                           item["klienta_pers_kods"], item["klienta_talr_num"]))
                if len(klienti) != 0:
                    print()
                    if len(klienti) == 1:
                        print("Tika veiksmīgi nolasīti dati par vienu klientu:")
                    else:
                        print("Tika veiksmīgi nolasīti dati par " + str(len(klienti)) + " klientiem:")
                    for klients in klienti:
                        print(klients)
            elif "pakalpojuma_id" in datnes_saturs[0]:
                for item in datnes_saturs:
                    try:
                        pakalpojumi.append(Pakalpojums(item["pakalpojuma_kategorija"], item["pakalpojuma_nosaukums"],
                                                       item["pakalpojuma_atlaide"], item["pakalpojuma_cena"],
                                                       datetime.strptime(item["pakalpojuma_datums"],
                                                                         "%d.%m.%Y.").date(),
                                                       datetime.strptime(item["pakalpojuma_sakuma_laiks"],
                                                                         "%H:%M").time(),
                                                       datetime.strptime(item["pakalpojuma_beigu_laiks"],
                                                                         "%H:%M").time()))
                    except ValueError:
                        print("Nepareizs skaitļu formāts!")
                if len(pakalpojumi) != 0:
                    print()
                    if len(pakalpojumi) == 1:
                        print("Tika veiksmīgi nolasīti dati par vienu pakalpojumu:")
                    else:
                        print("Tika veiksmīgi nolasīti dati par " + str(len(pakalpojumi)) + " pakalpojumiem:")
                    for pakalpojums in pakalpojumi:
                        print(pakalpojums)
                        print("Pakalpojuma kopsumma: " + str(pakalpojums.pakalpojuma_kopsumma()) + " EUR")
                        ilgums_minutes = pakalpojums.pakalpojuma_ilgums() / 60
                        if ilgums_minutes % 10 == 1:
                            print("Pakalpojuma ilgums: {:.0f} minūte\n".format(ilgums_minutes))
                        else:
                            print("Pakalpojuma ilgums: {:.0f} minūtes\n".format(ilgums_minutes))
            else:
                print("Nezināma objekta struktūra!")
        else:
            print("Nezināma datnes satura struktūra!")
        while True:
            ievade = input("Vai vēlaties importēt datus no vēl vienas datnes? y/n: ")
            if ievade[0].lower() not in ["y", "n"]:
                print("Jūs ievadījāt nepieņemamo vērtību! Lūdzu, mēģiniet vēlreiz!")
                continue
            else:
                break
        if ievade[0].lower() == "n":
            break

    # klients_1 = Klients("Mihails", "Korčevskis", "171299-00000", "20000000")
    # klients_2 = Klients("Andrejs", "Vasiļkovs", "101000-00000", "20000000")
    # klients_3 = Klients()
    # klienti = [klients_1, klients_2, klients_3]

    # pakalpojums_1 = Pakalpojums("Solārijs", "Solārijs", 0.2, 50, datetime.strptime("08.04.2022.", "%d.%m.%Y.").date(),
    #                             datetime.strptime("12:30", "%H:%M").time(), datetime.strptime("12:45", "%H:%M").time())
    # pakalpojums_2 = Pakalpojums()
    # pakalpojumi = [pakalpojums_1, pakalpojums_2]
