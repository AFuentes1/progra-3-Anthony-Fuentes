class tiempo:

    def __init__(self):
        self.hora = 0
        self.minuto = 0
        self.segundo = 0

    def setHora(self, hora):
        self.hora = hora

    def setMinuto(self, minuto):
        self.minuto = minuto

    def setSegundo(self, segundo):
        self.segundo = segundo

    def contraReloj(self):

        while self.segundo != 0 and self.minuto != 0 and self.hora != 0:

            self.segundo -= 1

            if self.segundo == 0:
                self.segundo = 59
                self.minuto -= 1

            if self.minuto == 0:
                self.minuto = 59
                self.hora -= 1

            if self.hora == 0:
                self.hora = 23
                self.minuto = 59
                self.segundo = 59

            time.sleep(1)

            print("{}:{}:{}".format(self.hora, self.minuto, self.segundo))

    def reloj(self):

        while True:

            self.segundo += 1

            if self.segundo == 60:
                self.segundo = 0
                self.minuto += 1

            if self.minuto == 60:
                self.minuto = 0
                self.hora += 1

            if self.hora == 24:
                self.hora = 0
                self.minuto = 0
                self.segundo = 0

            time.sleep(1)
            

