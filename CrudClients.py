from Customer import RegularClient, VipClient
from Icrud import Icrud
from clsJson import JsonFile
from Utilis import BorrarPantalla, Menu, green_color, blue_color, purple_color, reset_color, linea, gotoxy
from Components import Valida
from Company import Company
import time
import os

path, file = os.path.split(__file__)

class CrudClients(Icrud):
    json_file = JsonFile(f"{path}/data/clients.json")
   
    def create(self): 
        company = Company()
        while True:
            BorrarPantalla()
            linea(80,green_color)
            print(f"{purple_color}{'Registro de Cliente'.center(80)}{reset_color}")
            linea(80,green_color)
            company.show()
            linea(80,green_color)
            menu = Menu(titulo=f"{blue_color}Seleccione el tipo de cliente", opciones=["Cliente Regular", "Cliente VIP", "Volver al menú principal"], color=purple_color , color_numeros=blue_color)
            seleccion = menu.menu()
            linea(80,green_color)
            if seleccion == "1":
                tipo_cliente = "Regular"
            elif seleccion == "2":
                tipo_cliente = "VIP"
            elif seleccion == "3":
                return
            else:
                print("Opción inválida.")
                time.sleep(2)
                continue 

            nombre = Valida.validar_letras(f"{blue_color}Ingresa el nombre del cliente: {purple_color}", 1, 13, 32, 13)
            apellido = Valida.validar_letras(f"{blue_color}Ingresa el apellido del cliente: {purple_color}", 1, 14, 34, 14)
            dni = Valida.validar_dni(f"{blue_color}Ingrese el DNI del cliente: {purple_color}", 1, 15, 29, 15)

            if tipo_cliente == "Regular":
                tarjeta = Valida.validar_letras(f"{blue_color}¿El cliente tiene tarjeta de descuento? (s/n): {purple_color}",1,17,48,17).strip().lower() == "s"
                cliente = RegularClient(nombre, apellido, dni, tarjeta)
            else:
                cliente = VipClient(nombre, apellido, dni)
            linea(80,green_color)
            clientes = self.json_file.read()
            cliente_existente = any(c['DNI'] == dni for c in clientes)

            if cliente_existente:
                print(f"{purple_color}Este cliente ya está registrado. {reset_color}") 
            else:
                clientes.append(cliente.getJson())
                self.json_file.save(clientes)
                print(f"{purple_color}Cliente registrado exitosamente! {reset_color}")
            linea(80,green_color)
            time.sleep(3)

    def update(self):
        while True:
            compañia = Company()
            BorrarPantalla()
            linea(80,green_color)
            print(f"{purple_color}{'Actualizar Cliente'.center(80)}{reset_color}")
            linea(80,green_color)
            compañia.show()
            linea(80,green_color)
            dni = Valida.validar_dni(f"{blue_color}Ingrese el DNI del cliente a actualizar: {purple_color}", 1, 7, 42, 7)
            clientes = self.json_file.read()
            cliente_existente = next((cliente for cliente in clientes if cliente['DNI'] == dni), None)
            linea(80,green_color)

            if cliente_existente:
                print(f"{purple_color}Cliente encontrado: {cliente_existente['Nombre']} {cliente_existente['Apellido']}{reset_color}")
                nuevo_nombre = input(f"{blue_color}Nuevo nombre (Enter para dejar sin cambios): {purple_color}")
                nuevo_apellido = input(f"{blue_color}Nuevo apellido (Enter para dejar sin cambios): {purple_color}")

                if nuevo_nombre:
                    cliente_existente['Nombre'] = nuevo_nombre
                if nuevo_apellido:
                    cliente_existente['Apellido'] = nuevo_apellido

                linea(80,green_color)

                self.json_file.save(clientes)
                print(f"{purple_color}Cliente actualizado exitosamente!{reset_color}")
            else:
                print(f"{purple_color}Cliente no encontrado.{reset_color}")

            linea(80,green_color)
            time.sleep(3)
            return
    
    def delete(self):
        while True:
            BorrarPantalla()
            compañia = Company()
            linea(80,green_color)
            print(f"{purple_color}{'Eliminar Cliente'.center(80)}{reset_color}")
            linea(80,green_color)
            compañia.show()
            linea(80,green_color)

            dni = Valida.validar_dni(f"{blue_color}Ingrese el DNI del cliente a eliminar: {purple_color}" , 1, 7, 40, 7)
            clientes = self.json_file.read()
            cliente_existente = next((cliente for cliente in clientes if cliente['DNI'] == dni), None)

            if cliente_existente:
                print(f"{purple_color}Cliente encontrado:\n{blue_color}Nombre: {purple_color}{cliente_existente['Nombre']}\n{blue_color}Apellido: {purple_color}{cliente_existente['Apellido']}{reset_color}")
                linea(80,green_color)
                confirmacion = Valida.validar_letras(f"{blue_color}¿Está seguro de que desea eliminar este cliente? (s/n): {purple_color}",1,13,56,13).strip().lower()
                linea(80,green_color)
                if confirmacion == 's':
                    clientes.remove(cliente_existente)
                    self.json_file.save(clientes)
                    print(f"{purple_color}Cliente eliminado exitosamente!{reset_color}")
                else:
                    print(f"{purple_color}Eliminación cancelada.{reset_color}")
            else:
                print(f"{purple_color}Cliente no encontrado.{reset_color}")

            linea(80,green_color)
            time.sleep(3)
            return
    
    def consult(self):
        while True:
            BorrarPantalla()
            compañia = Company()
            linea(80,green_color)
            print(f"{purple_color}{'Consulta de Clientes'.center(80)}{reset_color}")
            linea(80,green_color)
            compañia.show()
            linea(80,green_color)

            clientes_totales = len(self.json_file.read())  
            print(f"{purple_color}Total de clientes registrados: {blue_color}{clientes_totales}{reset_color}")  

            menu = Menu(titulo=f"{blue_color}Seleccione una opción de consulta{reset_color}", opciones=["Buscar por DNI", "Buscar por Nombre", "Buscar por Apellido", "Ver todos los clientes", "Volver al menú principal"], color=purple_color, color_numeros=blue_color)
            seleccion = menu.menu()
            linea(80,green_color)

            clientes = []
            if seleccion == "1":
                dni = Valida.validar_dni(f"{blue_color}Ingrese el DNI del cliente: {purple_color}", 1, 16, 28, 16)
                clientes = self.json_file.find('DNI', dni)
            elif seleccion == "2":
                nombre = Valida.validar_letras(f"{blue_color}Ingrese el nombre del cliente: {purple_color}", 1, 16, 34, 16)
                clientes = self.json_file.find('Nombre', nombre)
            elif seleccion == "3":
                apellido = Valida.validar_letras(f"{blue_color}Ingrese el apellido del cliente: {purple_color}", 1, 16, 34, 16)
                clientes = self.json_file.find('Apellido', apellido)
            elif seleccion == "4":
                clientes = self.json_file.read()
            elif seleccion == "5":
                return
            else:
                print(f"{purple_color}Opción inválida.{reset_color}")
                time.sleep(2)
                continue 
         
            if clientes:   
                gotoxy(1,17);print(f"{purple_color}Resultados de la búsqueda:{reset_color}")
                for cliente in clientes:
                    print(f"{purple_color}Nombre: {blue_color}{cliente['Nombre']}\n{purple_color}Apellido: {blue_color}{cliente['Apellido']}\n{purple_color}DNI: {blue_color}{cliente['DNI']}\n{purple_color}")
            else:
                print(f"{purple_color}No se encontraron clientes con esa búsqueda.{reset_color}")

            linea(80,green_color)
            input(f"{blue_color}Presione Enter para volver al menú...{reset_color}")
