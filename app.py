from model import Base, session, Product, engine
import csv
import datetime 


def menu():
    while True:
        print("""
            \nProducts
              \rv) Display a product by its ID
              \ra) View all Products
              \rb) Search for book
              \re) Exit
            """)
        choice = input("what would you like to do? ")
        if choice in ["v", "a", "b"]:
            return choice   # return will always cancel out or stop a loop
        else:
            input("""\rPlease choose one of the options above.
                  \ra letter from the following (v/a/b/e)
                  \rPress enter to try again """)


def clean_date(date_str):

    split_date = date_str.split("/")
    month_date = int(split_date[0])
    day_date = int(split_date[1])
    year_date = int(split_date[2])
    # date_type_variable = datetime.datetime(year=0, month=0, day=0)
    #print(split_date)
    return datetime.date(year=year_date, month=month_date, day=day_date)



def clean_price(price_str):
    split_price = price_str.split("$")
    splitted_price_str = split_price[1]
    price_float = float(splitted_price_str)
    #print(price_float)
    return int(price_float * 100)



def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        next(data)  # returns the next item in an iterator
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none() # one_or_none returns none if there isn't a book or returns the book
            # this is going to either return a product if there is one or none if there isn't a book
            if product_in_db == None:
                product_name = row[0]
                product_quantity = row[2]
                date = clean_date(row[3])
                price = clean_price(row[1])
                new_product = Product(product_name=product_name,
                                      product_price=price,
                                      product_quantity=product_quantity,
                                      date_updated= date )
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "v":
            # Add product
            pass
        elif choice == "a":
            # view products
            pass
        elif choice == "b":
            # search product
            pass
        else:
            print("Goodbye ")
            app_running = False


"""
['product_name', 'product_price', 'product_quantity', 'date_updated']
['Bagel - Whole White Sesame', '$4.30', '97', '11/1/2018']
['Sauce - Caesar Dressing', '$8.05', '81', '12/28/2018']
['Shiratamako - Rice Flour', '$7.99', '71', '3/7/2018']


ValueError: invalid literal for int() with base 10: 'date_updated'


"""



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    #app()

    #add_csv() # we add the csv values to the database
    
    #clean_date("7/26/2018")  # used this line to test the split function for the date data
    #clean_price("$7.99")   # we test the clean_price function, as well as the split function in it

    #for product in session.query(Product): # we loop through all of our books to make sure they have been added to the database
    #    print(product)





