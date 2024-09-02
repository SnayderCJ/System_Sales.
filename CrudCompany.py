from Icrud import Icrud
from clsJson import JsonFile
from Utilis import BorrarPantalla, Menu, green_color, blue_color, purple_color, reset_color, linea, gotoxy
from Components import Valida
from Company import Company
import time
import os

path, file = os.path.split(__file__)

class CrudCompany(Icrud):
    json_file = JsonFile(f"{path}/data/company.json")
    def create(self):
        BorrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{'Registro de Compañía'.center(80)}{reset_color}")
        linea(80, green_color)
        name = Valida.validar_letras(f"{blue_color}Ingrese el nombre de la compañía: {purple_color}", 1, 4, 35, 4)
        ruc = str(Valida.validar_numeros(f"{blue_color}Ingrese el RUC de la compañía: {purple_color}", 1, 5, 32, 5))
        
        companies = self.json_file.read()
        
        if isinstance(companies, list) and all(isinstance(c, dict) for c in companies):
            ruc_existente = any(c['ruc'] == ruc for c in companies)
        else:
            ruc_existente = False
            companies = []

        if ruc_existente:
            linea(80, green_color)
            print(f"{purple_color}Esta compañía ya está registrada.{reset_color}")
        else:
            linea(80, green_color)
            print(f"{purple_color} Registro {reset_color}")
            linea(80, green_color)
            print(f"{blue_color}Nombre: {purple_color}{name}\n{blue_color}RUC: {purple_color}{ruc}")
            linea(80, green_color)
            company = Company(name, ruc)
            companies.append(company.getjson())
            self.json_file.save(companies)
            print(f"{purple_color}Compañía registrada exitosamente!{reset_color}")
        
        time.sleep(3)

    def update(self):
        BorrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{'Actualizar Compañía'.center(80)}{reset_color}")
        linea(80, green_color)
        ruc = str(Valida.validar_numeros(f"{blue_color}Ingrese el RUC de la compañía a actualizar: {purple_color}", 1,4, 45, 4))
        
        companies = self.json_file.read()
        company_existente = next((company for company in companies if company['ruc'] == ruc), None)

        if company_existente:
            print(f"{purple_color}Compañía encontrada: {company_existente['name']}{reset_color}")
            nuevo_nombre = input(f"{blue_color}Nuevo nombre (Enter para dejar sin cambios): {purple_color}")
        
            if nuevo_nombre:
                company_existente['name'] = nuevo_nombre

            self.json_file.save(companies)
            linea(80, green_color)
            print(f"{purple_color}Compañía actualizada exitosamente!{reset_color}")
        else:
            linea(80, green_color)
            print(f"{purple_color}Compañía no encontrada.{reset_color}")

        time.sleep(3)

    def delete(self):
        BorrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{'Eliminar Compañía'.center(80)}{reset_color}")
        linea(80, green_color)
        ruc = str(Valida.validar_numeros(f"{blue_color}Ingrese el RUC de la compañía a eliminar: {purple_color}", 1, 4, 43, 4))

        companies = self.json_file.read()
        company_existente = next((company for company in companies if company['ruc'] == ruc), None)

        if company_existente:
            print(f"{purple_color}Compañía encontrada:\n{blue_color}Nombre: {purple_color}{company_existente['name']}\n{blue_color}RUC: {purple_color}{company_existente['ruc']}{reset_color}")
            linea(80, green_color)
            confirmacion = Valida.validar_letras(f"{blue_color}¿Está seguro de que desea eliminar esta compañía? (s/n): {purple_color}", 1, 9, 58, 9).strip().lower()
            if confirmacion == 's':
                companies.remove(company_existente)
                self.json_file.save(companies)
                print(f"{purple_color}Compañía eliminada exitosamente!{reset_color}")
                linea(80, green_color)
            else:
                print(f"{purple_color}Eliminación cancelada.{reset_color}")
                linea(80, green_color)
        else:
            print(f"{purple_color}Compañía no encontrada.{reset_color}")
            linea(80, green_color)

        time.sleep(3)

    def consult(self):
        while True:
            BorrarPantalla()
            linea(80, green_color)
            print(f"{purple_color}{'Consulta de Compañías'.center(80)}{reset_color}")
            linea(80, green_color)
            
            companies_totales = len(self.json_file.read())
            print(f"{purple_color}Total de compañías registradas: {blue_color}{companies_totales}{reset_color}")

            menu = Menu(titulo=f"{blue_color}Seleccione una opción de consulta{reset_color}", opciones=["Buscar por RUC", "Buscar por Nombre", "Ver todas las compañías", "Volver al menú principal"], color=purple_color, color_numeros=blue_color)
            seleccion = menu.menu()
            linea(80, green_color)

            companies = []
            if seleccion == "1":
                ruc = str(Valida.validar_numeros(f"{blue_color}Ingrese el RUC de la compañía: {purple_color}", 1, 12, 32, 12))
                companies = self.json_file.find('ruc', ruc)
            elif seleccion == "2":
                name = Valida.validar_letras(f"{blue_color}Ingrese el nombre de la compañía: {purple_color}", 1, 16, 32, 16)
                companies = self.json_file.find('name', name)
            elif seleccion == "3":
                companies = self.json_file.read()
            elif seleccion == "4":
                return
            else:
                print(f"{purple_color}Opción inválida.{reset_color}")
                time.sleep(2)
                continue 
            
            if companies:
                gotoxy(1, 14); print(f"{purple_color}Resultados de la búsqueda:{reset_color}")
                for company in companies:
                    print(f"{purple_color}Nombre: {blue_color}{company['name']}\n{purple_color}RUC: {blue_color}{company['ruc']}\n{purple_color}")
            else:
                print(f"{purple_color}No se encontraron compañías con esa búsqueda.{reset_color}")

            linea(80, green_color)
            input(f"{blue_color}Presione Enter para volver al menú...{reset_color}")