import itertools

class Klients:
    klienta_vards = "Jānis"
    klienta_uzvards = "Bērziņš"
    klienta_pers_kods = "010100-00000"
    klienta_talr_num = "20000000"

    klienta_id_iter = itertools.count()

    def __init__(self):
        self.klienta_id = next(self.klienta_id_iter) + 1

    def __init__(self, _vards=klienta_vards, _uzvards=klienta_uzvards, _pers_kods=klienta_pers_kods, _talr_num=klienta_talr_num):
        self.klienta_id = next(self.klienta_id_iter) + 1
        self.klienta_vards = _vards
        self.klienta_uzvards = _uzvards
        self.klienta_pers_kods = _pers_kods
        self.klienta_talr_num = _talr_num

    def klienta_info(self):
        return [self.klienta_vards, self.klienta_uzvards, self.klienta_pers_kods, self.klienta_talr_num]

    def __str__(self):
        info = self.klienta_info()
        return "Klienta vārds: " + info[0] + "\n" \
               + "Klienta uzvārds: " + info[1] + "\n" \
               + "Klienta personas kods: " + info[2] + "\n" \
               + "Klienta tālruņa numurs: " + info[3] + "\n"
