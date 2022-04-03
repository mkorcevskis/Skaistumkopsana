from datetime import datetime
import itertools

class Pakalpojums:
    pakalpojuma_kategorija = "//"
    pakalpojuma_nosaukums = "//"
    pakalpojuma_atlaide = 0.0
    pakalpojuma_cena = 0.0
    vai_laiks_ir_pieejams = True
    pakalpojuma_datums = datetime.now()
    pakalpojuma_sakuma_laiks = datetime.time(datetime.now())
    pakalpojuma_beigu_laiks = datetime.time(datetime.now())

    pakalpojuma_id_iter = itertools.count()

    def __init__(self):
        self.pakalpojuma_id = next(self.pakalpojuma_id_iter) + 1
        self.pakalpojuma_kategorija = "//"
        self.pakalpojuma_nosaukums = "//"
        self.pakalpojuma_atlaide = 0.0
        self.pakalpojuma_cena = 0.0
        self.vai_laiks_ir_pieejams = False
        self.pakalpojuma_datums = datetime.now()
        self.pakalpojuma_sakuma_laiks = datetime.time(datetime.now())
        self.pakalpojuma_beigu_laiks = datetime.time(datetime.now())

