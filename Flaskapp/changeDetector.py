# -*- coding: utf-8 -*-

import difflib
import math
import statistics
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import util
from selenium import webdriver
from bs4 import BeautifulSoup

def change_detector(p_url, url, caso):

    # Variables
    difference                    = []
    sorted_difference             = []
    twenty_percent_elements       = []
    eighty_percent_elements       = []
    porcentajes_cambios_ordenados = []
    flatten20                     = []
    flatten80                     = []
    savecsv                       = []
    indices_cambios               = []

    unsorted_dicttexts   = []
    p_unsorted_dicttexts = []
    texts                = []
    p_texts              = []

    # Opciones del browser
    alloptions = webdriver.ChromeOptions()
    alloptions.add_argument('headless')
    alloptions.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=alloptions)
    browser.get(p_url)
    p_html = browser.page_source
    # Se guarda un screenshot de la página en el lugar correspondiente
    screenshot = util.fullpage_screenshot(browser, 'static/old_screenshot.png')
    browser.quit()

    browser = webdriver.Chrome(options=alloptions)
    browser.get(url)
    html = browser.page_source
    browser.quit()

    text   = BeautifulSoup(html, "lxml")
    divs   = text.find("div")
    head   = text.find("head")
    body   = text.find("body")
    p_text = BeautifulSoup(p_html, "lxml")
    p_divs = p_text.find("div")
    salida = ""

    counter = 0
    for item in divs.next_siblings:
        try:
            if counter == 0:
                unsorted_dicttexts.append({'id': counter, 'value': str(divs)})
                counter += 1

            unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1
        except AttributeError:
            if counter == 0:
                unsorted_dicttexts.append({'id': counter, 'value': str(divs)})
                counter += 1

            unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1

    counter = 0
    for item in p_divs.next_siblings:
        try:
            if counter == 0:
                p_unsorted_dicttexts.append({'id': counter, 'value': str(p_divs)})
                counter += 1

            p_unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1
        except AttributeError:
            if counter == 0:
                p_unsorted_dicttexts.append({'id': counter, 'value': str(p_divs)})
                counter += 1

            p_unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1

    for i in unsorted_dicttexts:
        texts.append(i['value'])

    for i in p_unsorted_dicttexts:
        p_texts.append(i['value'])

    if len(texts) == len(p_texts):

        if caso == 'diferencia'.upper():
            for iterator in range(0, len(texts)):
                if texts[iterator] is None:
                    texts[iterator] = ""
                if p_texts[iterator] is None:
                    p_texts[iterator] = ""

                result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
                difference.append(round((1 - result) * 100, 2))

            texts.sort(key=len, reverse=True)
            p_texts.sort(key=len, reverse=True)

            for iterator in range(0, len(texts)):
                result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
                sorted_difference.append(round((1 - result) * 100, 2))

            for index, element in enumerate(difference):
                if element != 0:
                    savecsv.append(1)
                    indices_cambios.append(index)
                else:
                    savecsv.append(0)

            # 20% de los bloques tienen 80% del peso
            twenty_percent_elements.append(sorted_difference[0:math.floor(len(difference) * 0.2)])  # Elementos con 80% del valor
            eighty_percent_elements.append(sorted_difference[math.floor(len(difference) * 0.2):])   # Elementos con 20% del valor

            for sublist in twenty_percent_elements:
                for item in sublist:
                    flatten20.append(item)

            for sublist in eighty_percent_elements:
                for item in sublist:
                    flatten80.append(item)

            # Asignacion del peso cuantitativo
            porcentajes_cambios_ordenados.append(flatten20)
            porcentajes_cambios_ordenados.append(flatten80)
            cambio_peso_80 = statistics.mean(porcentajes_cambios_ordenados[0]) * 0.8
            cambio_peso_20 = statistics.mean(porcentajes_cambios_ordenados[1]) * 0.2
            cambio_total   = cambio_peso_80 + cambio_peso_20

            # Aqui se hacen las manipulaciones al codigo para agregar el marco rojo que detalla el div cambiado
            # Si hubo cambios resaltar usando el id que yo le otorgué para la búsqueda
            reemplazo   = '<head>' + '\n' + '<script src="https://code.jquery.com/jquery-3.4.1.js"' \
                                            'integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU="' \
                                            'crossorigin="anonymous"></script>'
            salidafinal = sorted(unsorted_dicttexts, key=lambda k: k['id'])

            salida = salida + "<!DOCTYPE html>" + '\n' + "<html>" + '\n'
            head   = str(head).replace('<head>', reemplazo)
            salida = salida + head + '\n' + '<body>' + '\n'


            for element in indices_cambios:
                for element2 in salidafinal:
                    if element2['id'] == element:
                        if 'style' in element2['value']:
                            element2['value'] = element2['value'].replace('style="', 'style="border: 3px solid red; ', 1)
                        else:
                            reemplazo_border  = '< ' + ' style="border: 3px solid red;"'
                            element2['value'] = element2['value'].replace('<', reemplazo_border, 1)

            for element in salidafinal:
                if element['value'] != 'None':
                    salida = salida + element['value'] + '\n'

            salida = salida + "</body>" + '\n'
            salida = salida + "</html>"

            url2 = url.replace('.html', '_updated.html')
            g = open(url2, "w", encoding="utf-8")
            g.write(salida)
            g.close()

            # Screenshot
            # Opciones del browser
            alloptions = webdriver.ChromeOptions()
            alloptions.add_argument('headless')
            alloptions.add_argument("--window-size=1920,1080")
            # alloptions.add_argument("--window-size=640,360")

            n_cualitativo = 5
            first_row  = [0,0,0,0,0]
            second_row = [0,0,0,0,0]
            third_row  = [0,0,0,0,0]
            fourth_row = [0,0,0,0,0]
            fifth_row  = [0,0,0,0,0]

            # Operaciones con el browser
            browser = webdriver.Chrome(options=alloptions)
            # Trabajaremos con el centro del viewport porque queremos determinar cambios en contenido
            viewport_width         = browser.execute_script("return document.body.clientWidth")
            viewport_height        = browser.execute_script("return window.innerHeight")
            site_width             = browser.execute_script("return document.body.offsetWidth")
            site_height            = browser.execute_script("return document.body.parentNode.scrollHeight")
            site_n_horizontal      = site_width / n_cualitativo
            site_n_vertical        = site_height / n_cualitativo
            site_x_axis            = [0, site_n_horizontal, site_n_horizontal*2, site_n_horizontal*3, site_n_horizontal*4, site_n_horizontal*5]
            site_y_axis            = [0, site_n_vertical, site_n_vertical*2, site_n_vertical*3, site_n_vertical*4, site_n_vertical*5]
            viewport_center_width  = viewport_width / 2
            viewport_center_height = viewport_height / 2

            url_updated = 'file://'+url2
            browser.get(url_updated)
            bloques_con_cambios = browser.find_elements_by_xpath('//div[contains(@style, "border: 3px solid red")]')

            # Rellenamos la matriz con los valores correspondientes
            # Fila 1
            if site_y_axis[0] <= viewport_center_height < site_y_axis[1]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    first_row  = [2,1,0,0,0]
                    second_row = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    first_row  = [1,2,1,0,0]
                    second_row = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    first_row  = [0,1,2,1,0]
                    second_row = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    first_row  = [0,0,1,2,1]
                    second_row = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width <= site_x_axis[5]:
                    first_row  = [0,0,0,1,2]
                    second_row = [0,0,0,1,1]

            # Fila 2
            elif site_y_axis[1] <= viewport_center_height < site_y_axis[2]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    first_row  = [1,1,0,0,0]
                    second_row = [2,1,0,0,0]
                    third_row  = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    first_row  = [1,1,1,0,0]
                    second_row = [1,2,1,0,0]
                    third_row  = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    first_row  = [0,1,1,1,0]
                    second_row = [0,1,2,1,0]
                    third_row  = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    first_row  = [0,0,1,1,1]
                    second_row = [0,0,1,2,1]
                    third_row  = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width <= site_x_axis[5]:
                    first_row  = [0,0,0,1,1]
                    second_row = [0,0,0,1,2]
                    third_row  = [0,0,0,1,1]

            # Fila 3
            elif site_y_axis[2] <= viewport_center_height < site_y_axis[3]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    second_row = [1,1,0,0,0]
                    third_row  = [2,1,0,0,0]
                    fourth_row = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    second_row = [1,1,1,0,0]
                    third_row  = [1,2,1,0,0]
                    fourth_row = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    second_row = [0,1,1,1,0]
                    third_row  = [0,1,2,1,0]
                    fourth_row = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    second_row = [0,0,1,1,1]
                    third_row  = [0,0,1,2,1]
                    fourth_row = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    second_row = [0,0,0,1,1]
                    third_row  = [0,0,0,1,2]
                    fourth_row = [0,0,0,1,1]

            # Fila 4
            elif site_y_axis[3] <= viewport_center_height < site_y_axis[4]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    third_row  = [1,1,0,0,0]
                    fourth_row = [2,1,0,0,0]
                    fifth_row  = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    third_row  = [1,1,1,0,0]
                    fourth_row = [1,2,1,0,0]
                    fifth_row  = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    third_row  = [0,1,1,1,0]
                    fourth_row = [0,1,2,1,0]
                    fifth_row  = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    third_row  = [0,0,1,1,1]
                    fourth_row = [0,0,1,2,1]
                    fifth_row  = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    third_row  = [0,0,0,1,1]
                    fourth_row = [0,0,0,1,2]
                    fifth_row  = [0,0,0,1,1]

            # Fila 5
            elif site_y_axis[4] <= viewport_center_height <= site_y_axis[5]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    fourth_row = [1,1,0,0,0]
                    fifth_row  = [2,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    fourth_row = [1,1,1,0,0]
                    fifth_row  = [1,2,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    fourth_row = [0,1,1,1,0]
                    fifth_row  = [0,1,2,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    fourth_row = [0,0,1,1,1]
                    fifth_row  = [0,0,1,2,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    fourth_row = [0,0,0,1,1]
                    fifth_row  = [0,0,0,1,2]

            block_change_matrix = [first_row,second_row,third_row,fourth_row,fifth_row]

            # Calculamos importancia cualitativa
            qualitative_i = []
            for i in range(0, len(bloques_con_cambios)):
                cambio_cualitativo = 0
                x1_value  = bloques_con_cambios[i].location.get('x')
                x2_value  = bloques_con_cambios[i].size.get('width') + x1_value

                if site_x_axis[0] <= x1_value < site_x_axis[1]: indice_x1 = 0
                elif site_x_axis[1] <= x1_value < site_x_axis[2]: indice_x1 = 1
                elif site_x_axis[2] <= x1_value < site_x_axis[3]: indice_x1 = 2
                elif site_x_axis[3] <= x1_value < site_x_axis[4]: indice_x1 = 3
                elif site_x_axis[4] <= x1_value < site_x_axis[5]: indice_x1 = 4

                if site_x_axis[0] <= x2_value < site_x_axis[1]: indice_x2 = 0
                elif site_x_axis[1] <= x2_value < site_x_axis[2]: indice_x2 = 1
                elif site_x_axis[2] <= x2_value < site_x_axis[3]: indice_x2 = 2
                elif site_x_axis[3] <= x2_value < site_x_axis[4]: indice_x2 = 3
                elif (site_x_axis[4] <= x2_value < site_x_axis[5]) or (x2_value >= site_x_axis[5]): indice_x2 = 4

                y1_value = bloques_con_cambios[i].location.get('y')
                y2_value = bloques_con_cambios[i].size.get('height') + y1_value

                if site_y_axis[0] <= y1_value < site_y_axis[1]: indice_y1 = 0
                elif site_y_axis[1] <= y1_value < site_y_axis[2]: indice_y1 = 1
                elif site_y_axis[2] <= y1_value < site_y_axis[3]: indice_y1 = 2
                elif site_y_axis[3] <= y1_value < site_y_axis[4]: indice_y1 = 3
                elif site_y_axis[4] <= y1_value < site_y_axis[5]: indice_y1 = 4

                if site_y_axis[0] <= y2_value < site_y_axis[1]: indice_y2 = 0
                elif site_y_axis[1] <= y2_value < site_y_axis[2]: indice_y2 = 1
                elif site_y_axis[2] <= y2_value < site_y_axis[3]: indice_y2 = 2
                elif site_y_axis[3] <= y2_value < site_y_axis[4]: indice_y2 = 3
                elif (site_y_axis[4] <= y2_value < site_y_axis[5]) or (y2_value >= site_y_axis[5]): indice_y2 = 4

                for i in range(indice_x1, indice_x2):
                    for j in range(indice_y1, indice_y2):
                        cambio_cualitativo = cambio_cualitativo + block_change_matrix[i][j]

                qualitative_i.append(cambio_cualitativo * 10)

            screenshot = util.fullpage_screenshot(browser, 'static/new_screenshot.png')
            browser.quit()
            # Fin Screenshot
            # Creacion Grafico de barras
            obj                    = list(range(len(difference)))
            objects                = [x + 1 for x in obj]
            qualitative_difference = [0] * len(difference)
            contador               = 0

            for i in range(len(difference)):
                if difference[i] != 0:
                    qualitative_difference[i] = qualitative_i[contador]
                    contador +=1

            # Revisar valores de importancia para la gráfica
            quantitative_importance = [x * 0.4 for x in difference]
            qualitative_importance  = [x * 0.6 for x in qualitative_difference]
            weighted_importance = [x + y for x, y in zip(quantitative_importance, qualitative_importance)]
            print(quantitative_importance)
            print(qualitative_importance)
            print(weighted_importance)
            y_pos       = np.arange(len(objects))
            performance =  weighted_importance
            plt.tick_params(axis='x', which='major', labelsize=5)
            plt.figure(figsize=(10,3.8))
            barlist = plt.bar(y_pos,performance,align='center',alpha=0.5)

            for i in range(0, len(barlist)):
                height = barlist[i].get_height()
                if height >= 50:
                    barlist[i].set_color('r')
                elif height >= 20 and height < 50:
                    barlist[i].set_color('y')
                elif height > 0 and height < 20:
                    barlist[i].set_color('g')

            c_significativo    = mpatches.Patch(color='r', label = 'Significativo')
            c_intermedio       = mpatches.Patch(color='y', label = 'Intermedio')
            c_no_significativo = mpatches.Patch(color='g', label = 'No significativo')
            plt.legend(handles=[c_significativo, c_intermedio, c_no_significativo], title='Tipo de Cambio', fontsize='small', fancybox=True)
            plt.xticks(y_pos, objects)
            plt.ylabel('% de cambios')
            plt.xlabel('ID de bloques')
            plt.title('Cambios por bloque de texto')
            plt.savefig('static/block_text_change_percentage.png')
            # Fin Grafico

        # else:
            # Otro caso

    elif len(texts) > len(p_texts):
        for iterator in range(0, len(texts) - len(p_texts)):
            p_texts.append("")

        if caso == 'diferencia'.upper():
            for iterator in range(0, len(texts)):
                if texts[iterator] is None:
                    texts[iterator] = ""
                if p_texts[iterator] is None:
                    p_texts[iterator] = ""

                result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
                difference.append(round((1 - result) * 100, 2))

            texts.sort(key=len, reverse=True)
            p_texts.sort(key=len, reverse=True)

            for iterator in range(0, len(texts)):
                result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
                sorted_difference.append(round((1 - result) * 100, 2))

            for index, element in enumerate(difference):
                if element != 0:
                    savecsv.append(1)
                    indices_cambios.append(index)
                else:
                    savecsv.append(0)

            # 20% de los bloques tienen 80% del peso
            twenty_percent_elements.append(sorted_difference[0:math.floor(len(difference) * 0.2)])  # Elementos con 80% del valor
            eighty_percent_elements.append(sorted_difference[math.floor(len(difference) * 0.2):])   # Elementos con 20% del valor

            for sublist in twenty_percent_elements:
                for item in sublist:
                    flatten20.append(item)

            for sublist in eighty_percent_elements:
                for item in sublist:
                    flatten80.append(item)

            # Asignacion del peso cuantitativo
            porcentajes_cambios_ordenados.append(flatten20)
            porcentajes_cambios_ordenados.append(flatten80)
            cambio_peso_80 = statistics.mean(porcentajes_cambios_ordenados[0]) * 0.8
            cambio_peso_20 = statistics.mean(porcentajes_cambios_ordenados[1]) * 0.2
            cambio_total   = cambio_peso_80 + cambio_peso_20

            # Aqui se hacen las manipulaciones al codigo para agregar el marco rojo que detalla el div cambiado
            # Si hubo cambios resaltar usando el id que yo le otorgué para la búsqueda
            reemplazo   = '<head>' + '\n' + '<script src="https://code.jquery.com/jquery-3.4.1.js"' \
                                            'integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU="' \
                                            'crossorigin="anonymous"></script>'
            salidafinal = sorted(unsorted_dicttexts, key=lambda k: k['id'])

            salida = salida + "<!DOCTYPE html>" + '\n' + "<html>" + '\n'
            head   = str(head).replace('<head>', reemplazo)
            salida = salida + head + '\n' + '<body>' + '\n'


            for element in indices_cambios:
                for element2 in salidafinal:
                    if element2['id'] == element:
                        if 'style' in element2['value']:
                            element2['value'] = element2['value'].replace('style="', 'style="border: 3px solid red; ', 1)
                        else:
                            reemplazo_border  = '< ' + ' style="border: 3px solid red;"'
                            element2['value'] = element2['value'].replace('<', reemplazo_border, 1)

            for element in salidafinal:
                if element['value'] != 'None':
                    salida = salida + element['value'] + '\n'

            salida = salida + "</body>" + '\n'
            salida = salida + "</html>"

            url2 = url.replace('.html', '_updated.html')
            g = open(url2, "w", encoding="utf-8")
            g.write(salida)
            g.close()

            # Screenshot
            # Opciones del browser
            alloptions = webdriver.ChromeOptions()
            alloptions.add_argument('headless')
            alloptions.add_argument("--window-size=1920,1080")
            # alloptions.add_argument("--window-size=640,360")

            n_cualitativo = 5
            first_row  = [0,0,0,0,0]
            second_row = [0,0,0,0,0]
            third_row  = [0,0,0,0,0]
            fourth_row = [0,0,0,0,0]
            fifth_row  = [0,0,0,0,0]

            # Operaciones con el browser
            browser = webdriver.Chrome(options=alloptions)
            # Trabajaremos con el centro del viewport porque queremos determinar cambios en contenido
            viewport_width         = browser.execute_script("return document.body.clientWidth")
            viewport_height        = browser.execute_script("return window.innerHeight")
            site_width             = browser.execute_script("return document.body.offsetWidth")
            site_height            = browser.execute_script("return document.body.parentNode.scrollHeight")
            site_n_horizontal      = site_width / n_cualitativo
            site_n_vertical        = site_height / n_cualitativo
            site_x_axis            = [0, site_n_horizontal, site_n_horizontal*2, site_n_horizontal*3, site_n_horizontal*4, site_n_horizontal*5]
            site_y_axis            = [0, site_n_vertical, site_n_vertical*2, site_n_vertical*3, site_n_vertical*4, site_n_vertical*5]
            viewport_center_width  = viewport_width / 2
            viewport_center_height = viewport_height / 2

            url_updated = 'file://'+url2
            browser.get(url_updated)
            bloques_con_cambios = browser.find_elements_by_xpath('//div[contains(@style, "border: 3px solid red")]')

            # Rellenamos la matriz con los valores correspondientes
            # Fila 1
            if site_y_axis[0] <= viewport_center_height < site_y_axis[1]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    first_row  = [2,1,0,0,0]
                    second_row = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    first_row  = [1,2,1,0,0]
                    second_row = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    first_row  = [0,1,2,1,0]
                    second_row = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    first_row  = [0,0,1,2,1]
                    second_row = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width <= site_x_axis[5]:
                    first_row  = [0,0,0,1,2]
                    second_row = [0,0,0,1,1]

            # Fila 2
            elif site_y_axis[1] <= viewport_center_height < site_y_axis[2]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    first_row  = [1,1,0,0,0]
                    second_row = [2,1,0,0,0]
                    third_row  = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    first_row  = [1,1,1,0,0]
                    second_row = [1,2,1,0,0]
                    third_row  = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    first_row  = [0,1,1,1,0]
                    second_row = [0,1,2,1,0]
                    third_row  = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    first_row  = [0,0,1,1,1]
                    second_row = [0,0,1,2,1]
                    third_row  = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width <= site_x_axis[5]:
                    first_row  = [0,0,0,1,1]
                    second_row = [0,0,0,1,2]
                    third_row  = [0,0,0,1,1]

            # Fila 3
            elif site_y_axis[2] <= viewport_center_height < site_y_axis[3]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    second_row = [1,1,0,0,0]
                    third_row  = [2,1,0,0,0]
                    fourth_row = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    second_row = [1,1,1,0,0]
                    third_row  = [1,2,1,0,0]
                    fourth_row = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    second_row = [0,1,1,1,0]
                    third_row  = [0,1,2,1,0]
                    fourth_row = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    second_row = [0,0,1,1,1]
                    third_row  = [0,0,1,2,1]
                    fourth_row = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    second_row = [0,0,0,1,1]
                    third_row  = [0,0,0,1,2]
                    fourth_row = [0,0,0,1,1]

            # Fila 4
            elif site_y_axis[3] <= viewport_center_height < site_y_axis[4]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    third_row  = [1,1,0,0,0]
                    fourth_row = [2,1,0,0,0]
                    fifth_row  = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    third_row  = [1,1,1,0,0]
                    fourth_row = [1,2,1,0,0]
                    fifth_row  = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    third_row  = [0,1,1,1,0]
                    fourth_row = [0,1,2,1,0]
                    fifth_row  = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    third_row  = [0,0,1,1,1]
                    fourth_row = [0,0,1,2,1]
                    fifth_row  = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    third_row  = [0,0,0,1,1]
                    fourth_row = [0,0,0,1,2]
                    fifth_row  = [0,0,0,1,1]

            # Fila 5
            elif site_y_axis[4] <= viewport_center_height <= site_y_axis[5]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    fourth_row = [1,1,0,0,0]
                    fifth_row  = [2,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    fourth_row = [1,1,1,0,0]
                    fifth_row  = [1,2,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    fourth_row = [0,1,1,1,0]
                    fifth_row  = [0,1,2,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    fourth_row = [0,0,1,1,1]
                    fifth_row  = [0,0,1,2,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    fourth_row = [0,0,0,1,1]
                    fifth_row  = [0,0,0,1,2]

            block_change_matrix = [first_row,second_row,third_row,fourth_row,fifth_row]

            # Calculamos importancia cualitativa
            qualitative_i = []
            for i in range(0, len(bloques_con_cambios)):
                cambio_cualitativo = 0
                x1_value  = bloques_con_cambios[i].location.get('x')
                x2_value  = bloques_con_cambios[i].size.get('width') + x1_value

                if site_x_axis[0] <= x1_value < site_x_axis[1]: indice_x1 = 0
                elif site_x_axis[1] <= x1_value < site_x_axis[2]: indice_x1 = 1
                elif site_x_axis[2] <= x1_value < site_x_axis[3]: indice_x1 = 2
                elif site_x_axis[3] <= x1_value < site_x_axis[4]: indice_x1 = 3
                elif site_x_axis[4] <= x1_value < site_x_axis[5]: indice_x1 = 4

                if site_x_axis[0] <= x2_value < site_x_axis[1]: indice_x2 = 0
                elif site_x_axis[1] <= x2_value < site_x_axis[2]: indice_x2 = 1
                elif site_x_axis[2] <= x2_value < site_x_axis[3]: indice_x2 = 2
                elif site_x_axis[3] <= x2_value < site_x_axis[4]: indice_x2 = 3
                elif (site_x_axis[4] <= x2_value < site_x_axis[5]) or (x2_value >= site_x_axis[5]): indice_x2 = 4

                y1_value = bloques_con_cambios[i].location.get('y')
                y2_value = bloques_con_cambios[i].size.get('height') + y1_value

                if site_y_axis[0] <= y1_value < site_y_axis[1]: indice_y1 = 0
                elif site_y_axis[1] <= y1_value < site_y_axis[2]: indice_y1 = 1
                elif site_y_axis[2] <= y1_value < site_y_axis[3]: indice_y1 = 2
                elif site_y_axis[3] <= y1_value < site_y_axis[4]: indice_y1 = 3
                elif site_y_axis[4] <= y1_value < site_y_axis[5]: indice_y1 = 4

                if site_y_axis[0] <= y2_value < site_y_axis[1]: indice_y2 = 0
                elif site_y_axis[1] <= y2_value < site_y_axis[2]: indice_y2 = 1
                elif site_y_axis[2] <= y2_value < site_y_axis[3]: indice_y2 = 2
                elif site_y_axis[3] <= y2_value < site_y_axis[4]: indice_y2 = 3
                elif (site_y_axis[4] <= y2_value < site_y_axis[5]) or (y2_value >= site_y_axis[5]): indice_y2 = 4

                for i in range(indice_x1, indice_x2):
                    for j in range(indice_y1, indice_y2):
                        cambio_cualitativo = cambio_cualitativo + block_change_matrix[i][j]

                qualitative_i.append(cambio_cualitativo * 10)

            screenshot = util.fullpage_screenshot(browser, 'static/new_screenshot.png')
            browser.quit()
            # Fin Screenshot
            # Creacion Grafico de barras
            obj                    = list(range(len(difference)))
            objects                = [x + 1 for x in obj]
            qualitative_difference = [0] * len(difference)
            contador               = 0

            for i in range(len(difference)):
                if difference[i] != 0:
                    qualitative_difference[i] = qualitative_i[contador]
                    contador +=1

            # Revisar valores de importancia para la gráfica
            quantitative_importance = [x * 0.4 for x in difference]
            qualitative_importance  = [x * 0.6 for x in qualitative_difference]
            weighted_importance = [x + y for x, y in zip(quantitative_importance, qualitative_importance)]
            print(quantitative_importance)
            print(qualitative_importance)
            print(weighted_importance)
            y_pos       = np.arange(len(objects))
            performance =  weighted_importance
            plt.tick_params(axis='x', which='major', labelsize=5)
            plt.figure(figsize=(10,3.8))
            barlist = plt.bar(y_pos,performance,align='center',alpha=0.5)

            for i in range(0, len(barlist)):
                height = barlist[i].get_height()
                if height >= 50:
                    barlist[i].set_color('r')
                elif height >= 20 and height < 50:
                    barlist[i].set_color('y')
                elif height > 0 and height < 20:
                    barlist[i].set_color('g')

            c_significativo    = mpatches.Patch(color='r', label = 'Significativo')
            c_intermedio       = mpatches.Patch(color='y', label = 'Intermedio')
            c_no_significativo = mpatches.Patch(color='g', label = 'No significativo')
            plt.legend(handles=[c_significativo, c_intermedio, c_no_significativo], title='Tipo de Cambio', fontsize='small', fancybox=True)
            plt.xticks(y_pos, objects)
            plt.ylabel('% de cambios')
            plt.xlabel('ID de bloques')
            plt.title('Cambios por bloque de texto')
            plt.savefig('static/block_text_change_percentage.png')
            # Fin Grafico

        # else:
            # Otro caso

    else:
        for iterator in range(0, len(p_texts) - len(texts)):
            texts.append("")

        if caso == 'diferencia'.upper():
            for iterator in range(0, len(texts)):
                if texts[iterator] is None:
                    texts[iterator] = ""
                if p_texts[iterator] is None:
                    p_texts[iterator] = ""

                result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
                difference.append(round((1 - result) * 100, 2))

            texts.sort(key=len, reverse=True)
            p_texts.sort(key=len, reverse=True)

            for iterator in range(0, len(texts)):
                result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
                sorted_difference.append(round((1 - result) * 100, 2))

            for index, element in enumerate(difference):
                if element != 0:
                    savecsv.append(1)
                    indices_cambios.append(index)
                else:
                    savecsv.append(0)

            # 20% de los bloques tienen 80% del peso
            twenty_percent_elements.append(sorted_difference[0:math.floor(len(difference) * 0.2)])  # Elementos con 80% del valor
            eighty_percent_elements.append(sorted_difference[math.floor(len(difference) * 0.2):])   # Elementos con 20% del valor

            for sublist in twenty_percent_elements:
                for item in sublist:
                    flatten20.append(item)

            for sublist in eighty_percent_elements:
                for item in sublist:
                    flatten80.append(item)

            # Asignacion del peso cuantitativo
            porcentajes_cambios_ordenados.append(flatten20)
            porcentajes_cambios_ordenados.append(flatten80)
            cambio_peso_80 = statistics.mean(porcentajes_cambios_ordenados[0]) * 0.8
            cambio_peso_20 = statistics.mean(porcentajes_cambios_ordenados[1]) * 0.2
            cambio_total   = cambio_peso_80 + cambio_peso_20

            # Aqui se hacen las manipulaciones al codigo para agregar el marco rojo que detalla el div cambiado
            # Si hubo cambios resaltar usando el id que yo le otorgué para la búsqueda
            reemplazo   = '<head>' + '\n' + '<script src="https://code.jquery.com/jquery-3.4.1.js"' \
                                            'integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU="' \
                                            'crossorigin="anonymous"></script>'
            salidafinal = sorted(unsorted_dicttexts, key=lambda k: k['id'])

            salida = salida + "<!DOCTYPE html>" + '\n' + "<html>" + '\n'
            head   = str(head).replace('<head>', reemplazo)
            salida = salida + head + '\n' + '<body>' + '\n'


            for element in indices_cambios:
                for element2 in salidafinal:
                    if element2['id'] == element:
                        if 'style' in element2['value']:
                            element2['value'] = element2['value'].replace('style="', 'style="border: 3px solid red; ', 1)
                        else:
                            reemplazo_border  = '< ' + ' style="border: 3px solid red;"'
                            element2['value'] = element2['value'].replace('<', reemplazo_border, 1)

            for element in salidafinal:
                if element['value'] != 'None':
                    salida = salida + element['value'] + '\n'

            salida = salida + "</body>" + '\n'
            salida = salida + "</html>"

            url2 = url.replace('.html', '_updated.html')
            g = open(url2, "w", encoding="utf-8")
            g.write(salida)
            g.close()

            # Screenshot
            # Opciones del browser
            alloptions = webdriver.ChromeOptions()
            alloptions.add_argument('headless')
            alloptions.add_argument("--window-size=1920,1080")
            # alloptions.add_argument("--window-size=640,360")

            n_cualitativo = 5
            first_row  = [0,0,0,0,0]
            second_row = [0,0,0,0,0]
            third_row  = [0,0,0,0,0]
            fourth_row = [0,0,0,0,0]
            fifth_row  = [0,0,0,0,0]

            # Operaciones con el browser
            browser = webdriver.Chrome(options=alloptions)
            # Trabajaremos con el centro del viewport porque queremos determinar cambios en contenido
            viewport_width         = browser.execute_script("return document.body.clientWidth")
            viewport_height        = browser.execute_script("return window.innerHeight")
            site_width             = browser.execute_script("return document.body.offsetWidth")
            site_height            = browser.execute_script("return document.body.parentNode.scrollHeight")
            site_n_horizontal      = site_width / n_cualitativo
            site_n_vertical        = site_height / n_cualitativo
            site_x_axis            = [0, site_n_horizontal, site_n_horizontal*2, site_n_horizontal*3, site_n_horizontal*4, site_n_horizontal*5]
            site_y_axis            = [0, site_n_vertical, site_n_vertical*2, site_n_vertical*3, site_n_vertical*4, site_n_vertical*5]
            viewport_center_width  = viewport_width / 2
            viewport_center_height = viewport_height / 2

            url_updated = 'file://'+url2
            browser.get(url_updated)
            bloques_con_cambios = browser.find_elements_by_xpath('//div[contains(@style, "border: 3px solid red")]')

            # Rellenamos la matriz con los valores correspondientes
            # Fila 1
            if site_y_axis[0] <= viewport_center_height < site_y_axis[1]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    first_row  = [2,1,0,0,0]
                    second_row = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    first_row  = [1,2,1,0,0]
                    second_row = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    first_row  = [0,1,2,1,0]
                    second_row = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    first_row  = [0,0,1,2,1]
                    second_row = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width <= site_x_axis[5]:
                    first_row  = [0,0,0,1,2]
                    second_row = [0,0,0,1,1]

            # Fila 2
            elif site_y_axis[1] <= viewport_center_height < site_y_axis[2]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    first_row  = [1,1,0,0,0]
                    second_row = [2,1,0,0,0]
                    third_row  = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    first_row  = [1,1,1,0,0]
                    second_row = [1,2,1,0,0]
                    third_row  = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    first_row  = [0,1,1,1,0]
                    second_row = [0,1,2,1,0]
                    third_row  = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    first_row  = [0,0,1,1,1]
                    second_row = [0,0,1,2,1]
                    third_row  = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width <= site_x_axis[5]:
                    first_row  = [0,0,0,1,1]
                    second_row = [0,0,0,1,2]
                    third_row  = [0,0,0,1,1]

            # Fila 3
            elif site_y_axis[2] <= viewport_center_height < site_y_axis[3]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    second_row = [1,1,0,0,0]
                    third_row  = [2,1,0,0,0]
                    fourth_row = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    second_row = [1,1,1,0,0]
                    third_row  = [1,2,1,0,0]
                    fourth_row = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    second_row = [0,1,1,1,0]
                    third_row  = [0,1,2,1,0]
                    fourth_row = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    second_row = [0,0,1,1,1]
                    third_row  = [0,0,1,2,1]
                    fourth_row = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    second_row = [0,0,0,1,1]
                    third_row  = [0,0,0,1,2]
                    fourth_row = [0,0,0,1,1]

            # Fila 4
            elif site_y_axis[3] <= viewport_center_height < site_y_axis[4]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    third_row  = [1,1,0,0,0]
                    fourth_row = [2,1,0,0,0]
                    fifth_row  = [1,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    third_row  = [1,1,1,0,0]
                    fourth_row = [1,2,1,0,0]
                    fifth_row  = [1,1,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    third_row  = [0,1,1,1,0]
                    fourth_row = [0,1,2,1,0]
                    fifth_row  = [0,1,1,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    third_row  = [0,0,1,1,1]
                    fourth_row = [0,0,1,2,1]
                    fifth_row  = [0,0,1,1,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    third_row  = [0,0,0,1,1]
                    fourth_row = [0,0,0,1,2]
                    fifth_row  = [0,0,0,1,1]

            # Fila 5
            elif site_y_axis[4] <= viewport_center_height <= site_y_axis[5]:
                if site_x_axis[0] <= viewport_center_width < site_x_axis[1]:
                    fourth_row = [1,1,0,0,0]
                    fifth_row  = [2,1,0,0,0]
                elif site_x_axis[1] <= viewport_center_width < site_x_axis[2]:
                    fourth_row = [1,1,1,0,0]
                    fifth_row  = [1,2,1,0,0]
                elif site_x_axis[2] <= viewport_center_width < site_x_axis[3]:
                    fourth_row = [0,1,1,1,0]
                    fifth_row  = [0,1,2,1,0]
                elif site_x_axis[3] <= viewport_center_width < site_x_axis[4]:
                    fourth_row = [0,0,1,1,1]
                    fifth_row  = [0,0,1,2,1]
                elif site_x_axis[4] <= viewport_center_width < site_x_axis[5]:
                    fourth_row = [0,0,0,1,1]
                    fifth_row  = [0,0,0,1,2]

            block_change_matrix = [first_row,second_row,third_row,fourth_row,fifth_row]

            # Calculamos importancia cualitativa
            qualitative_i = []
            for i in range(0, len(bloques_con_cambios)):
                cambio_cualitativo = 0
                x1_value  = bloques_con_cambios[i].location.get('x')
                x2_value  = bloques_con_cambios[i].size.get('width') + x1_value

                if site_x_axis[0] <= x1_value < site_x_axis[1]: indice_x1 = 0
                elif site_x_axis[1] <= x1_value < site_x_axis[2]: indice_x1 = 1
                elif site_x_axis[2] <= x1_value < site_x_axis[3]: indice_x1 = 2
                elif site_x_axis[3] <= x1_value < site_x_axis[4]: indice_x1 = 3
                elif site_x_axis[4] <= x1_value < site_x_axis[5]: indice_x1 = 4

                if site_x_axis[0] <= x2_value < site_x_axis[1]: indice_x2 = 0
                elif site_x_axis[1] <= x2_value < site_x_axis[2]: indice_x2 = 1
                elif site_x_axis[2] <= x2_value < site_x_axis[3]: indice_x2 = 2
                elif site_x_axis[3] <= x2_value < site_x_axis[4]: indice_x2 = 3
                elif (site_x_axis[4] <= x2_value < site_x_axis[5]) or (x2_value >= site_x_axis[5]): indice_x2 = 4

                y1_value = bloques_con_cambios[i].location.get('y')
                y2_value = bloques_con_cambios[i].size.get('height') + y1_value

                if site_y_axis[0] <= y1_value < site_y_axis[1]: indice_y1 = 0
                elif site_y_axis[1] <= y1_value < site_y_axis[2]: indice_y1 = 1
                elif site_y_axis[2] <= y1_value < site_y_axis[3]: indice_y1 = 2
                elif site_y_axis[3] <= y1_value < site_y_axis[4]: indice_y1 = 3
                elif site_y_axis[4] <= y1_value < site_y_axis[5]: indice_y1 = 4

                if site_y_axis[0] <= y2_value < site_y_axis[1]: indice_y2 = 0
                elif site_y_axis[1] <= y2_value < site_y_axis[2]: indice_y2 = 1
                elif site_y_axis[2] <= y2_value < site_y_axis[3]: indice_y2 = 2
                elif site_y_axis[3] <= y2_value < site_y_axis[4]: indice_y2 = 3
                elif (site_y_axis[4] <= y2_value < site_y_axis[5]) or (y2_value >= site_y_axis[5]): indice_y2 = 4

                for i in range(indice_x1, indice_x2):
                    for j in range(indice_y1, indice_y2):
                        cambio_cualitativo = cambio_cualitativo + block_change_matrix[i][j]

                qualitative_i.append(cambio_cualitativo * 10)

            screenshot = util.fullpage_screenshot(browser, 'static/new_screenshot.png')
            browser.quit()
            # Fin Screenshot
            # Creacion Grafico de barras
            obj                    = list(range(len(difference)))
            objects                = [x + 1 for x in obj]
            qualitative_difference = [0] * len(difference)
            contador               = 0

            for i in range(len(difference)):
                if difference[i] != 0:
                    qualitative_difference[i] = qualitative_i[contador]
                    contador +=1

            # Revisar valores de importancia para la gráfica
            quantitative_importance = [x * 0.4 for x in difference]
            qualitative_importance  = [x * 0.6 for x in qualitative_difference]
            weighted_importance = [x + y for x, y in zip(quantitative_importance, qualitative_importance)]
            print(quantitative_importance)
            print(qualitative_importance)
            print(weighted_importance)
            y_pos       = np.arange(len(objects))
            performance =  weighted_importance
            plt.tick_params(axis='x', which='major', labelsize=5)
            plt.figure(figsize=(10,3.8))
            barlist = plt.bar(y_pos,performance,align='center',alpha=0.5)

            for i in range(0, len(barlist)):
                height = barlist[i].get_height()
                if height >= 50:
                    barlist[i].set_color('r')
                elif height >= 20 and height < 50:
                    barlist[i].set_color('y')
                elif height > 0 and height < 20:
                    barlist[i].set_color('g')

            c_significativo    = mpatches.Patch(color='r', label = 'Significativo')
            c_intermedio       = mpatches.Patch(color='y', label = 'Intermedio')
            c_no_significativo = mpatches.Patch(color='g', label = 'No significativo')
            plt.legend(handles=[c_significativo, c_intermedio, c_no_significativo], title='Tipo de Cambio', fontsize='small', fancybox=True)
            plt.xticks(y_pos, objects)
            plt.ylabel('% de cambios')
            plt.xlabel('ID de bloques')
            plt.title('Cambios por bloque de texto')
            plt.savefig('static/block_text_change_percentage.png')
            # Fin Grafico

        # else:
            # Otro caso

    # bom.ciens.ucv.ve/dataset
