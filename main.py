import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
def checkIfAnyIsEmpty(centers):
        for i in centers.values():
                if len(i) == 0:
                        return True
        return False
def recopilateCodes():
        centros = dict()
        for j in ["29", "41","04" ,"11", "14", "18", "21", "23"]:
                for i in ["Sección de Educación Secundaria Obligatoria","Instituto de Educación Secundaria","Centro de Convenio"]:
                        driver = webdriver.Firefox(firefox_profile=profile, executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
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
                                        flag = False
                                        for img in tr.find_elements_by_xpath("./child::*")[7].find_elements_by_xpath("./child::*"):
                                                if "secundaria" in img.get_attribute("src").lower():
                                                        flag = True
                                                        break
                                        td = tr.find_elements_by_xpath("./child::*")
                                        codigo = td[1].find_elements_by_xpath("./child::*")[0].text.strip()
                                        codigo = "0"*(len(codigo)-8) + codigo
                                        if "buscacentro" in tr.get_attribute("onclick").lower() and flag:
                                                centros[codigo] = []
                                                print(f"Recopilado el centro de código {codigo}")
                                except:
                                        continue
                        driver.close()
        return centros
profile = webdriver.FirefoxProfile()
# # ajax-loading.gif Buscar imagen para mejorar
profile.DEFAULT_PREFERENCES['frozen']['security.fileuri.strict_origin_policy']= True
centros = recopilateCodes()
while checkIfAnyIsEmpty(centros):
        prov = ["Málaga", "Sevilla","Almería","Cádiz","Córdoba", "Granada","Huelva" ,"Jaén"]
        p = 0
        for j in ["29", "41","04" ,"11", "14", "18", "21", "23"]:
                for i in ["Sección de Educación Secundaria Obligatoria","Instituto de Educación Secundaria","Centro de Convenio"]:
                        driver = webdriver.Firefox(firefox_profile=profile, executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
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
                                        flag = False
                                        for img in tr.find_elements_by_xpath("./child::*")[7].find_elements_by_xpath("./child::*"):
                                                if "secundaria" in img.get_attribute("src").lower():
                                                        flag = True
                                                        break
                                        td = tr.find_elements_by_xpath("./child::*")
                                        codigo = td[1].find_elements_by_xpath("./child::*")[0].text.strip()
                                        codigo = "0"*(len(codigo)-8) + codigo
                                        if "buscacentro" in tr.get_attribute("onclick").lower() and flag and len(centros[codigo]) == 0:
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
                                                fpb, fpgm, fpgs, bach = [], [], [], "No"
                                                centro = driver.find_elements_by_class_name("centro")[1].text.split("\n")
                                                for line in centro:
                                                        line_min = line.lower()
                                                        if "Formación Profesional".lower() in line_min:
                                                                fpb.append(line)
                                                        if "Medio".lower() in line_min:
                                                                fpgm.append(line)
                                                        if "Bachillerato".lower() in line_min:
                                                                bach = "Si"
                                                        if "Superior".lower() in line_min:
                                                                fpgs.append(line)
                                                centros[codigo] = [nombre_centro, prov[p], municipio, bach, "-".join(fpb), "-".join(fpgm), "-".join(fpgs), inglesBil, francesBil, alemanBil, 0, 0, 0, 0]
                                                print(f"{codigo} => {centros[codigo]}")
                                                driver.execute_script('document.getElementById("impresion").childNodes[1].childNodes[1].click()')
                                                time.sleep(0.5)
                                except:
                                        continue
                        driver.close()
                p += 1
driver = webdriver.Firefox(firefox_profile=profile, executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
driver.get("http://www.juntadeandalucia.es/educacion/vscripts/dgpc/pf20/index.asp")
driver.find_elements_by_id("botonLogin")[1].click()
time.sleep(1)
tr = driver.find_elements_by_tag_name("table")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[2:176]
ids = ["00590005", "10590005", "11590005", "12590005"]
n_tr = len(tr)
i = 0
id = -len(ids)
while len(ids) > 0 and i < n_tr:
        td = tr[i].find_elements_by_xpath("./child::*")
        title = td[0].text
        j = 0
        print(title)
        while j < len(ids):
                if ids[j] in title:
                        for l in range(1,9):
                                td = tr[i].find_elements_by_xpath("./child::*")
                                num_teachers = int(td[l].text.strip())
                                if  num_teachers != 0:
                                        td[l].find_elements_by_xpath("./child::*")[0].click()
                                        tr_temp = driver.find_elements_by_tag_name("table")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[1::]
                                        for k in tr_temp:
                                                td_temp = k.find_elements_by_xpath("./child::*")
                                                codigo = td_temp[0].text.strip().replace("(","").replace(")","").split(" ")[0]
                                                plazas = int(td_temp[2].text.strip())
                                                try:
                                                        centros[codigo][id]= plazas
                                                        print(f"{codigo} => {plazas}")
                                                except:
                                                        pass
                                        driver.close()
                                        driver = webdriver.Firefox(firefox_profile=profile, executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
                                        driver.get("http://www.juntadeandalucia.es/educacion/vscripts/dgpc/pf20/index.asp")
                                        driver.find_elements_by_id("botonLogin")[1].click()
                                        time.sleep(1)
                                tr = driver.find_elements_by_tag_name("table")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[2:176]
                        ids.pop(j)
                        id += 1
                j += 1
        i += 1
        time.sleep(1)
        tr = driver.find_elements_by_tag_name("table")[1].find_elements_by_xpath("./child::*")[0].find_elements_by_xpath("./child::*")[2:176]
driver.close()
dumb =set()
ids = ["00590005", "10590005", "11590005", "12590005"]
duration = 1
header = f"CODIGO NOMBRE_CENTRO PROVINCIA MUNICIPIO BACH FPB FPGM FPGS INGLES FRANCES ALEMAN PLAZAS_NORMAL PLAZAS_FRANCES PLAZAS_INGLES PLAZAS_ALEMAN"
driver = webdriver.Firefox(firefox_profile=profile, executable_path=".\\geckodriver-v0.29.1-win64\\geckodriver.exe")
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
driver.find_element_by_id("Sección de Educación Secundaria Obligatoria").click()
time.sleep(duration / 2)
driver.find_element_by_id("Instituto de Educación Secundaria").click()
time.sleep(duration / 2)
driver.find_element_by_id("Centro de Convenio").click()
time.sleep(duration / 2)
driver.find_element_by_id("Instituto de Educación Secundaria").click()
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
                if codigo in centros:
                        vacantes = int(temp[6].strip().split(" ")[0])
                        tables = driver.find_elements_by_tag_name("table")
                        interns = dict()
                        for body in tables:
                                type_intern = body.find_elements_by_tag_name("tbody")[0].find_elements_by_xpath("./child::*")[3].text.upper().replace(" ","_")
                                if type_intern not in interns and type_intern != "":
                                        interns[type_intern] = 0
                                try:
                                        interns[type_intern] += 1
                                except:
                                        pass
                        centros[codigo].append(vacantes)
                        centros[codigo].append(interns)
                        dumb = dumb | set(interns.keys())
                        print(f"Codigo:{codigo} Vacantes:{vacantes} Tipo:{interns}")
        time.sleep(duration)
        interns = " ".join(dumb)
        header += f"PLAZAS_MAPA_{j} {interns}"

header = ";".join(header.split(' '))
driver.close()
file = open(datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")+".csv", "w+")
file.write(f"{header}\n")
for i in centros:
        print(f"{i} => {centros[i]}")
        temp = f"{i};"
        size = len(centros[i]) - len(ids) * 4
        for j in range(size):
                temp += str(centros[i][j]) + ";"
        for k in range(int(len(ids) / 4)):
                try:
                        temp += f"{str(centros[i][size + k])};"
                except:
                        temp += "0;"
                t = 1 + 2 * k + size
                for j in interns.split(" "):
                        try:
                                if j in centros[i][t]:
                                        temp += str(centros[i][t + 1][j]) + ";"
                                else:
                                        temp += "0;"
                        except:
                                temp += "None;"
        file.write(f"{temp}\n")
file.close()