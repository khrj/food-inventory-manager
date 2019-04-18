import os
import pickle
import time

remaining_ingredients = {}
dishes = []


class Dish:
    name = ""
    required_ingredients = {}

    def __init__(self, name: str, required_ingredients: dict):
        self.required_ingredients = required_ingredients
        self.name = name

    def add_ingredient(self, name, amount):
        self.required_ingredients[name] = amount

    def remove_ingredient(self, to_delete):
        del self.required_ingredients[to_delete]

    def cook_dish(self):
        global remaining_ingredients
        remaining_ingredients_backup = remaining_ingredients.copy()
        for name, amount in self.required_ingredients.items():
            if remaining_ingredients[name] >= amount:
                remaining_ingredients[name] -= amount
            else:
                print(f"Dish requires more of ingredient {name}.\nYou currently have - {remaining_ingredients[name]}\n"
                      f"Required - {amount}\nTry again.")
                remaining_ingredients = remaining_ingredients_backup
                time.sleep(1)
                return
        print("Successfully removed ingredients required by the dish from inventory")
        time.sleep(1)
        return


# Save and load functions for remaining ingredients and dishes

def save_obj(obj, name):
    current_directory_is = os.getcwd()
    final_directory_is = os.path.join(current_directory_is, r'FoodMonitor')
    if not os.path.exists(final_directory_is):
        os.makedirs(final_directory_is)

    with open('FoodMonitor/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('FoodMonitor/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# Standard multi choice question template
def multi_choice_question(options: list):
    while True:
        print("Enter the number of your choice -",
              *(f"{number}. {option}" for number, option in enumerate(options, 1)),
              sep='\n', end='\n\n')
        '''
        The same as - 
           print("\nEnter the number of your choice - ")
        for i, option in enumerate(options, 1):
            print('{0}. {1}'.format(i, option))
        print("\n"")        
        '''
        try:
            answer = int(input())
            if 1 <= answer <= len(options):
                return answer
            print("That option does not exist! Try again!")
        except ValueError:
            print("Doesn't seem like a number! Try again!")


# For getting an int from the user'
def get_int():
    while True:
        try:
            return int(input())
        except ValueError:
            print("Doesn't seem like a number! Try again!")


''' UI methods - For direct interaction with the user'''


def buy_ingredients():
    if len(remaining_ingredients) != 0:
        print("Which ingredient did you buy?\n")
        multi_choice_params = []
        for name, amount in remaining_ingredients.items():
            multi_choice_params.append(name)
        ingredient_name = multi_choice_params[multi_choice_question(multi_choice_params) - 1]
        print("How much did you buy?")
        ingredient_amount = get_int()
        remaining_ingredients[ingredient_name] += ingredient_amount
        print("Successfully updated ingredient library")
    else:
        print("No ingredients yet! Use option 4 to add new ingredients.")

    time.sleep(1)


def cook_dish():
    if len(dishes) != 0:
        print("Which dish would you like to cook?")
        dish_names = []
        for dish in dishes:
            dish_names.append(dish.name)
        answer = multi_choice_question(dish_names)
        Dish.cook_dish(dishes[answer - 1])
    else:
        print("No dishes yet! Use option 3 to create new dish templates")


def edit_dish():
    def new_dish():
        if len(remaining_ingredients) != 0:
            while True:
                name_of_dish = input("What will the name of the dish be?").lower().strip()
                if name_of_dish not in dishes:
                    break
                print("That dish already exists! Try again!")

            print("How many ingredients will the dish contain?")
            amount = get_int()
            list_of_ingredients = {}

            # get ingredients
            print("Enter all your ingredients:")
            for x in range(amount):
                # check if ingredient exists
                while True:
                    s = input(f"No. {x + 1}. -----> ").lower().strip()
                    if s in remaining_ingredients:
                        name_of_ingredient = s
                        break
                    else:
                        print("That ingredient doesn't exist! Try again!")

                print("How much of that ingredient will the dish use?")
                amount = get_int()
                list_of_ingredients[name_of_ingredient] = amount
            dishes.append(Dish(name_of_dish, list_of_ingredients))
        else:
            print("No ingredients yet! Use option 4 to add new ingredients for use in this dish.")

    def remove_dish():
        if len(dishes) != 0:
            print("Which dish would you like to delete?")
            dish_names = []
            for dish in dishes:
                dish_names.append(dish.name)

            to_delete = multi_choice_question(dish_names) - 1
            to_delete_name = dishes[to_delete].name
            del dishes[to_delete]
            print(f"Successfully deleted dish {to_delete_name}")
        else:
            print("No dishes yet! Use option 3 to add new ingredients.")

    def modify_dish():
        global dishes
        if len(dishes) != 0:
            print("Which dish would you like to modify?")
            dish_names = []
            for dish in dishes:
                dish_names.append(dish.name)
            to_modify = multi_choice_question(dish_names)

            print(f"What would you like to modify about this dish?")
            thing_to_modify = multi_choice_question(
                ["Name", "Required ingredients", "Quantity of required ingredient(s)"])

            if thing_to_modify == 1:
                dishes[to_modify - 1].name = input("Enter new name: ").lower().strip()
                print("Successfully changed name!")

            elif thing_to_modify == 2:
                answer = multi_choice_question(["Add a new ingredient", "Remove an existing ingredient"])
                if answer == 1:
                    print("Which ingredient would you like to add to this dish?")
                    remaining_ingredient_names = list(remaining_ingredients.keys())
                    required_ingredients = list(dishes[to_modify - 1].required_ingredients.keys())
                    ingredients_not_used_in_dish = list(set(remaining_ingredient_names) - set(required_ingredients))
                    if len(ingredients_not_used_in_dish) != 0:
                        to_add = multi_choice_question(ingredients_not_used_in_dish)
                        print("How much of that ingredient will the dish require?")
                        amount_required = get_int()
                        dishes[to_modify - 1].add_ingredient(ingredients_not_used_in_dish[to_add - 1], amount_required)
                        print(f"Successfully added {ingredients_not_used_in_dish[to_add - 1]} "
                              f"to {dishes[to_modify - 1].name}")
                    else:
                        print("All ingredients in inventory are already used in dish")

                else:
                    print("Which ingredient would you like to remove from this dish?")
                    required_ingredient_names = list(dishes[to_modify - 1].required_ingredients.keys())
                    to_remove = multi_choice_question(required_ingredient_names)
                    dishes[to_modify - 1].remove_ingredient(required_ingredient_names[to_remove - 1])
                    print(f"Successfully removed {required_ingredient_names[to_remove - 1]} from "
                          f"{dishes[to_modify - 1].name}")

            else:
                print("Which ingredient's quantity would you like to change?")
                required_ingredient_names = list(dishes[to_modify - 1].required_ingredients.keys())
                to_change = multi_choice_question(required_ingredient_names)
                print("Enter the new quantity for the ingredient")
                quantity = get_int()
                dishes[to_modify - 1].required_ingredients[required_ingredient_names[to_change - 1]] = quantity
                print(
                    f"Successfully changed amount of {required_ingredient_names[to_change - 1]} required "
                    f"in {dishes[to_modify - 1].name} to {quantity}")
        else:
            print("No ingredients yet! Use option 3 to add new ingredients.")

    to_do = multi_choice_question(["Add a new dish",
                                   "Delete an existing dish",
                                   "Edit an existing dish",
                                   ])

    if to_do == 1:
        new_dish()
    elif to_do == 2:
        remove_dish()
    else:
        modify_dish()
    time.sleep(1)


def edit_ingredients():
    def new_ingredient():
        while True:
            name = input("What will the name of the new ingredient be?").lower().strip()
            if name in remaining_ingredients:
                print("Ingredient already exists! Try again!")
                continue
            break

        print("How much of this ingredient do you currently have?")
        amount = get_int()
        remaining_ingredients[name] = amount
        print(f"Successfully added {name}")

    def remove_ingredient():
        if len(remaining_ingredients) != 0:
            print("Which ingredient do you want to delete?")
            to_remove = multi_choice_question(list(remaining_ingredients.keys()))
            removed = list(remaining_ingredients.keys())[to_remove - 1]
            del remaining_ingredients[removed]
            print(f"Successfully deleted {removed}")
        else:
            print("No ingredients yet! Use option 4 to add new ingredients.")

    def edit_ingredient_quantity():
        if len(remaining_ingredients) != 0:
            print("Which ingredient's amount do you want to change?")
            to_change = multi_choice_question(list(remaining_ingredients.keys()))
            print("What will the new amount of the ingredient?")
            new_value = get_int()
            remaining_ingredients[list(remaining_ingredients.keys())[to_change - 1]] = new_value
            print(f"Success! {list(remaining_ingredients.keys())[to_change - 1]} now has value {new_value}")
        else:
            print("No ingredients yet! Use option 4 to add new ingredients.")

    to_do = multi_choice_question(
        ["Add a new ingredient", "Remove an existing ingredient", "Edit the amount of an existing ingredient"])

    if to_do == 1:
        new_ingredient()
    elif to_do == 2:
        remove_ingredient()
    else:
        edit_ingredient_quantity()
    time.sleep(1)


def get_ingredients():
    print("Current Ingredient Inventory:\n")
    if len(remaining_ingredients) == 0:
        print("No ingredients yet!\n")
    else:
        for name, amount in remaining_ingredients.items():
            print(f"{name} : {amount}")
    time.sleep(1)


def get_dishes():
    print("Current Dishes:\n")
    if len(dishes) == 0:
        print("No dishes yet!\n")
    for x in dishes:
        print(f"{x.name}, containing ", end="")
        print(str(x.required_ingredients)[1:-1])
    time.sleep(1)


current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'FoodMonitor')
if os.path.exists(final_directory):
    remaining_ingredients = load_obj("I")
    dishes = load_obj("D")
while True:
    choice = multi_choice_question(
        ["If you bought ingredients, choose option 1. ", "If you cooked a dish choose option 2. ",
         "To add a new dish or edit/delete an existing one, choose option 3. ",
         "To add a new ingredient or edit/delete an existing one, choose option 4. ",
         "To view current ingredient inventory, choose option 5",
         "To view current dishes, choose option 6",
         "To save inventory and quit the application, choose option 7. "])

    if choice == 1:
        buy_ingredients()

    if choice == 2:
        cook_dish()

    if choice == 3:
        edit_dish()

    if choice == 4:
        edit_ingredients()

    if choice == 5:
        get_ingredients()

    if choice == 6:
        get_dishes()

    if choice == 7:
        print("See you next time...")
        save_obj(remaining_ingredients, "I")
        save_obj(dishes, "D")
        exit(0)
