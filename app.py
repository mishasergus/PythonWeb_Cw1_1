import json
import random


class Table:
    def __init__(self, number, seats):
        self.number = number
        self.seats = seats
        self.is_busy = False
    def __str__(self):
        return f"Table {self.number} | Seats: {self.seats} | {'Busy' if self.is_busy else 'Available'}"
    def occupy(self):
        if self.is_busy:
            raise Exception(f"Table {self.number} is already occupied.")
        self.is_busy = True
    def free(self):
        if not self.is_busy:
            raise Exception(f"Table {self.number} is already free.")
        self.is_busy = False
    

class Dish:
    def __init__(self, name, price, status="default"):
        self.name = name
        self.price = price
        self.status = status
        if self.status == "popular":
            self.price *= 0.8
    def __str__(self):
        return f"{self.name} | {self.price} UAH {'⭐' if self.status == 'popular' else ''}"
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        if value not in ["default", "popular"]:
            raise ValueError("Status must be 'default' or 'popular'")
        prev_status = getattr(self, "_status", None)
        self._status = value
        if prev_status != "popular" and self._status == "popular":
            self.price *= 0.8
        elif prev_status == "popular" and self._status == "default":
            self.price /= 0.8
    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Dish name cannot be empty")
        self._name = value

class MainDish(Dish):
    def __init__(self, name, price, weight_g, status="default"):
        super().__init__(name, price, status)
        self.weight_g = weight_g
    def __str__(self):
        return f"{self.name} | {self.price} UAH | main dish | {self.weight_g}g {'⭐' if self.status == 'popular' else ''}"
    @property
    def weight_g(self):
        return self._weight_g
    @weight_g.setter
    def weight_g(self, value):
        if value <= 0:
            raise ValueError("Weight must be positive")
        self._weight_g = value

class Drink(Dish):
    def __init__(self, name, price, volume_ml, status="default"):
        super().__init__(name, price, status)
        self.volume_ml = volume_ml
    def __str__(self):
        return f"{self.name} | {self.price} UAH | drink | {self.volume_ml}ml {'⭐' if self.status == 'popular' else ''}"
    @property
    def volume_ml(self):
        return self._volume_ml
    @volume_ml.setter
    def volume_ml(self, value):
        if value <= 0:
            raise ValueError("Volume must be positive")
        self._volume_ml = value

class Dessert(Dish):
    def __init__(self, name, price, calories, status="default"):
        super().__init__(name, price, status)
        self.calories = calories
    def __str__(self):
        return f"{self.name} | {self.price} UAH | dessert | {self.calories} kcal {'⭐' if self.status == 'popular' else ''}"
    @property
    def calories(self):
        return self._calories
    @calories.setter
    def calories(self, value):
        if value <= 0:
            raise ValueError("Calories must be positive")
        self._calories = value
    
    

class Restaurant:
    def __init__(self):
        self.dishes = [
            Dish("Суп з локшиною", 100),
            MainDish("Борщ", 120, 200),
            MainDish("Вареники з картоплею", 110, 150),
            MainDish("Деруни зі сметаною", 130, 180),
            Dish("Салат «Цезар»", 140),
            Drink("Узвар", 40, 250),
            Drink("Капучино", 55, 200),
            Dessert("Медовик", 90, 300),
            Dessert("Сирники", 95, 250),
        ]
        dish_of_the_day = self.dishes[random.randint(0, len(self.dishes) - 1)]
        dish_of_the_day.status = "popular"

        self.tables = [
            Table(2, 4),
            Table(3, 2),
            Table(4, 6),
            Table(5, 7),
        ]
    def menu(self, status_filter=None):
        if status_filter == "Dessert":
            return "".join(f"{dish}\n" for dish in self.dishes if isinstance(dish, Dessert))
        elif status_filter == "Drink":
            return "".join(f"{dish}\n" for dish in self.dishes if isinstance(dish, Drink))
        elif status_filter == "MainDish":
            return "".join(f"{dish}\n" for dish in self.dishes if isinstance(dish, MainDish))
        
        return "".join(f"{dish}\n" for dish in self.dishes)
    def add_dish(self, name, price, type):
        if type == "main":
            weight_g = float(input("Enter weight in grams: "))
            self.dishes.append(MainDish(name, price, weight_g))
        elif type == "drink":
            volume_ml = float(input("Enter volume in milliliters: "))
            self.dishes.append(Drink(name, price, volume_ml))
        elif type == "dessert":
            calories = float(input("Enter calories: "))
            self.dishes.append(Dessert(name, price, calories))
        else:
            self.dishes.append(Dish(name, price))
    def show_tables(self):
        return "".join(f"{table}\n" for table in self.tables)
    def book_table(self, guests):
        for table in self.tables:
            if not table.is_busy and table.seats >= guests:
                table.occupy()
                return table
        return None
    def dish_by_name(self, name):
        for dish in self.dishes:
            if dish.name == name:
                return dish
        return None
    def free(self, number):
        for table in self.tables:
            if table.number == number:
                table.free()
                return True
        return False

