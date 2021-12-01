class Jugadas:

    def __init__(self):

        self.jugadasDeshacer = []
        self.jugadasRehacer = []

    def AgregarDeshacer(self,i,j,num):

        self.jugadasDeshacer.append([i,j,num])

    def AgregarRehacer(self,i,j,num):

        self.jugadasRehacer.append([i,j,num])

    def Deshacer(self):

        if len(self.jugadasDeshacer) > 0:

            i,j = self.jugadasDeshacer[-1][0],self.jugadasDeshacer[-1][1]
            self.AgregarRehacer(i,j,self.jugadasDeshacer[-1][2])
            self.jugadasDeshacer.pop()

            return [i,j]

        return None

    def Rehacer(self):

        if len(self.jugadasRehacer) > 0:

            i,j,num = self.jugadasRehacer[-1][0],self.jugadasRehacer[-1][1],self.jugadasRehacer[-1][2]
            self.AgregarDeshacer(i,j,self.jugadasRehacer[-1][2])
            self.jugadasRehacer.pop()

            return [i,j,num]

        return None
