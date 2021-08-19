import sys
import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
input = sys.argv[1::]
header = "CODIGO NOMBRE_CENTRO PROVINCIA MUNICIPIO BACH FPB FPGM FPGS E_ESPECIAL E_ADULTO_BACH E_ADULTO_ESO INGLES FRANCES ALEMAN "
input_size = len(input)
def id_val(val):
        res = []
        for j in val.split(","):
                if len(j) != 8 and j in res:
                        print(f"Error con el formato del id {j}")
                        exit()
                res += [j]
        return res
def type(val):
        res = ["secundaria", "bachillerato"]
        if val == "--ALL":
                return res
        temp = []
        for j in val.split(","):
                if j in res:
                        temp += [j]
        if not len(temp):
                print("No se ha encontrado ninguna coincidencia con el tipo de centro")
                exit()
        return temp
val = dict()
for j in range(0,input_size, 2):
        try:
                if input[j] == "-id":
                        val[input[j]] = id_val(input[j + 1])
                elif input[j] == "-t":
                        val[input[j]] = type(input[j + 1])
                else:
                        print("Input no está definido correctamente")
                        exit()
        except:
                print("Input no está definido correctamente")
                exit()
provincias = ["29", "41","04" ,"11", "14", "18", "21", "23"] #De momento No cambiar esto, por defecto leerá de todas las provincias
provincias_names = ["Málaga", "Sevilla","Almería","Cádiz","Córdoba", "Granada","Huelva" ,"Jaén"]
type_of_center = ["Sección de Educación Secundaria Obligatoria","Instituto de Educación Secundaria","Centro de Convenio"] #Deberá de poderse modificar por entrada por teclado
# list_ids = ["00590005", "10590005", "11590005", "12590005"] #Deberá de poderse modificar por una entrada por teclado
# types_center_valid = ["secundaria", "bachillerato"] #De momento se quedará así
list_ids = val["-id"]
types_center_valid = val["-t"]
print(list_ids)
print(types_center_valid)

def centerIsValid(img):
        for k in types_center_valid:
                if k in img:
                        return True
        return False
def checkIfAnyIsEmpty(centers):
        for i in centers.values():
                if len(i) == 0:
                        return True
        return False
