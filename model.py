
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



engine = create_engine("sqlite:///inventory.db", echo=False) 
# echo turned to True, helps to send more messages to the console, so we may understand better whats happening

Session = sessionmaker(bind=engine)
# this binds our sessions to the database

session = Session() # we use sessions to keep track of the products

Base = declarative_base()




class Product(Base):

    __tablename__ = "products"

    
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer) # stored as an Integer, and then multiplied by 100 to represent cents
    date_updated = Column(Date)

    def __repr__(self):
        return f"<Product(name={self.product_name}, id={self.product_id},  quantity={self.product_quantity}, price={self.product_price}, date={self.date_updated})>"




if __name__ == '__main__':
    Base.metadata.create_all(engine)     # This connects the engine with the model class to create our database table

    #product = Product()

    #session.add(product)
    #session.commit() # this adds the product to the database

    #session.add_all(variable) # here we must pass in a variable
    #session.commit()

    #for product in variable:
    #    print(product.product_id)
