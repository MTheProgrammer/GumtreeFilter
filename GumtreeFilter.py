from urllib.request import Request
from urllib.request import urlopen

#https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/krakow/page-2/v1c9008l3200208p2?nr=2
#href="/a-mieszkania-i-domy-do-wynajecia/krakow/mieszkanie-do-wynaj%C4%99cia-w-centrum-nowej-huty-50-m2/1001982788890911159891709">Mieszkanie do wynajęcia w centrum Nowej Huty 50 m2</a>

#Parametry
number_of_pages = 20
wanted = b"/a-mieszkania-i-domy-do-wynajecia/krakow"
expected = "Bronowice", "bronowice", "AGH", "agh", "Agh", "Mogilskie", "mogilskie", "Mogilskiego", "mogilskiego", "Armii", "armii", "Krajowej", "krajowej", "Zarzecze", "zarzecze", "Kijowska", "kijowska", "balkon", "Stańczyka", "stańczyka", "Stanczyka", "stanczyka", "Krowodrza", "krowodrza"
unexpected = "elektryczne", "gazowe", "prowizja", "Prowizja", "aneks", "Aneks", "kuchenny", "aneksem", "Prokocim", "Czyżyny", "Ruczaj", "Huta"

#Reszta zmiennych
filtered_list = []
result_url_list = []
offer_index = 0


#Strony glowne
for page_index in range(1, number_of_pages + 1):
    if page_index == 1:
        url = "https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/krakow/v1c9008l3200208p1?nr=2"
    else:
        url = "https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/krakow/page-{}/v1c9008l3200208p2?nr=2".format(page_index)

    try:
        req = Request(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.27 (KHTML, like Gecko) Chrome/26.0.1384.2 Safari/537.27"})
        response = urlopen(req)
        the_page = response.read()
        data = the_page.split()

        #Listy do wyciagania URL ogloszen
        urllist = []
        ready_url_list = []

        for url in data:
            if wanted in url:
                urllist.append(url)

        for url in urllist:
            tmp = url.split(b'\"')
            for part in tmp:
                if wanted in part:
                    ready_url_list.append(part)

        #Ogloszenia
        for ready_url in ready_url_list:
            try:
                home_url = "https://www.gumtree.pl" + ready_url.decode()
                req = Request(home_url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.27 (KHTML, like Gecko) Chrome/26.0.1384.2 Safari/537.27"})
                response = urlopen(req)
                the_page = response.read()
                data = the_page.split(b'\n')

                #***********************************
                #FILTROWANIE
                #***********************************
                offer_index += 1
                print("Checking offer number", offer_index)

                #Wycinamy odpowiedni fragment strony
                del data[1650:]
                del data[:1500]

                #Lista na content
                content = []

                #Flaga okresla czy dotarlismy do contentu
                is_begun = False

                #Wycinamy wlasciwy content
                for line in data:
                    if is_begun:
                        if b'</div>' in line:
                            break
                        content.append(line.decode())
                    else:
                        if b'style="font-family: inherit; white-space: pre-wrap;"' in line:
                            is_begun = True

                try:
                    content = "\n".join(content)
                    #??????????????????????????
                    #print(content)
                except:
                    print("Nie ma co polaczyc!")

                try:
                    good = False
                    for exp in expected:
                        if not good and not content.find(exp) == -1:
                            good = True
                    for unexp in unexpected:
                        if good and not content.find(unexp) == -1:
                            good = False
                    if good:
                        print("Adding: " + home_url)
                        filtered_list.append(home_url)

                except:
                    print("Filtrowanie nie pyklo")

            except:
                print("Nie udalo sie wczytac strony.")

    except:
        print("Nie udalo sie wczytac strony.")

    newfile = open("gumtree.txt", "w")
    for url in filtered_list:
        newfile.write(url + "\n")
    newfile.close()
