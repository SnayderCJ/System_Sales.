from Utilis import green_color, blue_color, purple_color, reset_color,red_color, BorrarPantalla,linea, Menu,gotoxy
from CrudClients import CrudClients
from CrudProducts import CrudProducts
from CrudCompany import CrudCompany
from Company import Company
from Sales import Sale, SaleDetail, Product
from Icrud import Icrud
from clsJson import JsonFile
from Customer import RegularClient, VipClient
from Product import Product 
from datetime import date
from Components import Valida
import datetime
import os
import time
import platform


path, file = os.path.split(__file__)

class CrudSales(Icrud):
 def create(self):
    validar = Valida()
    Compañia = Company()
    BorrarPantalla()
    print('\033c', end='')
    linea(90,green_color)
    gotoxy(30, 2); print(blue_color + "Registro de Venta")
    linea(90,green_color)
    gotoxy(1, 4); print(f"{blue_color}Empresa: {purple_color}{Compañia.name}{reset_color} {" "*4} {blue_color}RUC: {purple_color}{Compañia.ruc}{reset_color}")

    json_file = JsonFile(f"{path}/data/invoices.json")
    invoices = json_file.read()

    if invoices:
        last_invoice = int(invoices[-1]["factura"][1:]) 
        new_invoice = f"F{last_invoice + 1:07d}" 
    else:
        new_invoice = "F0000001"  

    gotoxy(1, 5); print(f"{blue_color}Factura#: {purple_color}{new_invoice} {" "*4} {blue_color}Fecha: {purple_color}{datetime.datetime.now()}{reset_color}")
    gotoxy(66, 4); print(f"{blue_color}Subtotal:")
    gotoxy(66, 5); print(f"{blue_color}Decuento:")
    gotoxy(66, 6); print(f"{blue_color}Iva     : ")
    gotoxy(66, 7); print(f"{blue_color}Total   :")
    gotoxy(1, 7); print(f"{blue_color}Cedula:{reset_color}{purple_color} ")
    
    dni = validar.solo_numeros("Error: Solo numeros", 9, 7)
    json_file = JsonFile(f"{path}/data/clients.json")
    client = json_file.find("DNI", dni)
    
    if not client:
        gotoxy(35, 6); print("Cliente no existe")
        return
    
    client = client[0]
    if client['Valor'] == 0.1:
        cli = RegularClient(client['Nombre'], client['Apellido'], client['DNI'], True)
    elif client['Valor'] == 0:
        cli = RegularClient(client['Nombre'], client['Apellido'], client['DNI'], False)
    elif client['Valor'] >= 10000:
        cli = VipClient(client['Nombre'], client['Apellido'], client['DNI'])

    sale = Sale(cli)
    gotoxy(25, 7); print(f"{blue_color} Nombres: {purple_color}{client['Nombre']} {client['Apellido']}{reset_color}")
    gotoxy(1, 8); print(green_color + "-" * 90 + reset_color)
    gotoxy(5, 9); print(purple_color + "Linea")
    gotoxy(12, 9); print("Id_Articulo")
    gotoxy(24, 9); print("Descripcion")
    gotoxy(38, 9); print("Precio")
    gotoxy(48, 9); print("Cantidad")
    gotoxy(58, 9); print("Subtotal")
    gotoxy(70, 9); print("n->Terminar Venta)" + reset_color)

    follow = "s"
    line = 1
    while follow.lower() == "s":
        gotoxy(7, 9 + line); print(line)
        gotoxy(15, 9 + line)
        id = int(validar.solo_numeros("Error: Solo numeros", 15, 9 + line))
        json_file = JsonFile(f"{path}/data/products.json")
        prods = json_file.find("ID", id)
        
        if not prods:
            gotoxy(24, 9 + line); print("Producto no existe")
            time.sleep(1)
            gotoxy(24, 9 + line); print(" " * 20)
        else:
            prods = prods[0]
            product = Product(prods["ID"], prods["Description"], prods["Precio"], prods["Stock"])
            gotoxy(24, 9 + line); print(product.descrip)
            gotoxy(38, 9 + line); print(product.preci)
            gotoxy(49, 9 + line); qyt = int(validar.solo_numeros("Error:Solo numeros", 49, 9 + line))
            gotoxy(59, 9 + line); print(product.preci * qyt)
            sale.add_detail(product, qyt)
            gotoxy(76, 4); print(f"{purple_color}{round(sale.subtotal, 2)}")
            gotoxy(76, 5); print(round(sale.discount, 2))
            gotoxy(76, 6); print(round(sale.iva, 2))
            gotoxy(76, 7); print(round(sale.total, 2))
            gotoxy(74, 9 + line); follow = input() or "s"
            gotoxy(76, 9 + line); print(green_color + "✔" + reset_color)
            line += 1
    gotoxy(1, 10 + line); print(green_color + "-" * 90 + reset_color)
    gotoxy(15, 11 + line); print(blue_color + "Esta seguro de grabar la venta(s/n):")
    gotoxy(54, 11 + line); procesar = input().lower()
    
    if procesar == "s":
        gotoxy(15, 12 + line); print(" Venta Grabada satisfactoriamente " + reset_color)
        
        data = sale.getJson()
        data["factura"] = new_invoice
        invoices.append(data)
        
        json_file = JsonFile(f"{path}/data/invoices.json")
        json_file.save(invoices)
    else:
        gotoxy(20, 10 + line); print(" Venta Cancelada " + reset_color)
    
    time.sleep(2)
 def update(self):
    while True:
        BorrarPantalla()
        compañia = Company()
        linea(90,green_color)
        gotoxy(30, 2); print(blue_color + "Actualización de Venta")
        linea(90,green_color)
        compañia.show()
        linea(90,green_color)

        invoice_number = input(f"{blue_color}Ingrese el número de factura que desea actualizar: {purple_color}")

        json_file = JsonFile(f"{path}/data/invoices.json")
        invoices = json_file.read()

        if invoices:
            for invoice in invoices:
                if invoice["factura"] == invoice_number:
                    while True:
                        BorrarPantalla()
                        linea(90,green_color)
                        gotoxy(30, 2); print(blue_color + "Actualización de Venta")
                        linea(90,green_color)
                        compañia.show()
                        linea(90,green_color)
                        print(blue_color + "Número de Factura: " + purple_color + f"{invoice['factura']}")
                        print(blue_color + "Fecha:" + purple_color + f"{invoice['Date']}")
                        print(blue_color + "Cliente: " + purple_color + f"{invoice['Client']['Nombre']} {invoice['Client']['Apellido']}")
                        print(blue_color + "Total:" + purple_color + f"{invoice['Total']}")
                        gotoxy(2, 12)
                        print("\nDetalle de la Venta:")
                        
                        detalles = invoice['details']
                        print(f"{blue_color + 'num'.center(5)} {blue_color + 'Producto'.center(28)} {blue_color + 'Cantidad'.center(10)} {blue_color + 'Precio'.center(10)}")
                        
                        for i, detalle in enumerate(detalles, start=1):
                            print(purple_color + f" {i}) {detalle['Product'].center(28)} {str(detalle['Quantity']).center(10)}  {str(detalle['Price']).center(10)}")
                        
                        linea(90,green_color)
                        gotoxy(2, 20)
                        print(blue_color + "\nOpciones:")
                        print("1. Modificar cantidad de un producto")
                        print("2. Eliminar un producto")
                        print("3. Agregar un nuevo producto")
                        print("4. Terminar actualización")
                        
                        option = Valida.validar_numeros("Seleccione una opción: ", 2, 23, 25, 21)

                        if option == "1":
                            # Modificar cantidad de un producto en la factura
                            detalle_index = int(input(f"{blue_color}Ingrese el número de línea del detalle que desea modificar: {purple_color}")) - 1
                            
                            if 0 <= detalle_index < len(detalles):
                                new_quantity = int(input(f"{blue_color}Ingrese la nueva cantidad para el producto {detalles[detalle_index]['Product']}: {purple_color}"))
                                detalles[detalle_index]['Quantity'] = new_quantity

                                
                                invoice['Total'] = sum(item['Quantity'] * item['Price'] for item in detalles)
                                linea(90,green_color)
                                print(blue_color + "Cantidad modificada correctamente.")
                                linea(90,green_color)
                                input("Presione Enter para continuar...")
                            else:
                                print("Número de línea inválido.")
                                input("Presione Enter para continuar...")

                        elif option == "2":
                            detalle_index = int(input(f"{blue_color}Ingrese el número de línea del detalle que desea eliminar: {purple_color}")) - 1
                            
                            if 0 <= detalle_index < len(detalles):
                                del detalles[detalle_index]
                                
                                invoice['Total'] = sum(item['Quantity'] * item['Price'] for item in detalles)
                                linea(90,green_color)
                                gotoxy(3, 29)
                                print(blue_color + "Producto eliminado correctamente.")
                                gotoxy(4, 30)
                                input("Presione Enter para continuar...")
                            else:
                                print("Número de línea inválido.")
                                input("Presione Enter para continuar...")

                        elif option == "3":
                            product_id = int(input(f"{blue_color}Ingrese el ID del nuevo producto: {purple_color}"))
                            product_quantity = int(input(f"{blue_color}Ingrese la cantidad del nuevo producto: {purple_color}"))
                            
                            json_file_products = JsonFile(f"{path}/data/products.json")
                            products = json_file_products.find("ID", product_id)
                            
                            if products:
                                product = products[0]
                                new_product = {
                                    'Product': product['Description'],  
                                    'Price': product['Precio'],
                                    'Quantity': product_quantity
                                }

                                detalles.append(new_product)

                                invoice['Total'] = sum(item['Quantity'] * item['Price'] for item in detalles)
                                print("Producto agregado correctamente.")
                                input("Presione Enter para continuar...")
                            else:
                                print("Producto no encontrado.")
                                input("Presione Enter para continuar...")

                        elif option == "4":
                            print("Actualización de factura terminada.")
                            
                            invoice['details'] = detalles
                            for index, inv in enumerate(invoices):
                                if inv["factura"] == invoice_number:
                                    invoices[index] = invoice
                                    break
                            
                            json_file.save(invoices)
                            break

                        else:
                            print("Opción inválida. Intente nuevamente.")
                            input("Presione Enter para continuar...")
        
        else:
            print("No hay facturas disponibles.")

        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)
 def delete(self):
        BorrarPantalla()
        compañia = Company()
        linea(90,green_color)
        gotoxy(30, 2); print(blue_color + "Eliminación de Factura")
        linea(90,green_color)
        compañia.show()
        linea(90,green_color)

        invoice_number = input(f"{blue_color}Ingrese el número de factura que desea eliminar: {purple_color}")
        
        json_file = JsonFile(f"{path}/data/invoices.json")
        invoices = json_file.read()

        found = False
        updated_invoices = []
        for invoice in invoices:
            if invoice["factura"] == invoice_number:
                found = True

                gotoxy(2, 9)
                print("Factura encontrada:")
                gotoxy(2, 10)
                print(blue_color + "Número de Factura: "+ purple_color +f"{invoice['factura']}")
                gotoxy(2, 10)
                print(blue_color + "Fecha: " + purple_color + f"{invoice['Date']}")
                gotoxy(2, 11)
                print(blue_color + "Cliente: " + purple_color + f"{invoice['Client']['Nombre']} {invoice['Client'] ['Apellido']}")
                gotoxy(2, 12)
                print(blue_color + "Total: " + purple_color + f"{invoice['Total']}")
                gotoxy(2, 14)
                print(blue_color + "Detalle de la Venta:")
                print(f" {'Producto'.center(20)}  {'Cantidad'.center(20)} {'Precio'.center(20)}")
                for i, detalle in enumerate(invoice['details'], start=1):
                    print(purple_color + f"{detalle['Product'].center(20)} {str(detalle['Quantity']).center(20)}  {str(detalle['Price']).center(20)}")
                print(green_color + "=" * 90 + reset_color)

                confirmacion = input(blue_color + "¿Está seguro que desea eliminar esta factura? (s/n): " + purple_color).lower()
                if confirmacion == "s":
                    print("Factura eliminada exitosamente.")
                else:
                    print("Eliminación cancelada.")
            else:
                updated_invoices.append(invoice)

        if not found:
            print("Factura no encontrada.")

        json_file.save(updated_invoices)
        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)
 
 def consult(self):
        BorrarPantalla()
        compañia = Company()
        linea(90,green_color)
        gotoxy(30, 2); print(blue_color + "Consulta de Factura")
        linea(90,green_color)
        compañia.show()
        linea(90,green_color)

        invoice_number = input(f"{blue_color}Ingrese el número de factura que desea consultar: {purple_color}")

        json_file = JsonFile(f"{path}/data/invoices.json")
        invoices = json_file.read()

        found = False
        for invoice in invoices:
            if invoice["factura"] == invoice_number:
                found = True

                gotoxy(2, 8)
                print("Factura encontrada:")
                gotoxy(2, 9)
                print(blue_color + "Número de Factura: " + purple_color + f"{invoice['factura']}")
                gotoxy(2, 10)
                print(blue_color + "Fecha: " + purple_color + f"{invoice['Date']}")
                gotoxy(2, 11)
                print(blue_color + "Cliente: " + purple_color + f"{invoice['Client']['Nombre']} {invoice['Client'] ['Apellido']}")
                gotoxy(2, 12)
                print(blue_color + "Total: " + purple_color + f"{invoice['Total']}")
                gotoxy(2, 14)
                print(blue_color + "Detalle de la Venta:")
                print(f" {'Producto'.center(20)}  {'Cantidad'.center(20)} {'Precio'.center(20)}")
                for detalle in invoice['details']:
                    print(purple_color + f"{detalle['Product'].center(20)} {str(detalle['Quantity']).center(20)}  {str(detalle['Price']).center(20)}")
                linea(90,green_color)
                break

        if not found:
            gotoxy(2, 8)
            print("Factura no encontrada.")
        gotoxy(2, 18)
        input("Presione una tecla para continuar...")
 


