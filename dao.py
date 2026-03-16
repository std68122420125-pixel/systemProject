from systemProject.connectdb import con,cur 
from models import Pc

def insert(product: Pc):
    sql =' insert into pc(brand, model, year, price) values(?,?,?,?)' 
    rs = con.execute(sql, (product.brand, product.model,product.year, product.price))
    row = rs.rowcount
    if row > 0 : 
        con.commit()
        return row 
    else:
        return 0 

def update(product: Pc):
    sql =' update product set price= ? where id =?  values(?,?,?,?)' 
    rs = con.execute(sql, (product.price ,product.id))
    row = rs.rowcount
    if row > 0 : 
        con.commit()
        return row 
    else:
        return 0 
    
def delete (id: int):
    sql = 'delete from prroduct where id = ?'
    rs = con.execute(sql,(id, ))
    row = rs.rowcount
    if row >0:
        con.commit()
        return row
    else:
        return 0
    
def select():
    sql ='select *from product'
    rs =con.execute(sql)
    products = rs.fetchall()
    if products:
        data =[]
        for product in products:
            id, brand ,model,year,price = product
            data.append(Pc(id=id,brand=brand,model=model,year=year,price=price))
        return data
    else:
     return[]
    
def select_by_brand(brand_name: str):
    sql ='select *from product where brand like ?'
    rs =con.execute(sql('%' + brand_name + '%', ))
    products = rs.fetchall()
    if products:
        data =[]
        for product in products:
            id, brand ,model,year,price = product
            data.append(Pc(id=id,brand=brand,model=model,year=year,price=price))
        return data
    else:
     return[]