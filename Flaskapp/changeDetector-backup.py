# -*- coding: utf-8 -*-

import difflib
import math
import statistics
# import os                           # Se usa en la toma del screenshot
# import util                         # Se usa en la toma del screenshot
from selenium import webdriver
from bs4 import BeautifulSoup


def change_detector():
    # Opciones del browser
    alloptions = webdriver.ChromeOptions()
    alloptions.add_argument('headless')

    # Operaciones con el browser
    browser = webdriver.Chrome(options=alloptions)
    url = "https://www.w3schools.com/"
    # url = 'http://bom.ciens.ucv.ve/dataset/data/20140924152321/'
    browser.get(url)
    # print(browser.current_url)
    html = browser.page_source
    browser.quit()

    browser = webdriver.Chrome(options=alloptions)
    p_url = "https://www.w3schools.com/"
    # p_url = 'http://bom.ciens.ucv.ve/dataset/data/20140924152321/'
    browser.get(p_url)
    p_html = browser.page_source
    browser.quit()

    # Guardar screenshot de la pagina web visitada
    # DRIVER = 'chromedriver'
    # driver = webdriver.Chrome(DRIVER)
    # driver.get('http://bom.ciens.ucv.ve/dataset/data/20140924152321/')
    # screenshot = driver.save_screenshot('my_screenshot.png')
    # driver.quit()

    difference = []
    sorted_difference = []
    twenty_percent_elements = []
    eighty_percent_elements = []
    flatten20 = []
    flatten80 = []
    savecsv = []
    indices_cambios = []

    unsorted_dicttexts = []
    p_unsorted_dicttexts = []
    texts = []
    p_texts = []

    text = BeautifulSoup(html, "lxml")
    # alldivs = text.find_all("div")
    divs = text.find("div")
    head = text.find("head")
    p_text = BeautifulSoup(p_html, "lxml")
    # p_alldivs = p_text.find_all("div")
    p_divs = p_text.find("div")
    # p_head = text.find("head")
    caso = 'diferencia'.upper()
    salida = ""
    # borde = ""

    counter = 0
    for item in divs.next_siblings:
        try:
            # texts.append(str(item.next))
            unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1
        except AttributeError:
            # texts.append(str(item))
            unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1

    # for element in texts:
    #     i += 1
    #     print("Elemento ", i, " :\n", type(element))

    counter = 0
    for item in p_divs.next_siblings:
        try:
            # p_texts.append(str(item.next))
            p_unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1
        except AttributeError:
            # p_texts.append(str(item))
            p_unsorted_dicttexts.append({'id': counter, 'value': str(item.next)})
            counter += 1

    # for element in p_texts:
    #     i += 1
    #     print("p_Elemento ", i, " :\n", type(element))
    #

    # dicttexts = sorted(unsorted_dicttexts, key=lambda k: len(k['value']), reverse=True)
    # p_dicttexts = sorted(p_unsorted_dicttexts, key=lambda k: len(k['value']), reverse=True)

    for i in unsorted_dicttexts:
        texts.append(i['value'])

    for i in p_unsorted_dicttexts:
        p_texts.append(i['value'])

    if len(texts) == len(p_texts):

        # Incluir función que verifica que los bloques están alineados correctamente
        # texts.sort(key=len, reverse=True)
        # p_texts.sort(key=len, reverse=True)
        # dicttexts = sorted(dicttexts, key=lambda k: k['value'], reverse=True)
        # p_dicttexts = sorted(p_dicttexts, key=lambda k: k['value'], reverse=True)
        if caso == 'diferencia'.upper():
            for iterator in range(0, len(texts)):
                # if texts[iterator] is not None and p_texts[iterator] is not None:
                if texts[iterator] is None:
                    texts[iterator] = ""
                if p_texts[iterator] is None:
                    p_texts[iterator] = ""
                # print("Tipo texts[", iterator, "] es: ", type(texts[iterator]))
                # print("Tipo p_texts[", iterator, "] es: ", type(p_texts[iterator]))
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

            # Agregar id a los divs para poder enlazarlos con el arreglo de flatten20 y flatten80 (DONE)
            # Usando selenium destacar esos divs
            # Agregar condicional a donde se calcula el % de diferencia (DONE)
            # Guardar el arreglo difference completo en un csv de ceros y unos en un url y hacer append
            # de cada una de las pruebas (DONE)

            # 20% de los bloques tienen 80% del peso
            twenty_percent_elements.append(sorted_difference[0:math.floor(len(difference) * 0.2)])  # Elementos con 80%
            #                                                                                         del valor
            eighty_percent_elements.append(sorted_difference[math.floor(len(difference) * 0.2):])   # Elementos con 20%
            #                                                                                         del valor

            for sublist in twenty_percent_elements:
                for item in sublist:
                    flatten20.append(item)

            for sublist in eighty_percent_elements:
                for item in sublist:
                    flatten80.append(item)

            # Asignacion del peso
            # twenty_percent_elements_value = round((statistics.mean(flatten20)) * 0.8, 2)    # 80% promedio valores
            # eighty_percent_elements_value = round((statistics.mean(flatten80)) * 0.2, 2)    # 20% promedio valores

            # for i in dicttexts:
            #     print(i['id'], end=" ")
            #
            # with open(r'Salida.txt', 'a') as salida:                                      # Funciona, solo texto
            #     arguments = [url, savecsv]
            #     salida.writelines(", ".join(map(str, arguments)) + '\n')
            #
            # print("\n")
            # print(twenty_percent_elements_value, eighty_percent_elements_value)

            # Aqui se hacen las manipulaciones al codigo para agregar el marco rojo que detalla el div cambiado
            # Si hubo cambios resaltar usando el id que yo le otorgué para la búsqueda
            # Se agrega jQuery al código por si hace falta, para poder insertar los recuadros
            reemplazo = '<head>' + '\n' + '<script src="https://code.jquery.com/jquery-3.4.1.js"' \
                                          'integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU="' \
                                          'crossorigin="anonymous"></script>'
            salidafinal = sorted(unsorted_dicttexts, key=lambda k: k['id'])
            salida = salida + "<!DOCTYPE html>" + '\n' + "<html>" + '\n'
            head = str(head).replace('<head>', reemplazo)
            salida = salida + head + '\n' + "<body>" + "\n"

            print(indices_cambios)
            for element in indices_cambios:
                for element2 in salidafinal:
                    if element2['id'] == element:
                        print(element2['value'].find('style'))
                        if element2['value'].find('style') != -1:
                            element2 = element2['value'].replace('style="', 'style="border: 3px solid red; ')
                            print(element2)
                            print('\n')
                        else:
                            reemplazo_border = '< ' + ' style="border: 3px solid red;"'
                            element2 = element2['value'].replace('<', reemplazo_border, 1)
                            print(element2)
                            print('\n')

            for element in salidafinal:
                if element['value'] != 'None':
                    salida = salida + element['value'] + '\n'

            salida = salida + "</body>" + '\n'
            salida = salida + "</html>"                             # Error se quita cuando se descomenta su screenshot

            # g = open("carga.html", "w", encoding="utf-8")
            # g.write(salida)
            # g.close()

            # # Screenshot
            # # Opciones del browser
            # alloptions = webdriver.ChromeOptions()
            # alloptions.add_argument('headless')
            #
            # # Operaciones con el browser
            # browser = webdriver.Chrome(options=alloptions)
            # path = os.path.abspath('carga.html')
            # url = 'file://' + path
            # browser.get(url)
            # # screenshot = browser.save_screenshot('my_screenshot.png')
            # util.fullpage_screenshot(browser, 'my_screenshot.png')
            # browser.quit()
            # # Fin Screenshot

        # else:
            # Otro caso

        # Añadir condicionales de acuerdo a las políticas a establecer

    # elif len(texts) > len(p_texts):
    #     for iterator in range(0, len(texts) - len(p_texts)):
    #         p_texts.append("")
    #
    #     # Incluir función que verifica que los bloques están alineados correctamente
    #     # texts.sort(key=len, reverse=True)
    #     # p_texts.sort(key=len, reverse=True)
    #     # dicttexts = sorted(dicttexts, key=lambda k: k['value'], reverse=True)
    #     # p_dicttexts = sorted(p_dicttexts, key=lambda k: k['value'], reverse=True)
    #     if caso == 'diferencia'.upper():
    #         for iterator in range(0, len(texts)):
    #             # if texts[iterator] is not None and p_texts[iterator] is not None:
    #             if texts[iterator] is None:
    #                 texts[iterator] = ""
    #             if p_texts[iterator] is None:
    #                 p_texts[iterator] = ""
    #             # print("Tipo texts[", iterator, "] es: ", type(texts[iterator]))
    #             # print("Tipo p_texts[", iterator, "] es: ", type(p_texts[iterator]))
    #             result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
    #             difference.append(round((1 - result) * 100, 2))
    #
    #         # Agregar id a los divs para poder enlazarlos con el arreglo de flatten20 y flatten80 (DONE)
    #         # Usando selenium destacar esos divs
    #         # Agregar condicional a donde se calcula el % de diferencia (DONE)
    #         # Guardar el arreglo difference completo en un csv de ceros y unos en un url y hacer append
    #         # de cada una de las pruebas (DONE)
    #
    #         # 20% de los bloques tienen 80% del peso
    #         twenty_percent_elements.append(difference[0:math.floor(len(difference) * 0.2)])       # Elementos con 80%
    #         #                                                                                       del valor
    #         eighty_percent_elements.append(difference[math.floor(len(difference) * 0.2):])        # Elementos con 20%
    #         #                                                                                       del valor
    #
    #         for sublist in twenty_percent_elements:
    #             for item in sublist:
    #                 flatten20.append(item)
    #
    #         for sublist in eighty_percent_elements:
    #             for item in sublist:
    #                 flatten80.append(item)
    #
    #         # Asignacion del peso
    #         twenty_percent_elements_value = round((statistics.mean(flatten20)) * 0.8, 2)    # 80% promedio valores
    #         eighty_percent_elements_value = round((statistics.mean(flatten80)) * 0.2, 2)    # 20% promedio valores
    #
    #         for element in difference:
    #             if element != 0:
    #                 savecsv.append(1)
    #             else:
    #                 savecsv.append(0)
    #
    #         for i in dicttexts:
    #             print(i['id'], end=" ")
    #
    #         # with open(r'salida.csv', 'a', newline=' ') as csvfile:
    #         #     fieldnames = ['URL', 'Cambios']
    #         #     writer = csv.writer(csvfile, fieldnames=fieldnames)
    #         #     writer.writerow({'URL': url, 'Cambios': savecsv})
    #
    #         with open(r'Salida.txt', 'a') as salida:                                      # Funciona, solo texto
    #             arguments = [url, savecsv]
    #             salida.writelines(", ".join(map(str, arguments)) + '\n')
    #     # else:
    #         # Otro caso
    #
    #     # Añadir condicionales de acuerdo a las políticas a establecer
    #
    # else:
    #     for iterator in range(0, len(p_texts) - len(texts)):
    #         texts.append("")
    #
    #     # Incluir función que verifica que los bloques están alineados correctamente
    #     # texts.sort(key=len, reverse=True)
    #     # p_texts.sort(key=len, reverse=True)
    #     # dicttexts = sorted(dicttexts, key=lambda k: k['value'], reverse=True)
    #     # p_dicttexts = sorted(p_dicttexts, key=lambda k: k['value'], reverse=True)
    #     if caso == 'diferencia'.upper():
    #         for iterator in range(0, len(texts)):
    #             # if texts[iterator] is not None and p_texts[iterator] is not None:
    #             if texts[iterator] is None:
    #                 texts[iterator] = ""
    #             if p_texts[iterator] is None:
    #                 p_texts[iterator] = ""
    #             # print("Tipo texts[", iterator, "] es: ", type(texts[iterator]))
    #             # print("Tipo p_texts[", iterator, "] es: ", type(p_texts[iterator]))
    #             result = difflib.SequenceMatcher(None, texts[iterator], p_texts[iterator]).ratio()
    #             difference.append(round((1 - result) * 100, 2))
    #
    #         # Agregar id a los divs para poder enlazarlos con el arreglo de flatten20 y flatten80 (DONE)
    #         # Usando selenium destacar esos divs
    #         # Agregar condicional a donde se calcula el % de diferencia (DONE)
    #         # Guardar el arreglo difference completo en un csv de ceros y unos en un url y hacer append
    #         # de cada una de las pruebas (DONE)
    #
    #         # 20% de los bloques tienen 80% del peso
    #         twenty_percent_elements.append(difference[0:math.floor(len(difference) * 0.2)])       # Elementos con 80%
    #         #                                                                                       del valor
    #         eighty_percent_elements.append(difference[math.floor(len(difference) * 0.2):])        # Elementos con 20%
    #         #                                                                                       del valor
    #
    #         for sublist in twenty_percent_elements:
    #             for item in sublist:
    #                 flatten20.append(item)
    #
    #         for sublist in eighty_percent_elements:
    #             for item in sublist:
    #                 flatten80.append(item)
    #
    #         # Asignacion del peso
    #         twenty_percent_elements_value = round((statistics.mean(flatten20)) * 0.8, 2)    # 80% promedio valores
    #         eighty_percent_elements_value = round((statistics.mean(flatten80)) * 0.2, 2)    # 20% promedio valores
    #
    #         for element in difference:
    #             if element != 0:
    #                 savecsv.append(1)
    #             else:
    #                 savecsv.append(0)
    #
    #         for i in dicttexts:
    #             print(i['id'], end=" ")
    #
    #         # with open(r'salida.csv', 'a', newline=' ') as csvfile:
    #         #     fieldnames = ['URL', 'Cambios']
    #         #     writer = csv.writer(csvfile, fieldnames=fieldnames)
    #         #     writer.writerow({'URL': url, 'Cambios': savecsv})
    #
    #         with open(r'Salida.txt', 'a') as salida:                                      # Funciona, solo texto
    #             arguments = [url, savecsv]
    #             salida.writelines(", ".join(map(str, arguments)) + '\n')
    #     # else:
    #         # Otro caso
    #
    #     # Añadir condicionales de acuerdo a las políticas a establecer
    #
    # # count = 0
    # # for element in difference:
    # #     print("Diferencia entre bloques ", count,  "es: ", element)
    # #     count += 1
    #
    # # with open("Salida.txt", "w") as text_file:
    # #     print(cleanhtml.encode("utf-8"), file=text_file)
    #
    # # bom.ciens.ucv.ve/dataset
