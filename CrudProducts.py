from Utilis import green_color, blue_color, purple_color, reset_color, BorrarPantalla,linea, Menu
from Components import Valida, gotoxy
from Company import Company
from Product import Product
from Icrud import Icrud
from clsJson import JsonFile
import os
import time

path, file = os.path.split(__file__)

class CrudProducts(Icrud):
    json_file = JsonFile(f"{path}/data/products.json")
    def create(self):
        compañia = Company()
        BorrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{'Registro de Productos'.center(80)}{reset_color}")
        linea(80, green_color)
        compañia.show()
        linea(80, green_color)
        productos = self.json_file.read()

        if productos:
            next_id = max(producto['ID'] for producto in productos) + 1
        else:
            next_id = 1 

        descrip = Valida.validar_letras(f"{blue_color}Descripción del producto: {purple_color}", 1, 7, 27, 7)
        preci = float(Valida.validar_numeros_decimales(f"{blue_color}Ingrese el precio del producto: {purple_color}", 1, 8, 33, 8))
        stock = int(Valida.validar_numeros(f"{blue_color}Ingrese la cantidad en stock: {purple_color}", 1, 9, 31, 9))

        producto_existente = any(p['Description'] == descrip for p in productos)

        if producto_existente:
            print(f"{purple_color}Este producto ya está registrado.{reset_color}")
        else:
            producto = Product(next_id, descrip, preci, stock)
            productos.append(producto.getjson())
            self.json_file.save(productos)
            print(f"{purple_color}Producto registrado exitosamente!{reset_color}")

        linea(80, green_color)
        time.sleep(3)

    def update(self):
        while True:
            compañia = Company()
            validar = Valida()
            BorrarPantalla()
            linea(80, green_color)
            print(f"{purple_color}{'Actualizar Producto'.center(80)}{reset_color}")
            linea(80, green_color)
            compañia.show()
            linea(80, green_color)

            product_id = int(Valida.validar_numeros(f"{blue_color}Ingrese el ID del producto a actualizar: {purple_color}", 1, 7, 42, 7))
            productos = self.json_file.read()
            producto_existente = next((producto for producto in productos if producto['ID'] == product_id), None)

            linea(80, green_color)

            if producto_existente:
                print(f"{purple_color}Producto encontrado: {producto_existente['Description']}{reset_color}")
                nuevo_preci = input(f"{blue_color}Nuevo precio (Enter para dejar sin cambios): {purple_color}").strip()
                nuevo_stock = input(f"{blue_color}Nuevo stock (Enter para dejar sin cambios): {purple_color}").strip()

                if nuevo_preci:
                    producto_existente['Precio'] = float(nuevo_preci)
                if nuevo_stock:
                    producto_existente['Stock'] = int(nuevo_stock)

                self.json_file.save(productos)
                print(f"{purple_color}Producto actualizado exitosamente!{reset_color}")
            else:
                print(f"{purple_color}Producto no encontrado.{reset_color}")

            linea(80, green_color)
            time.sleep(3)
            return

    def delete(self):
        while True:
            compañia = Company()
            validar = Valida()
            BorrarPantalla()
            linea(80, green_color)
            print(f"{purple_color}{'Eliminar Producto'.center(80)}{reset_color}")
            linea(80, green_color)
            compañia.show()
            linea(80, green_color)

            product_id = int(Valida.validar_numeros(f"{blue_color}Ingrese el ID del producto a eliminar: {purple_color}", 1, 7, 40, 7))
            productos = self.json_file.read()
            producto_existente = next((producto for producto in productos if producto['ID'] == product_id), None)

            if producto_existente:
                print(f"{purple_color}Producto encontrado:\n{blue_color}Descripción: {purple_color}{producto_existente['Description']}{reset_color}\n{blue_color}Precio: {purple_color}{producto_existente['Precio']}{reset_color}\n{blue_color}Stock: {purple_color}{producto_existente['Stock']}{reset_color}")
                linea(80, green_color)
                confirmacion = input(f"{blue_color}¿Está seguro de que desea eliminar este producto? (s/n): {purple_color}").strip().lower()

                if confirmacion == 's':
                    productos.remove(producto_existente)
                    self.json_file.save(productos)
                    print(f"{purple_color}Producto eliminado exitosamente!{reset_color}")
                else:
                    print(f"{purple_color}Eliminación cancelada.{reset_color}")
            else:
                print(f"{purple_color}Producto no encontrado.{reset_color}")

            linea(80, green_color)
            time.sleep(3)
            return

    def consult(self):
        while True:
            BorrarPantalla()
            compañia = Company()
            linea(80, green_color)
            print(f"{purple_color}{'Consulta de Productos'.center(80)}{reset_color}")
            linea(80, green_color)
            compañia.show()
            linea(80, green_color)

            menu = Menu(titulo=f"{blue_color}Seleccione una opción de consulta{reset_color}", opciones=["Buscar por ID", "Buscar por Descripción", "Ver todos los productos", "Volver al menú principal"], color=purple_color, color_numeros=blue_color)
            seleccion = menu.menu()
            linea(80, green_color)

            productos = []
            if seleccion == "1":
                product_id = int(Valida.validar_numeros(f"Ingrese el ID del producto:",1,14,28,14))
                productos = self.json_file.find('ID', product_id)
            elif seleccion == "2":
                descrip = Valida.validar_letras(f"Ingrese la descripción del producto:",1,14,35,14)
                productos = self.json_file.find('Descripción', descrip)
            elif seleccion == "3":
                productos = self.json_file.read()
            elif seleccion == "4":
                return
            else:
                print(f"{purple_color}Opción inválida.{reset_color}")
                time.sleep(2)
                continue 

            if productos:
                gotoxy(1, 15); print(f"{purple_color}Resultados de la búsqueda:{reset_color}")
                for producto in productos:
                    print(f"{purple_color}ID: {blue_color}{producto['ID']}\n{purple_color}Descripción: {blue_color}{producto['Description']}\n{purple_color}Precio: {blue_color}{producto['Precio']}\n{purple_color}Stock: {blue_color}{producto['Stock']}\n{reset_color}")
            else:
                print(f"{purple_color}No se encontraron productos con esa búsqueda.{reset_color}")

            linea(80, green_color)
            input(f"{blue_color}Presione Enter para volver al menú...{reset_color}")