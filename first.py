from bs4 import BeautifulSoup
import requests
from Accomodation import mycol
import datetime
import time
import os
from flask import Flask


app = Flask(__name__)
def str_to_date(string):
    date_string = string.replace(" ", "/").replace(",", "")
    return datetime.datetime.strptime(date_string, "%m/%b/%Y")

def get_tag_content(htmlString,tag):
    list_of_content=[]
    def tag_exsists(htmlString,tag):
        tag_1='<'+tag
        count1=0 
        for (count,elem) in enumerate(htmlString):
            if elem==tag_1[0]:
                if htmlString[count+1]==tag_1[1]:
                    count1=1 
                    for count2 in range(1,len(tag)):
                        if htmlString[count+1+count2]==tag[count2]:
                            count1=count1+1
                    if count1==len(tag):
                        return True
                    
    while 1:
        if (tag_exsists(htmlString,tag))==True:
            tag_1='<'+tag
            tag_2=tag+'>'
            lista1=htmlString.partition(tag_1)
            lista2=lista1[2].partition(tag_2)
            list_of_content.append(lista2[0])
            htmlString=lista2[2]
        else:
            break
    list_of_content_final=[]
    for elem in list_of_content:
        start=elem.find(">")
        end=elem.find('</')
        list_of_content_final.append(elem[start+1:end].replace('\n', '').lstrip().rstrip())
    return list_of_content_final
@app.route("/")
def get_content(content_name, link1, a):
    #print(str(link1).split("strong>"))
    html_list = str(link1).split("strong>")
    last_change=html_list.index(content_name+'</')
    if content_name == "Oglasio":
        string = html_list[last_change+1].split('\n')[0].strip(': ') + "s"
        return get_tag_content(string.split('\n')[0].strip(': '), "a")[0]
    if content_name == "Opis":
        if "<br/>" in html_list[last_change+1]:
            return html_list[last_change+1].split('\n')[0].strip(': ').split("<br/>")[0]
        else:
            return html_list[last_change+1].strip(': ')
    if content_name in ["Mobitel", "Telefon", "ME", "Mobilni"]:
        phone_number = html_list[last_change + 1].replace(" ", "")
        if phone_number[1] == "+":
            list_of_numbers = ["+"]
        else:
            list_of_numbers = ["0"]
    
        i = 2
        while i < len(phone_number):
            if phone_number[i].isnumeric():
                list_of_numbers.append(phone_number[i])
            else:
                return ''.join(list_of_numbers)
            i += 1
    if content_name in ["Novogradnja", "Klima Uređaj"]:
        return True
    if a!="":
        if content_name=="Stambena Površina":
            return int(html_list[last_change+1].split('\n')[0].strip(': ')[:-len(a)].split("<font")[0].strip("m"))
        if content_name == "Spavaćih Soba" or content_name == "Kupatila" or content_name == "Od Mora (m)" or content_name == "Parking Mjesta" :
            if content_name == "Parking Mjesta":
                if  html_list[last_change+1].split('\n')[0].strip(': ')[:-len(a)] == '':
                    return True
            return int(html_list[last_change+1].split('\n')[0].strip(': ')[:-len(a)])
        elif content_name == "Cijena":
            return float(html_list[last_change+1].split('\n')[0].strip(': ')[:-len(a)].strip("€"))
        elif content_name == "Zemljište":
            return html_list[last_change+1].split('\n')[0].strip(': ')[:-len(a)]
        else: 
            return html_list[last_change+1].split('\n')[0].strip(': ')[:-len(a)]
    else:
       return html_list[last_change+1].split('\n')[0].strip(': ')
    
i=0
while 1:
    try:
        source = requests.get(f'https://www.realitica.com/?cur_page={i}&for=DuziNajam&pZpa=Crna+Gora&pState=Crna+Gora&type%5B%5D=&lng=hr').text

        
        html = BeautifulSoup(source,'lxml')
        link = html.find_all('div', class_ = 'thumb_div')
        for elem in link:
            time.sleep(2)
            current_ad = {}
            url=elem.a['href']
            source1=requests.get(url).text
            html1 = BeautifulSoup(source1,'lxml')
            link1 = html1.find_all('div', style= 'clear:both;')
            a = ""
            try:
                current_ad = {"zadnja promjena" : str_to_date(get_content("Zadnja Promjena",link1, a))}
                current_ad.update({"oglas broj" : int( get_content("Oglas Broj",link1, a))})
            except:
                print("Ad does not contain required fields!")
                continue
            help = 0
            for ad in mycol.find():
                try:
                    if ad["oglas broj"] == current_ad["oglas broj"]:
                        if ad["zadnja promjena"] == current_ad["zadnja promjena"]:
                            help = 2
                            break
                        help = 1
                        break
                except:
                    continue
            if help == 2:
                print("Ad already exsists!")
                continue
            link1 = html1.find('div', id= 'rea_blueimp')
            list_of_images=[]
            help_list=str(link1).split("\n")
            for elem in help_list:
                if "href" in elem:
                    position=elem.split("href=")[1].index("rel")
                    list_of_images.append(elem.split("href=")[1][1:position-2])
            current_ad.update({"slike" : str(list_of_images)}) 
            if current_ad["slike"]=="[]":
                print("Ad does not contain required fields!")
                continue 
            link1 = html1.find_all('div', id= 'listing_body')
            b = "<br/><"
            
            list_of_fields = get_tag_content(str(link1), "strong")
            
            required=["Lokacija", "Opis", "Oglasio"]
            phone=['Mobitel', "Telefon", "ME", "Mobilni"]
            phone_exsists=0
            if  set(required).issubset(list_of_fields) and get_tag_content(str(link1), "h2")[0]:
                for elem in phone: 
                    if elem in list_of_fields:
                            phone_exsists=1
                if phone_exsists==1:
                    pass
                    #print("Ad has all required fields from this section")
                else:
                    print("Ad does not contain required fields!")
                    continue
            else:
                print("Ad does not contain required fields!")
                continue
            unwanted=["Zadnja Promjena", "Oglas Broj", "Tags", "Više detalja na"]
            list_of_fields=[elem for elem in list_of_fields if elem not in unwanted]
            current_ad.update({"naslov":get_tag_content(str(link1), "h2")[0]})
            for elem in list_of_fields:
                a = {elem.lower() : get_content(elem,link1, b)}
                current_ad.update(a)
            list_of_optional = ["vrsta", "pordučje", "spavaćih soba", "kupatila", "cijena", "stambena površina", "parking mjesta", "zemljište", "od mora (m)", "klima uređaj", "novogradnja", "web stranica"]
            for elem in list_of_optional:
                if elem not in current_ad.keys():
                    current_ad.update({elem:"Not stated" })
            #print(current_ad)
            try:
                if help == 1:
                    mycol.update_one({"oglas broj" : current_ad["oglas broj"]}, {"$set" :current_ad})
                    print("Successfully updated!")
                else:
                    mycol.insert_one(current_ad)
                    print("Successfully updated!")
            except Exception as e:
                print(str(e))

        

            
            
          
                

        i=i+1
        
    except Exception as e :
        print(str(e))
        print("end")    
        break
if __name__=="__main__" :
    port= int(os.environ.get("PORT", 17995))
    app.run(host="0.0.0.0", port=port) 