opc = ''
while opc != '5':
    BorrarPantalla()
    menu_main = Menu("Menu facturación", ["Clientes", "Productos", "Ventas", "Compañía", "Salir"])
    opc = menu_main.menu()
    
    if opc == '1':
        opc1 = ''
        while opc1 != '5':
            BorrarPantalla()
            menu_clients = Menu("Menu clientes", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
            opc1 = menu_clients.menu()
            crud = CrudClients()
            if opc1 == '1':
                crud.create()
            elif opc1 == '2':
                crud.update()
            elif opc1 == '3':
                crud.delete()
            elif opc1 == '4':
                crud.consult()
            print("Regresando al menu principal")
    
    elif opc == '2':
        opc2 = ''
        while opc2 != '5':
            BorrarPantalla()
            menu_products = Menu("Menu productos", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
            opc2 = menu_products.menu()
            crud = CrudProducts()
            if opc2 == '1':
                crud.create()
            elif opc2 == '2':
                crud.update()
            elif opc2 == '3':
                crud.delete()
            elif opc2 == '4':
                crud.consult()
    
    elif opc == '3':
        opc3 = ''
        while opc3 != '5':
            BorrarPantalla()
            menu_sales = Menu("Menu ventas", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
            opc3 = menu_sales.menu()
            crud = CrudSales()
            if opc3 == '1':
                crud.create()
            elif opc3 == '2':
                crud.update()
            elif opc3 == '3':
                crud.delete()
            elif opc3 == '4':
                crud.consult()
    
    elif opc == '4':
        opc4 = ''
        while opc4 != '5':
            BorrarPantalla()
            menu_company = Menu("Menu compañía", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
            opc4 = menu_company.menu()
            crud = CrudCompany()
            if opc4 == '1':
                crud.create()
            elif opc4 == '2':
                crud.update()
            elif opc4 == '3':
                crud.delete()
            elif opc4 == '4':
                crud.consult()
                print("Regresando al menu principal")

    print("Regresando al menu principal")

BorrarPantalla()
input("Presione una tecla para salir...")
BorrarPantalla()