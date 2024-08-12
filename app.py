from model import Base, session, Product, engine
import csv
import datetime 
from sys import exit
import time


def menu():
    while True:
        print("""
            \nProducts
              \rv) Display a Product by its ID
              \ra) Add a new product to the database
              \rb) Make a backup of the entire database
              \re) Exit
            """)
        choice = input("what would you like to do? ")
        if choice in ["v", "a", "b", "e"]:
            return choice   # return will always cancel out or stop a loop
        else:
            input("""\rPlease choose one of the options above.
                  \ra letter from the following (v/a/b/e)
                  \rPress enter to try again """)


def clean_date(date_str):

    split_date = date_str.split("/")
    try:
        month_date = int(split_date[0])
        day_date = int(split_date[1])
        year_date = int(split_date[2])
        # date_type_variable = datetime.datetime(year=0, month=0, day=0)
        #print(split_date)
        return_date = datetime.date(year=year_date, month=month_date, day=day_date)

    except ValueError:
        input("""
                \n ***Date Error***
                \r The date format should include a valid Month/Day/Year from the past
                \rExample: 12/28/2018
                \rPress enter to try again
                \r*****************
""")

    else:
        return return_date
    



def clean_price(price_str):

    try:
        split_price = price_str.split("$")
        splitted_price_str = split_price[1]
        price_float = float(splitted_price_str)
        
    except ValueError:
        input("""
                \n ***Price Error***
                \r The price format should include a valid $#.## (currency symbol dollar.cents)
                \rExample: $7.99
                \rPress enter to try again
                \r*****************
""")
    else:
        #print(price_float)
        return int(price_float * 100)
    
    
def clean_id(id_str, id_options):
    try:
        product_id = int(id_str)
        

    except ValueError:
        input("""
                \n ***Id Error***
                \r The id format should be a number 
                \rExample: 14
                \rPress enter to try again
                \r***************** """)
        return None
        
    else:
        if product_id in id_options:
            return product_id
        
        else:
            input(f"""
                \n ***Id Error***
                \r Options: {id_options} 
                \r Press enter to try again
                \r***************** """)
            return None




def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        next(data)  # returns the next item in an iterator
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none() 
            # one_or_none returns none if there isn't a book or returns the book
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


def generate_backup():

    with open("backup.csv", "w", newline='') as csvfile:
        productwriter = csv.writer(csvfile)# fieldnames=fieldnames)

        productwriter.writerow(['product_id',
                                'product_name', 
                                'product_price', 
                                'product_quantity', 
                                'date_updated'])
        
        for product in session.query(Product).order_by(Product.product_id):
            productwriter.writerow([product.product_id,
                             product.product_name,
                             product.product_price,
                             product.product_quantity,
                             product.date_updated])
    print("The data has been backed-up to the 'back-up.csv' data file")
    




def app():
    app_running = True
    while app_running:
        choice = menu()

        if choice == "v":
            # Display a product by its ID
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f"""
                \nId Options: {id_options} 
                \rPlease enter the Product id: """)
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.product_id==id_choice).first()
            print(f"""
            \n {the_product.product_name}, 
            \r Costs: ${the_product.product_price/100}, Amount available: {the_product.product_quantity},
            \r last date updated: {the_product.date_updated}
                """)
            input("\n Press enter to go back to the main menu ")
            

        elif choice == "a":
            # Add a new product to the database
            name = input("product_name: ")

            price_error = True
            while price_error:
                price = input("product_price: (Example: $4.30) ")
                price_cleaned = clean_price(price)
                if type(price_cleaned) == int:
                    price_error = False


            quantity = input("product_quantity: ")

            date_error = True
            while date_error:
                date = input("date_updated: (Example: 12/28/2018) ")
                date_cleaned = clean_date(date)
                if type(date_cleaned) == datetime.date:
                    date_error = False
                
            new_product = Product(product_name=name, 
                                  product_price=price_cleaned, 
                                  product_quantity=quantity, 
                                  date_updated=date_cleaned)
            session.add(new_product)
            session.commit()
            print("product added !!!")
            input("\n Press enter to go back to the main menu ")
            time.sleep(3)
            

        elif choice == "b":
            # Make a backup of the entire database
            generate_backup()
            input("\n Press enter to go back to the main menu ")
            time.sleep(3)

        elif choice == "e":
            # Exit
            print("Goodbye! ")
            exit()

        else:
            input("""\rPlease choose one of the options above.
                  \ra letter from the following (v/a/b/e)
                  \rPress enter to try again """)


"""
['product_name', 'product_price', 'product_quantity', 'date_updated']
['Bagel - Whole White Sesame', '$4.30', '97', '11/1/2018']
['Sauce - Caesar Dressing', '$8.05', '81', '12/28/2018']
['Shiratamako - Rice Flour', '$7.99', '71', '3/7/2018']


ValueError: invalid literal for int() with base 10: 'date_updated'

Step 12 
Displaying a product by its ID - Menu Option V
Create a function to handle getting and displaying a product by its product_id.


Code from websites
https://stackoverflow.com/questions/6750017/how-to-query-database-by-id-using-sqlalchemy


Step 14
Backup the database (Export new CSV) - Menu Option B
Create a function to handle making a backup of the database. The backup should be written to a .csv file.


"""



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv() # we add the csv values to the database
    app() # we use this to test the functionality of our app

    #add_csv() # we add the csv values to the database

    #clean_date("7/26/2018")  # used this line to test the split function for the date data
    #clean_price("$7.99")   # we test the clean_price function, as well as the split function in it

    for product in session.query(Product): # we loop through all of our books to make sure they have been added to the database
        print(product)


