class Product:
    def __init__(self, id,descrip = "Ninguno",preci = 0,stock = 0 ):
        self.id = id
        self.descrip = descrip
        self.preci = preci
        self.__stock = stock
    
    
    @property
    def stock(self):
        return self.__stock
    
    @stock.setter
    def stock(self,stock):
        if stock >= 0:
            self.__stock = stock
        else:
            raise ValueError("No se puede tener stock negativo")
        
    def __str__(self):
        return f"ID: {self.id}\nDescripción: {self.descrip}\nPrecio: {self.preci}\nStock: {self.__stock}"
    
    def getjson(self):
        return {"ID":self.id, "Description":self.descrip, "Precio":self.preci, "Stock":self.__stock}

if __name__ == "__main__":
    Producto1 = Product(1,"Laptop", 1000, 10)