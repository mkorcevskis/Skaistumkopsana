from datetime import datetime, timedelta, date
import itertools


class Pakalpojums:
    pakalpojuma_kategorija = "Frizētava"
    pakalpojuma_nosaukums = "Matu griešana"
    pakalpojuma_atlaide = 0.00
    pakalpojuma_cena = 20.00
    pakalpojuma_datums = datetime.now().date()
    pakalpojuma_sakuma_laiks = datetime.now().time()
    pakalpojuma_beigu_laiks = datetime.time(datetime.now() + timedelta(minutes=40))
    vai_laiks_ir_pieejams = True

    pakalpojuma_id_iter = itertools.count()

    def __init__(self):
        self.pakalpojuma_id = next(self.pakalpojuma_id_iter) + 1
        self.vai_laiks_ir_pieejams = True

    def __init__(self, _kategorija=pakalpojuma_kategorija, _nosaukums=pakalpojuma_nosaukums,
                 _atlaide=pakalpojuma_atlaide, _cena=pakalpojuma_cena, _datums=pakalpojuma_datums,
                 _sakuma_laiks=pakalpojuma_sakuma_laiks, _beigu_laiks=pakalpojuma_beigu_laiks):
        self.pakalpojuma_id = next(self.pakalpojuma_id_iter) + 1
        self.pakalpojuma_kategorija = _kategorija
        self.pakalpojuma_nosaukums = _nosaukums
        self.pakalpojuma_atlaide = _atlaide
        self.pakalpojuma_cena = _cena
        self.pakalpojuma_datums = _datums
        self.pakalpojuma_sakuma_laiks = _sakuma_laiks
        self.pakalpojuma_beigu_laiks = _beigu_laiks
        self.vai_laiks_ir_pieejams = True

    def pakalpojuma_ilgums(self):
        return (datetime.combine(date.min, self.pakalpojuma_beigu_laiks) -
                datetime.combine(date.min, self.pakalpojuma_sakuma_laiks)).total_seconds()

    def pakalpojuma_kopsumma(self):
        return self.pakalpojuma_cena * (1.00 - self.pakalpojuma_atlaide)

    def pakalpojuma_info(self):
        return [self.pakalpojuma_kategorija, self.pakalpojuma_nosaukums, self.pakalpojuma_atlaide,
                self.pakalpojuma_cena, self.pakalpojuma_datums, self.pakalpojuma_sakuma_laiks,
                self.pakalpojuma_beigu_laiks, self.vai_laiks_ir_pieejams]

    def __str__(self):
        info = self.pakalpojuma_info()
        return "Pakalpojuma kategorija: " + info[0] + "\n" \
               + "Pakalpojuma nosaukums: " + info[1] + "\n" \
               + "Pakalpojuma atlaide: " + str(info[2] * 100) + " %\n" \
               + "Pakalpojuma cena: " + str(info[3]) + " EUR\n" \
               + "Pakalpojuma datums: " + info[4].strftime("%d.%m.%Y.") + "\n" \
               + "Pakalpojuma sākuma laiks: " + info[5].strftime("%H:%M") + "\n" \
               + "Pakalpojuma beigu laiks: " + info[6].strftime("%H:%M") + "\n" \
               + "Vai laiks ir pieejams: " + ("Jā" if info[7] else "Nē") + "\n"
