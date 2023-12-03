import random

class Postać:
    def __init__(self, imię, zdrowie, atak, obrona, złoto, broń=None, zwierzak=None):
        self.imię = imię
        self.zdrowie = zdrowie
        self.atak = atak
        self.obrona = obrona
        self.złoto = złoto
        self.broń = broń
        self.zwierzak = zwierzak

    def żyje(self):
        return self.zdrowie > 0

    def otrzymaj_obrażenia(self, obrażenia):
        self.zdrowie -= obrażenia

    def zaatakuj_przeciwnika(self, przeciwnik):
        if self.broń:
            obrażenia = max(0, self.atak + self.broń.bonus_atak - przeciwnik.obrona)
        else:
            obrażenia = max(0, self.atak - przeciwnik.obrona)
        przeciwnik.otrzymaj_obrażenia(obrażenia)
        return obrażenia

    def kup_przedmiot(self, przedmiot):
        if self.złoto >= przedmiot.koszt:
            self.złoto -= przedmiot.koszt
            if isinstance(przedmiot, Broń):
                print(f"Zakupiłeś {przedmiot.nazwa}. Twoja nowa broń: {przedmiot.nazwa} (Bonus Ataku: {przedmiot.bonus_atak})")
                self.broń = przedmiot
            else:
                self.atak += przedmiot.bonus_atak
                self.obrona += przedmiot.bonus_obrona
                print(f"Zakupiłeś {przedmiot.nazwa}. Twoje nowe statystyki: Atak {self.atak}, Obrona {self.obrona}")
        else:
            print("Nie masz wystarczająco złota, aby kupić ten przedmiot.")

    def przywołaj_zwierzaka(self):
        self.zwierzak = Zwierzak()
        print("Przywołałeś swojego zwierzaka! Pomoc jest na blisku.")

class Przeciwnik(Postać):
    def __init__(self, imię, zdrowie, atak, obrona, nagroda_złoto):
        super().__init__(imię, zdrowie, atak, obrona, nagroda_złoto)

class Kupiec:
    def __init__(self):
        self.przedmioty_na_sprzedaż = [
            Przedmiot("Mikstura zdrowia", 20, 0, 10),
            Broń("Miecz", 5, 0, 15),
            Broń("Topór", 8, 0, 20),
            Broń("Łuk", 4, 0, 12),
            Przedmiot("Tarcza", 0, 10, 10),
            Przedmiot("Magiczny Pergamin", 10, 5, 20),
            Przedmiot("Zbroja", 0, 15, 25),
            Przedmiot("Eliksir Szybkości", 30, 0, 15)
        ]

    def oferuj_przedmioty(self):
        print("Kupiec oferuje następujące przedmioty:")
        for i, przedmiot in enumerate(self.przedmioty_na_sprzedaż, 1):
            print(f"{i}. {przedmiot.nazwa} - {przedmiot.koszt} złota")

    def sprzedaj_przedmiot(self, gracz, indeks_przedmiotu):
        if 1 <= indeks_przedmiotu <= len(self.przedmioty_na_sprzedaż):
            przedmiot = self.przedmioty_na_sprzedaż[indeks_przedmiotu - 1]
            gracz.kup_przedmiot(przedmiot)
            del self.przedmioty_na_sprzedaż[indeks_przedmiotu - 1]
        else:
            print("Nieprawidłowy indeks przedmiotu.")

class Przedmiot:
    def __init__(self, nazwa, bonus_atak, bonus_obrona, koszt):
        self.nazwa = nazwa
        self.bonus_atak = bonus_atak
        self.bonus_obrona = bonus_obrona
        self.koszt = koszt

class Broń(Przedmiot):
    def __init__(self, nazwa, bonus_atak, bonus_obrona, koszt):
        super().__init__(nazwa, bonus_atak, bonus_obrona, koszt)

