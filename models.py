class Pc:
    def __init__(
            self, 
            id : int,
            brand : str,
            model : str,
            year: int ,
            price : int ):
        self.id =id
        self.brand =brand
        self.model =model
        self.year =year
        self.price =price

    def __repr__(self):
        return f'<Pc : {self.model}>'
