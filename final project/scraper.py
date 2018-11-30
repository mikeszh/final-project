# import libraries

from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
from fractions import Fraction
from urllib.parse import urlencode


def scrape():
    # open the csv file
    with open('index.csv', 'a') as csv_file:
        # create the writer
        writer = csv.writer(csv_file)
        # create a new array where we will store the items
        items = []
        # We want to iterate over three links: breakfast, lunch and dinner
        for i in range(3):
            # Per the huds URL design, i=0 is breakfast, i=1 is lunch, i=2 is dinner
            meal_page = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=30&meal='+str(i)

            # Query the link and return the html for the ‘page’
            page = urlopen(meal_page)

            # prase "page" into beautiful soup format
            soup = BeautifulSoup(page, 'html.parser')

            # Take out the <div> of name and get its value

            # Add a new array per meal type to group all the breakfast items together, lunch items together, dinner items together
            items.append([])
            # Loops through all instances of div as all the items have div's around them. All the divs have class="item_wrap"
            for wrapper in soup.find_all('div', attrs={'class': 'item_wrap'}):

                # Get link as a string
                link = wrapper.span.a.get('href')

                # Open the food page
                food_page = urlopen(link)
                # Turn into beautiful soup object

                nutrition_data = BeautifulSoup(food_page, 'html.parser')
                # Get the item name and strip off html tags
                item_name = nutrition_data.find('span', attrs={'class': 'sub_title'}).text.strip()
                # We use try except clause because some of the items have "no data"
                try:
                    # Returns a list with three elements for the three categories: "nutrition facts", "amount/serving", "% daily value"
                    nutrition_table = nutrition_data.find('tr', attrs={'class': 'three_column'}).find_all('td')

                    # We first look at the left most column which is nutriton facts

                    nutrition_facts = nutrition_table[0].p.text.split('\n')
                    # gets to the right of </b> and left of &nbsp

                    serving_size = float(Fraction(nutrition_facts[1].split(': ')[1].split('\xa0')[0]))
                    calories = int(nutrition_facts[2].split(': ')[1])
                    calories_from_fat = int(nutrition_facts[3].split(': ')[1])

                    # We move to the amount_servings column
                    amount_serving = nutrition_table[1].p.text.split('\n')

                    total_fat = float(amount_serving[1].split(': ')[1].split(' ')[0])
                    cholesterol = float(amount_serving[4].split(': ')[1].split(' ')[0])
                    sodium = float(amount_serving[5].split(': ')[1].split(' ')[0])
                    protein = float(amount_serving[9].split(': ')[1].split(' ')[0])

                    # open a csv file with append, so old data will not be erased
                    writer.writerow([item_name, i, serving_size, calories, calories_from_fat, total_fat, cholesterol, sodium, protein])
                except:
                    print ("invalid data")
        # Go through "Basic food offerings": snacks / drinks, etc
        # This does not change on daily. General link: http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=16&meal=0
        meal_page = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date=11-27-2018&type=16'


        # Query the link and return the html for the ‘page’
        page = urlopen(meal_page)

        # prase "page" into beautiful soup format
        soup = BeautifulSoup(page, 'html.parser')

        # Take out the <div> of name and get its value

        # Add a new array per meal type to group all the breakfast items together, lunch items together, dinner items together
        items.append([])
        # Loops through all instances of div as all the items have div's around them. All the divs have class="item_wrap"
        for wrapper in soup.find_all('div', attrs={'class': 'item_wrap'}):

            # Get link as a string
            link = wrapper.span.a.get('href')

            # Open the food page
            food_page = urlopen(link.replace(' ', '%20'))

            # Turn into beautiful soup object

            nutrition_data = BeautifulSoup(food_page, 'html.parser')
            # Get the item name and strip off html tags
            item_name = nutrition_data.find('span', attrs={'class': 'sub_title'}).text.strip()
            # We use try except clause because some of the items have "no data"
            try:
                # Returns a list with three elements for the three categories: "nutrition facts", "amount/serving", "% daily value"
                nutrition_table = nutrition_data.find('tr', attrs={'class': 'three_column'}).find_all('td')

                # We first look at the left most column which is nutriton facts

                nutrition_facts = nutrition_table[0].p.text.split('\n')
                # gets to the right of </b> and left of &nbsp

                serving_size = float (Fraction (nutrition_facts[1].split(': ')[1].split('\xa0')[0]))
                calories = int (nutrition_facts[2].split(': ')[1])
                calories_from_fat = int(nutrition_facts[3].split(': ')[1])

                # We move to the amount_servings column
                amount_serving = nutrition_table[1].p.text.split('\n')

                total_fat = float(amount_serving[1].split(': ')[1].split(' ')[0])
                saturated_fat = float(amount_serving[2].split(': ')[1].split(' ')[0])

                trans_fat = float(amount_serving[3].split(': ')[1].split(' ')[0])
                cholesterol = float(amount_serving[4].split(': ')[1].split(' ')[0])
                sodium = float(amount_serving[5].split(': ')[1].split(' ')[0])
                total_carbs = float(amount_serving[6].split(': ')[1].split(' ')[0])
                dietary_fiber = float(amount_serving[7].split(': ')[1].split(' ')[0])
                sugars = float(amount_serving[8].split(': ')[1].split(' ')[0])
                protein = float(amount_serving[9].split(': ')[1].split(' ')[0])



                # open a csv file with append, so old data will not be erased


                writer.writerow([item_name, 3, serving_size, calories, calories_from_fat, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbs, dietary_fiber, sugars, protein])
            except:
                print ("invalid data")





if __name__ == "__main__":
    scrape()