class Zwierzak:
    def __init__(self):
        self.atak = 5
        self.zdrowie = 20

    def żyje(self):
        return self.zdrowie > 0

    def otrzymaj_obrażenia(self, obrażenia):
        self.zdrowie -= obrażenia

    def zaatakuj_przeciwnika(self, przeciwnik):
        obrażenia = max(0, self.atak - przeciwnik.obrona)
        przeciwnik.otrzymaj_obrażenia(obrażenia)
        return obrażenia

def generuj_przeciwnika():
    typy_przeciwników = [
        {"nazwa": "Goblin", "zdrowie": 30, "atak": 10, "obrona": 5, "nagroda_złoto": 15},
        {"nazwa": "Ork", "zdrowie": 40, "atak": 15, "obrona": 8, "nagroda_złoto": 20},
        {"nazwa": "Troll", "zdrowie": 60, "atak": 20, "obrona": 10, "nagroda_złoto": 25},
        {"nazwa": "Smok", "zdrowie": 80, "atak": 25, "obrona": 15, "nagroda_złoto": 30}
    ]
    przeciwnik = random.choice(typy_przeciwników)
    return Przeciwnik(przeciwnik["nazwa"], przeciwnik["zdrowie"], przeciwnik["atak"], przeciwnik["obrona"], przeciwnik["nagroda_złoto"])

def generuj_przeciwników(liczba_przeciwników):
    przeciwnicy = [generuj_przeciwnika() for _ in range(liczba_przeciwników)]
    return przeciwnicy

def wybierz_drogę():
    print("Stoisz na skrzyżowaniu. Wybierz drogę:")
    print("1. Droga w lewo")
    print("2. Droga w prawo")
    wybór = input("Twój wybór: ")
    return wybór

def main():
    gracz = Postać("Gracz", 100, 20, 10, 50)
    przeciwnicy = generuj_przeciwników(10)
    kupiec = Kupiec()

    print("Witaj w Tekstowej Przygodowej Grze RPG!")
    print("Znajdujesz się w mrocznej jaskini.")

    while gracz.żyje():
        wybór_drogi = wybierz_drogę()

        if wybór_drogi == "1":
            print("Idziesz drogą w lewo...")
            
        elif wybór_drogi == "2":
            print("Idziesz drogą w prawo...")
           
        else:
            print("Nieprawidłowy wybór. Wybierz ponownie.")
            continue

        przeciwnik = random.choice(przeciwnicy)
        print(f"Dziki {przeciwnik.imię} się pojawił!")

        while przeciwnik.żyje() and gracz.żyje():
            print(f"\n{gracz.imię} (Zdrowie: {gracz.zdrowie}, Złoto: {gracz.złoto}) vs {przeciwnik.imię} (Zdrowie: {przeciwnik.zdrowie})")
            akcja = input("Czy chcesz (a)ttakować, (u)ciekać, przywołać (z)wierzaka, czy odwiedzić (k)upca? ").lower()

            if akcja == "a":
                obrażenia = gracz.zaatakuj_przeciwnika(przeciwnik)
                print(f"Zadałeś {obrażenia} obrażeń {przeciwnik.imię}!")

                if gracz.zwierzak and gracz.zwierzak.żyje():
                    obrażenia_zwierzaka = gracz.zwierzak.zaatakuj_przeciwnika(przeciwnik)
                    print(f"{gracz.zwierzak} zadał {obrażenia_zwierzaka} obrażeń {przeciwnik.imię}!")

                if przeciwnik.żyje():
                    obrażenia_przeciwnika = przeciwnik.zaatakuj_przeciwnika(gracz)
                    print(f"{przeciwnik.imię} zadał ci {obrażenia_przeciwnika} obrażeń!")

            elif akcja == "u":
                print("Uciekasz z walki.")
                break

            elif akcja == "k":
                kupiec.oferuj_przedmioty()
                indeks_przedmiotu = int(input("Podaj numer przedmiotu, który chcesz kupić (0, aby anulować): "))
                if indeks_przedmiotu == 0:
                    continue
                kupiec.sprzedaj_przedmiot(gracz, indeks_przedmiotu)

            elif akcja == "z":
                if not gracz.zwierzak or not gracz.zwierzak.żyje():
                    gracz.przywołaj_zwierzaka()
                else:
                    print("Twój zwierzak już ci towarzyszy.")

        if gracz.żyje():
            print(f"Pokonałeś {przeciwnik.imię}! Zostało ci {gracz.zdrowie} zdrowia.\n")
            
            if random.random() < 0.3:
                print("Spotkałeś kupca!")
                kupiec.oferuj_przedmioty()
                indeks_przedmiotu = int(input("Podaj numer przedmiotu, który chcesz kupić (0, aby anulować): "))
                if indeks_przedmiotu != 0:
                    kupiec.sprzedaj_przedmiot(gracz, indeks_przedmiotu)
        else:
            print("Koniec gry. Zostałeś pokonany.")