def recopilateCodes():
        centros = dict()
        for i in type_of_center:
                driver = webdriver.Firefox(executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
                for k in range(2):
                        driver.get("http://www.juntadeandalucia.es/educacion/vscripts/centros/index.asp")
                        driver.find_element_by_id("solapastab1").click()
                        Select(driver.find_element_by_id("PROVINCIA")).select_by_value("00")
                        driver.find_element_by_id("publica").click()
                        Select(driver.find_element_by_id("dengen")).select_by_value(i)
                        for t in driver.find_elements_by_tag_name("div")[0].find_elements_by_tag_name("a"):
                                if t.get_attribute("onclick") != None:
                                        if "envioconsulta" in t.get_attribute("onclick").lower():
                                                t.click()
                                                break
                time.sleep(10) #Podemos sustituir esto por un checkeo que revise el loader ajax-loading.gif
                for tr in driver.find_elements_by_tag_name("tr"):
                        try:
                                flag = False
                                for img in tr.find_elements_by_xpath("./child::*")[7].find_elements_by_xpath("./child::*"):
                                        if centerIsValid(img.get_attribute("src").lower()):
                                                flag = True
                                                break
                                td = tr.find_elements_by_xpath("./child::*")
                                codigo = td[1].find_elements_by_xpath("./child::*")[0].text.strip()
                                codigo = "0"*(len(codigo)-8) + codigo
                                if flag:
                                        centros[codigo] = []
                                        print(f"Recopilado el centro de código {codigo}")
                        except:
                                continue
                driver.close()
        return centros
def recopilateCenters(centros, ids):
        while checkIfAnyIsEmpty(centros):
                prov = provincias_names
                p = 0
                for j in provincias:
                        for i in type_of_center:
                                driver = webdriver.Firefox(executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
                                for k in range(2):
                                        driver.get("http://www.juntadeandalucia.es/educacion/vscripts/centros/index.asp")
                                        driver.find_element_by_id("solapastab1").click()
                                        Select(driver.find_element_by_id("PROVINCIA")).select_by_value(j)
                                        driver.find_element_by_id("publica").click()
                                        Select(driver.find_element_by_id("dengen")).select_by_value(i)
                                        for t in driver.find_elements_by_tag_name("div")[0].find_elements_by_tag_name("a"):
                                                        if t.get_attribute("onclick") != None:
                                                                if "envioconsulta" in t.get_attribute("onclick").lower():
                                                                        t.click()
                                                                        break
                                time.sleep(5)
                                for tr in driver.find_elements_by_tag_name("tr"):
                                        try:
                                                td = tr.find_elements_by_xpath("./child::*")
                                                codigo = td[1].find_elements_by_xpath("./child::*")[0].text.strip()
                                                if len(centros[codigo]) == 0:
                                                        nombre_centro = td[2].text.strip()
                                                        municipio = td[3].text.strip()
                                                        inglesBil = "No"
                                                        francesBil = "No"
                                                        alemanBil = "No"
                                                        for img in td[9].find_elements_by_xpath("./child::*"):
                                                                lang = img.get_attribute("src")
                                                                if "CBI" in lang:
                                                                        inglesBil = "Si"
                                                                if "CBF" in lang:
                                                                        francesBil = "Si"
                                                                if "CBA" in lang:
                                                                        alemanBil = "Si"
                                                        td[1].click()
                                                        driver.find_elements_by_tag_name("ul")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[1].click()
                                                        fpb, fpgm, fpgs, bach, ee, eab, eas = "No", "No", "No", "No", "No", "No", "No"
                                                        centro = driver.find_elements_by_class_name("centro")[1].text.split("\n")
                                                        for line in centro:
                                                                line_min = line.lower()
                                                                if "Formación Profesional".lower() in line_min:
                                                                        fpb = "Si"
                                                                if "Medio".lower() in line_min:
                                                                        fpgm = "Si"
                                                                if "Bachillerato".lower() in line_min:
                                                                        bach = "Si"
                                                                if "Superior".lower() in line_min:
                                                                        fpgs = "Si"
                                                                if "adulta" in line_min:
                                                                        if "bachiller" in line_min:
                                                                                eab = "Si"
                                                                        elif "e.s.o".lower() in line_min:
                                                                                eas = "Si" 
                                                                if "Especial".lower() in line_min:
                                                                        ee = "Si"
                                                        centros[codigo] = [nombre_centro, prov[p], municipio, bach, fpb, fpgm, fpgs, ee, eab, eas,inglesBil, francesBil, alemanBil] + [0 for i in range(len(ids))]
                                                        print(f"{codigo} => {centros[codigo]}")
                                                        driver.execute_script('document.getElementById("impresion").childNodes[1].childNodes[1].click()')
                                                        time.sleep(0.5)
                                        except:
                                                continue
                                driver.close()
                        p += 1
        return centros
def plazasByCenter(centros, list_ids, header):
        driver = webdriver.Firefox(executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
        driver.get("http://www.juntadeandalucia.es/educacion/vscripts/dgpc/pf20/index.asp")
        driver.find_elements_by_id("botonLogin")[1].click()
        time.sleep(1)
        tr = driver.find_elements_by_tag_name("table")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[2:176]
        ids = list_ids.copy()
        n_tr = len(tr)
        i = 0
        title_subject = dict()
        id = -len(ids)
        while len(ids) > 0 and i < n_tr:
                td = tr[i].find_elements_by_xpath("./child::*")
                title = td[0].text
                print(title)
                title = title.split(" ")
                temp_title = title[0].replace("(","").replace(")","").strip()
                if temp_title in ids: 
                        for l in range(1,9):
                                td = tr[i].find_elements_by_xpath("./child::*")
                                num_teachers = int(td[l].text.strip())
                                if  num_teachers != 0:
                                        td[l].find_elements_by_xpath("./child::*")[0].click()
                                        time.sleep(0.5)
                                        tr_temp = driver.find_elements_by_tag_name("table")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[1::]
                                        for k in tr_temp:
                                                td_temp = k.find_elements_by_xpath("./child::*")
                                                codigo = td_temp[0].text.strip().replace("(","").replace(")","").split(" ")[0]
                                                if codigo in centros:
                                                        plazas = int(td_temp[2].text.strip())
                                                        centros[codigo][id]= plazas
                                                        print(f"{codigo} => {plazas}")
                                        driver.close()
                                        driver = webdriver.Firefox(executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
                                        driver.get("http://www.juntadeandalucia.es/educacion/vscripts/dgpc/pf20/index.asp")
                                        driver.find_elements_by_id("botonLogin")[1].click()
                                        time.sleep(1)
                                        tr = driver.find_elements_by_tag_name("table")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[2:176]
                        ids.pop(ids.index(temp_title))
                        title_subject[temp_title] = "_".join(title[1::]).upper()
                        header += f"PLAZAS_ASIGNATURA_{temp_title} "
                        id += 1
                i += 1
        driver.close()
        return centros, header, title_subject
def plazasByCenterMap(centros, list_ids, header, titles):
        ids = list_ids.copy()
        duration = 1
        t = 2
        driver = webdriver.Firefox(executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
        driver.get("https://www.mapavacantesandalucia.es/")
        driver.find_elements_by_class_name("menu-icon")[0].click()
        time.sleep(duration)
        driver.find_elements_by_class_name("accordion-title")[0].click()
        time.sleep(duration / 2)
        Select(driver.find_element_by_id("select-cuerpo")).select_by_value("590")
        time.sleep(duration / 2)
        driver.find_elements_by_class_name("accordion-title")[1].click()
        time.sleep(duration / 2)
        driver.find_elements_by_id("todos-provincia")[0].click()
        time.sleep(duration / 2)
        driver.execute_script('document.getElementsByClassName("menu-icon")[0].click()')
        driver.execute_script('document.getElementsByClassName("menu-icon")[0].click()')
        time.sleep(duration / 2)
        driver.find_elements_by_class_name("accordion-title")[0].click()
        time.sleep(duration / 2)
        driver.find_elements_by_class_name("accordion-title")[2].click()
        time.sleep(duration / 2)
        driver.find_element_by_id("Instituto de Educación Secundaria").click()
        time.sleep(duration / 2)
        for k in type_of_center:
                driver.find_element_by_id(k).click()
                time.sleep(duration / 2)
        driver.find_elements_by_class_name("accordion-title")[0].click()
        driver.execute_script('document.getElementsByClassName("menu-icon")[0].click()')
        time.sleep(duration)
        for j in ids:
                driver.execute_script('document.getElementsByClassName("menu-icon")[0].click()')
                time.sleep(duration / 2)
                Select(driver.find_element_by_id("select-especialidad")).select_by_value(j)
                time.sleep(duration / 2)
                driver.execute_script('document.getElementsByClassName("menu-icon")[0].click()')
                time.sleep(duration)
                for i in range(len(driver.find_elements_by_class_name("leaflet-marker-icon"))):
                        driver.execute_script(f"document.getElementsByClassName('leaflet-marker-icon leaflet-zoom-animated leaflet-interactive')[{i}].click()")
                        centro = driver.find_element_by_id("info-centro")
                        time.sleep(duration / 2)
                        temp = centro.text.split("\n")
                        codigo = temp[0].strip().split(" ")[-1].replace("(","").replace(")", "")
                        codigo = "0"*(8 - len(codigo)) + codigo
                        if codigo in centros:
                                vacantes = int(temp[6].strip().split(" ")[0])
                                tables = driver.find_elements_by_tag_name("table")
                                interns = {
                                        "OTROS": 0,
                                        "INTERINOS_CON_TIEMPO_DE_SERVICIO": 0,
                                        "COMISIONES_DE_SERVICIO": 0
                                }
                                for body in tables:
                                        type_intern = body.find_elements_by_tag_name("tbody")[0].find_elements_by_xpath("./child::*")[3].text.upper().replace(" ","_")
                                        if type_intern != "":
                                                if type_intern in interns:
                                                        interns[type_intern] += 1
                                                else:
                                                        interns["OTROS"] += 1
                                centros[codigo].append(vacantes)
                                centros[codigo].append(interns)
                                print(f"Codigo:{codigo} Vacantes:{vacantes} Tipo:{interns}")
                        driver.execute_script('document.getElementsByClassName("close-button")[1].click()')
                        time.sleep(duration / 2)
                time.sleep(duration)
                for k in centros:
                        if len(centros[k]) < 13 + len(list_ids) + t:
                                centros[k].append(0)
                                centros[k].append({
                                        "OTROS": 0,
                                        "INTERINOS_CON_TIEMPO_DE_SERVICIO": 0,
                                        "COMISIONES_DE_SERVICIO": 0
                                })
                header += "PLAZAS_MAPA_" + titles[j] + " " + " ".join(interns) + " "
                t += 2
        driver.close()
        return centros, header
def writeOnCSV(centros, header):
        header = header.strip().replace(" ",";")
        file = open(datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")+".csv", "w+")
        file.write(f"{header}\n")
        for i in centros:
                print(f"{i} => {centros[i]}")
                temp = f"{i};"
                init_size = 13 + len(list_ids)
                for j in range(init_size):
                        temp += f"{centros[i][j]};"
                for j in range(init_size, len(centros[i]), 2):
                        vacantes = centros[i][j]
                        tipos = centros[i][j + 1]
                        temp += f"{vacantes};"
                        temp += f"{tipos['OTROS']};"
                        temp += f"{tipos['INTERINOS_CON_TIEMPO_DE_SERVICIO']};"
                        temp += f"{tipos['COMISIONES_DE_SERVICIO']};"
                temp += "0;" * (1 + init_size + 4 * len(list_ids) - len(temp.split(";")))
                temp = f"{temp.strip()}\n" 
                file.write(temp)
        file.close()


centros = recopilateCenters(recopilateCodes(), list_ids)
centros, header, subjects  = plazasByCenter(centros, list_ids, header)
centros, header = plazasByCenterMap(centros, list_ids, header, subjects)
writeOnCSV(centros, header)