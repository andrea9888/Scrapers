from bs4 import BeautifulSoup
import requests
from Accomodation import mycol

def getTagContent(htmlString,tag):
    konacna_lista_sadrzaja=[]
    def ima_li_taga(htmlString,tag):
        tag_1='<'+tag
        brojac=0 #broji da li se svi brojevi u nazivu taga poklapaju
        for (count,elem) in enumerate(htmlString):
            if elem==tag_1[0]:
                if htmlString[count+1]==tag_1[1]:
                    brojac=1 
                    for count2 in range(1,len(tag)):
                        if htmlString[count+1+count2]==tag[count2]:
                            brojac=brojac+1
                    if brojac==len(tag):
                        return True
                    
    while 1:
        if (ima_li_taga(htmlString,tag))==True:
            tag_1='<'+tag
            tag_2=tag+'>'
            lista1=htmlString.partition(tag_1)
            lista2=lista1[2].partition(tag_2)
            konacna_lista_sadrzaja.append(lista2[0])
            htmlString=lista2[2]
        else:
            break
  
    konacna_lista_sadrzaja_bez_oznaka=[]
    for elem in konacna_lista_sadrzaja:
        pocetak=elem.find(">")
        kraj=elem.find('</')
        konacna_lista_sadrzaja_bez_oznaka.append(elem[pocetak+1:kraj].replace('\n', '').lstrip().rstrip())
    return konacna_lista_sadrzaja_bez_oznaka

def get_content(content_name, link1, a):
    #print(str(link1).split("strong>"))
    last_change=str(link1).split("strong>").index(content_name+'</')
    if a!="":
        return str(link1).split("strong>")[last_change+1].split('\n')[0].strip(': ')[:-len(a)]
    else:
        return str(link1).split("strong>")[last_change+1].split('\n')[0].strip(': ')
i=0
while 1:
    try:
        source = requests.get(f'https://www.realitica.com/?cur_page={i}&for=DuziNajam&pZpa=Crna+Gora&pState=Crna+Gora&type%5B%5D=&lng=hr').text


        html = BeautifulSoup(source,'lxml')
        link = html.find_all('div', class_ = 'thumb_div')
        for elem in link:
            url=elem.a['href']
            source1=requests.get(url).text
            html1 = BeautifulSoup(source1,'lxml')
            link1 = html1.find_all('div', style= 'clear:both;')
            a = ""
            diction = {"Zadnja Promjena" : get_content("Zadnja Promjena",link1, a)}
            diction.update({"Oglas Broj" : get_content("Oglas Broj",link1, a)})
            help = 0
            for ad in mycol.find():
                if ad["Oglas Broj"] == diction["Oglas Broj"]:
                    if ad["Zadnja Promjena"] == diction["Zadnja Promjena"]:
                        help = 2
                        break
                    help = 1
                    break
            if help == 2:
                print("Ad already exsists!")
                continue
            link1 = html1.find_all('div', id= 'listing_body')
            b = "<br/><"
            list_of_fields = getTagContent(str(link1), "strong")
            '''
            if "Lokacija" in list_of_fileds and "Opis" in list_of_fileds and "Oglasio " in list_of_fileds and "Oglas Broj" in list_of_fileds and "Oglas Broj" in list_of_fileds:
                print("dasd")
            else:
                print("nee") 
            print(list_of_fields, "strong"))
            '''
            for elem in list_of_fields:
                diction.update({elem.lower() : get_content(elem,link1, b)})
                '''
                diction.update({"područje" : get_content("Područje",link1, b)})
                diction.update({"lokacija" : get_content("Lokacija",link1, b)})
                diction.update({"broj spavaćih soba" : get_content("Spavaćih Soba",link1, b)})
                diction.update({"broj kupatila" : get_content("Kupatila",link1, b)})
                '''


            


            
        
                

            print(diction)
            print("--------------------")
           
        
            
          
                

        i=i+1
    except Exception as e:
            print(str(e))
            
            break
