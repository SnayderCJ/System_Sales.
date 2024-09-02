from datetime import date
from Company import Company
from Product import Product
from Customer import RegularClient, VipClient
from Icalculos import ICalculos
from Utilis import green_color, blue_color, purple_color, reset_color, BorrarPantalla
import os

class SaleDetail:
    next_id = 0
    def __init__(self, product, quantity):
        SaleDetail.next_id += 1
        self.__id = SaleDetail.next_id
        self.product = product
        self.quantity = quantity
        self.preci = product.preci
    
    @property
    def id(self):
        return self.__id
    
    def __str__(self):
        return f' {self.id}  {self.product.descrip}  {self.quantity}  {self.preci}'
    
class Sale(ICalculos):
    next_id = 0
    Factor_iva = 0.12
    def __init__(self, client):
        Sale.next_id += 1
        self.__invoice = f"F{Sale.next_id:07d}"
        self.date = date.today()
        self.client = client
        self.subtotal = 0
        self.porcentage_discount = client.discount if isinstance(client, RegularClient) else 0
        self.discount = 0
        self.iva = 0
        self.total = 0
        self.details = []
    
    @property
    def invoice(self):
        print(self.__invoice)
    
    def add_detail(self, prod, qty):
        detail = SaleDetail(prod, qty)
        self.subtotal += round(detail.preci * detail.quantity, 2)
        self.discount = round(self.subtotal * self.porcentage_discount, 2)
        self.iva = self.cal_iva(Sale.Factor_iva, self.subtotal - self.discount)
        self.total = round(self.subtotal - self.discount + self.iva, 2)
        self.details.append(detail)
    
    def cal_iva(self, iva, value):
        return round(value * iva, 2)
    
    def cal_discount(self, valor = 0, discount = 0):
        return round(valor * discount, 2)
    

    def print_invoice(self,company):
        BorrarPantalla()
        print('\033c', end='')
        print(green_color + "*"*70 + reset_color)
        print(blue_color + f"Empresa: {company.name} Ruc: {company.ruc}", end='')
        print(" Factura#:{:7}Fecha:{}".format(self.invoice, self.date))
        self.client.show()
        print(green_color + "*"*70 + reset_color)
        print(purple_color + "Linea Articulo Precio Cantidad Subtotal")
        for det in self.details:
            print(blue_color + f"{det.id:5} {det.product.descrip:6} {det.preci:7} {det.quantity:2} {det.preci*det.quantity:14}")
        print(green_color + "*"*70 + reset_color)
        print(purple_color + " "*23, "Subtotal:  ", str(self.subtotal))
        print(" "*23, "Descuento: ", str(self.discount))
        print(" "*23, "Iva:       ", str(self.iva))
        print(" "*23, "Total:     ", str(self.total) + reset_color)

    def getJson(self):
        invoice = {"Invoice":self.invoice, "Date":str(self.date), "Client":self.client.getJson(), "Subtotal":self.subtotal, "Discount":self.discount, "Iva":self.iva, "Total":self.total, "details":[]}
        for det in self.details:
            invoice["details"].append(
                {"Product":det.product.descrip, "Price":det.preci, "Quantity":det.quantity} 
            )
        return invoice
    
if __name__ == '__main__':
    company = Company()
    cli1 = RegularClient("Daniel", "Vera", "0914122419", card=True)
    cli2 = VipClient("Erick", "Bohorquez", "0714122412")
    product1 = Product("Aceite", 2, 1000)
    product2 = Product("Colas", 3, 5000)
    sale1 = Sale(cli1)
    sale1.add_detail(product1, 5)
    sale1.add_detail(product2, 10)
    sale1.print_invoice(company)