Restaurant_instance = Restaurant()
print(Restaurant_instance.menu())

def calculate_bill(ordered_dishes):
    suma = sum(dish.price for dish in ordered_dishes)
    if suma > 2000:
        suma *= 0.9
    elif suma > 1000:
        suma *= 0.95
    return suma

choice = None
current_table = None
ordered_dishes = []
reviews = []
while choice != 0:
    try:
        print("""
        1. Show menu
        2. Add dish
        3. Show tables
        4. Book table
        5. Take order
        6. Calculate bill
        7. Free table
        0. Exit""")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            print("1. All dishes")
            print("2. Main dishes")
            print("3. Desserts")
            print("4. Drinks")
            menu_choice = input("Enter your choice: ")
            if menu_choice == "1":
                print(Restaurant_instance.menu())
            elif menu_choice == "2":
                print(Restaurant_instance.menu(status_filter="MainDish"))
            elif menu_choice == "3":
                print(Restaurant_instance.menu(status_filter="Dessert"))
            elif menu_choice == "4":
                print(Restaurant_instance.menu(status_filter="Drink"))
        elif choice == 2:
            name = input("Enter dish name: ")
            price = float(input("Enter dish price: "))
            type = input("Enter dish type (starter/main/dessert/drink): ")
            Restaurant_instance.add_dish(name, price, type)
        elif choice == 3:
            print(Restaurant_instance.show_tables())
        elif choice == 4:
            guests = int(input("Enter number of guests: "))
            table = Restaurant_instance.book_table(guests)
            if table:
                current_table = table
                print(f"Table {table.number} booked successfully.")
            else:
                print("No available table for the given number of guests.")
        elif choice == 5:
            if current_table:
                while True:
                    dish_name = input("Enter dish name to order (or '0' to finish): ")
                    if dish_name == '0':
                        break
                    dish = Restaurant_instance.dish_by_name(dish_name)
                    if dish is not None:

                        ordered_dishes.append(dish)
                        print(f"Ordered {dish.name} for {dish.price} UAH.")
                        print(f"Current order: {[d.name for d in ordered_dishes]}")
                    else:
                        print("Dish not found in the menu.")
                if current_table.number % 5 == 0:
                    print("You get a free dessert for booking a table with a number divisible by 5!")
                    free_dessert = Dessert("Free Dessert", 0, 200)
                    ordered_dishes.append(free_dessert)
            else:
                print("Please book a table first.")
        elif choice == 6:
            if current_table:
                total = calculate_bill(ordered_dishes)
                print(f"Total bill for table {current_table.number}: {total} UAH.")
                review = float(input("Please leave a review (1-5): "))
                if 1 <= review <= 5:
                    reviews.append(review)
                    print("Thank you for your review!")
            else:
                print("Please book a table first.")
            
        elif choice == 7:
            if current_table:
                Restaurant_instance.free(current_table.number)
                print(f"Table {current_table.number} is now free.")
                current_table = None
                ordered_dishes = []
            else:
                print("No table is currently booked.")


    except Exception as e:
        print(f"An error occurred: {e}")

print(f"Average review score: {sum(reviews)/len(reviews) if reviews else 'No reviews yet.'}")