class Lokacja:
    def __init__(self, nazwa, opis, wydarzenie=None, przeciwnicy=None):
        self.nazwa = nazwa
        self.opis = opis
        self.wydarzenie = wydarzenie
        self.przeciwnicy = przeciwnicy or []

    def __str__(self):
        return f"{self.nazwa} - {self.opis}"

lokacja1 = Lokacja("Leśna Polana", "Jasna i otwarta przestrzeń wśród drzew.")
lokacja2 = Lokacja("Zatrzaskane Drzwi", "Ciemne pomieszczenie, a przed tobą zatrzaskane drzwi.")
lokacja3 = Lokacja("Tajemnicza Grota", "Zagadkowa grota ukryta w górach.")
lokacja4 = Lokacja("Opuszczona Chata", "Stara, opuszczona chata pośrodku lasu.")
lokacja5 = Lokacja("Most nad Potokiem", "Stoisz na drewnianym moście nad rwącym potokiem.")
lokacje = [lokacja1, lokacja2, lokacja3, lokacja4, lokacja5]

def historia_lewa_droga():
    print("Podążasz leśną ścieżką, gdzieś w oddali słyszysz szum strumienia.")
    print("Zbliżasz się do strumienia i zauważasz coś błyszczącego pod wodą.")
    decyzja = input("Czy chcesz (z)anurkować, aby zobaczyć, co to, czy (i)ść dalej? ").lower()
    if decyzja == "z":
        print("Zanurkowałeś i znalazłeś starożytne artefakty!")
        self.złoto += 50
        print(f"Zdobyłeś 50 złota. Aktualny stan złota: {gracz.złoto}")
    elif decyzja == "i":
        print("Podążasz dalej ścieżką.")
    else:
        print("Nieprawidłowa decyzja. Kontynuujesz dalej.")

def historia_prawa_droga():
    print("Idziesz wzdłuż wąskiej ścieżki między górami. W powietrzu unosi się zapach kwiatów.")
    print("Nagle napotykasz grupę krasnoludów, którzy handlują rzadkimi ziołami.")
    decyzja = input("Czy chcesz (k)upić zioła, czy (o)depchnąć krasnoludy i iść dalej? ").lower()
    if decyzja == "k":
        print("Kupujesz kilka magicznych ziół, które mogą ci pomóc w podróży.")
        gracz.zdrowie += 10
        print(f"Zdrowie wzrosło o 10. Aktualne zdrowie: {gracz.zdrowie}")
    elif decyzja == "o":
        print("Odechujesz krasnoludy i kontynuujesz podróż.")
    else:
        print("Nieprawidłowa decyzja. Kontynuujesz dalej.")

def wydarzenie_karczma():
    print("Napotykasz karczmę na swojej drodze. W środku znajduje się tajemniczy obieżyświat.")
    decyzja = input("Czy chcesz (p)oczekaj na rozmowę z obieżyświatem, czy (o)dejdź? ").lower()
    if decyzja == "p":
        print("Obieżyświat dzieli się z tobą cennymi informacjami na temat okolicznych krain.")
        print("Za pomocą swojej wiedzy zyskujesz +5 do ataku.")
        gracz.atak += 5
        print(f"Twój atak wzrósł do {gracz.atak}.")
    elif decyzja == "o":
        print("Decydujesz się odejść od karczmy.")
    else:
        print("Nieprawidłowa decyzja. Kontynuujesz dalej.")

def zmień_lokację():
    global gracz, lokacje
    nowa_lokacja = random.choice(lokacje)
    print(f"Przemierzasz ścieżkę i docierasz do {nowa_lokacja}. {nowa_lokacja.opis}\n")
    lokacje.remove(nowa_lokacja)
    lokacje.append(Lokacja("Nieznana Lokacja", "To miejsce już odwiedziłeś.", []))
    gracz.zdrowie = gracz.maksymalne_zdrowie

def main():
    gracz = Postać("Gracz", 100, 20, 10, 50)
    przeciwnicy = generuj_przeciwników(10)
    kupiec = Kupiec()

    print("Witaj w Tekstowej Przygodowej Grze RPG!")
    print("Znajdujesz się w mrocznej jaskini.")

    while gracz.żyje():
        wybór_drogi = wybierz_drogę()

        if wybór_drogi == "1":
            historia_lewa_droga()
        elif wybór_drogi == "2":
            historia_prawa_droga()
        else:
            print("Nieprawidłowy wybór. Wybierz ponownie.")
            continue

        przeciwnik = random.choice(przeciwnicy)
        print(f"Dziki {przeciwnik.imię} się pojawił!")

        while przeciwnik.żyje() and gracz.żyje():
            print(f"\n{gracz.imię} (Zdrowie: {gracz.zdrowie}, Złoto: {gracz.złoto}) vs {przeciwnik.imię} (Zdrowie: {przeciwnik.zdrowie})")
            akcja = input("Czy chcesz (a)ttakować, (u)ciekać, przywołać (z)wierzaka, czy odwiedzić (k)upca? ").lower()

            if akcja == "a":
                obrażenia = gracz.zaatakuj_przeciwnika(przeciwnik)
                print(f"Zadałeś {obrażenia} obrażeń {przeciwnik.imię}!")

                if gracz.zwierzak and gracz.zwierzak.żyje():
                    obrażenia_zwierzaka = gracz.zwierzak.zaatakuj_przeciwnika(przeciwnik)
                    print(f"{gracz.zwierzak} zadał {obrażenia_zwierzaka} obrażeń {przeciwnik.imię}!")

                if przeciwnik.żyje():
                    obrażenia_przeciwnika = przeciwnik.zaatakuj_przeciwnika(gracz)
                    print(f"{przeciwnik.imię} zadał ci {obrażenia_przeciwnika} obrażeń!")

            elif akcja == "u":
                print("Uciekasz z walki.")
                break

            elif akcja == "k":
                kupiec.oferuj_przedmioty()
                indeks_przedmiotu = int(input("Podaj numer przedmiotu, który chcesz kupić (0, aby anulować): "))
                if indeks_przedmiotu == 0:
                    continue
                kupiec.sprzedaj_przedmiot(gracz, indeks_przedmiotu)

            elif akcja == "z":
                if not gracz.zwierzak or not gracz.zwierzak.żyje():
                    gracz.przywołaj_zwierzaka()
                else:
                    print("Twój zwierzak już ci towarzyszy.")

        if gracz.żyje():
            print(f"Pokonałeś {przeciwnik.imię}! Zostało ci {gracz.zdrowie} zdrowia.\n")

            if random.random() < 0.3:
                print("Spotkałeś kupca!")
                kupiec.oferuj_przedmioty()
                indeks_przedmiotu = int(input("Podaj numer przedmiotu, który chcesz kupić (0, aby anulować): "))
                if indeks_przedmiotu != 0:
                    kupiec.sprzedaj_przedmiot(gracz, indeks_przedmiotu)
            elif random.random() < 0.5:
                wydarzenie_karczma()
            else:
                zmień_lokację()
        else:
            print("Koniec gry. Zostałeś pokonany.")

if __name__ == "__main__":
    main()