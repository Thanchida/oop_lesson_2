import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

players = []
with open(os.path.join(__location__, 'Players.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        players.append(dict(r))

teams = []
with open(os.path.join(__location__, 'Teams.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        teams.append(dict(r))

titanic = []
with open(os.path.join(__location__, 'Titanic.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        titanic.append(dict(r))


class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None



import copy


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
    
    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table
    
    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
                else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def pivot_table(self, keys_to_pivot_list, keys_to_aggregate_list, aggregate_func_list):


    def __str__(self):
        return self.table_name + ':' + str(self.table)


table1 = Table('players', players)
table2 = Table('teams', teams)
table4 = Table('titanic', titanic)
my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)
my_DB.insert(table4)
my_tb1 = my_DB.search('players')
my_tb2 = my_DB.search('teams')
table3 = my_tb1.join(my_tb2, 'team')
table3_filtered = table3.filter(lambda x: 'ai' in x['team'])\
    .filter(lambda x: int(x['minutes']) < 200)\
    .filter(lambda x: int(x['passes']) > 100)
table3_select = table3_filtered.select(['surname', 'team', 'position'])
print(table3_select)
table4_below = table3.filter(lambda x: int(x['ranking']) < 10).aggregate(lambda x: sum(x)/len(x),'games')
table4_above = table3.filter(lambda x: int(x['ranking']) >= 10).aggregate(lambda x: sum(x)/len(x),'games')
print('games below:', table4_below)
print('games above:', table4_above)

table4_for = table3.filter(lambda x: x['position'] == 'forward').aggregate(lambda x: sum(x)/len(x), 'passes')
table4_mid = table3.filter(lambda x: x['position'] == 'midfielder').aggregate(lambda x: sum(x)/len(x), 'passes')
print('passes forward:', table4_for)
print('passes midfielders:', table4_mid)

titanic_first = table4.filter(lambda x: int(x['class']) == 1).aggregate(lambda x: sum(x)/len(x), 'fare')
titanic_third = table4.filter(lambda x: int(x['class']) == 3).aggregate(lambda x: sum(x)/len(x), 'fare')
print('average fare in the first class:', titanic_first)
print('average fare in the third class:', titanic_third)

titanic_male = table4.filter(lambda x: x['gender'] == 'M')
titanic_male_survived = table4.filter(lambda x: x['gender'] == 'M')\
    .filter(lambda x: x['survived'] == 'yes')
titanic_female = table4.filter(lambda x: x['gender'] == 'F')
titanic_female_survived = table4.filter(lambda x: x['gender'] == 'F')\
    .filter(lambda x: x['survived'] == 'yes')
male = 0
male_survived = 0
female = 0
female_survived = 0
for j in titanic_male.table:
    male += 1
for i in titanic_male_survived.table:
    male_survived += 1
for m in titanic_female.table:
    female += 1
for n in titanic_female_survived.table:
    female_survived += 1
print(f'rate of survived male passengers: {male_survived/male}')
print(f'rate of survived female passenger: {female_survived/female}')
# table1 = Table('cities', cities)
# table2 = Table('countries', countries)
# table3 = Table('players', players)
# table4 = Table('teams', teams)
# table5 = Table('titanic', titanic)
# my_DB = DB()
# my_DB.insert(table1)
# my_DB.insert(table2)
# my_table1 = my_DB.search('cities')
# my_table3 = my_DB.search('players')
# # print(my_table3.table_name, my_table3.table)
#
#
# print("Test filter: only filtering out cities in Italy")
# my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
# print(my_table1_filtered)
# print()
#
# print("Test select: only displaying two fields, city and latitude, for cities in Italy")
# my_table1_selected = my_table1_filtered.select(['city', 'latitude'])
# print(my_table1_selected)
# print()
#
# print("Calculting the average temperature without using aggregate for cities in Italy")
# temps = []
# for item in my_table1_filtered.table:
#     temps.append(float(item['temperature']))
# print(sum(temps)/len(temps))
# print()
#
# print("Calculting the average temperature using aggregate for cities in Italy")
# print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
# print()
#
# print("Test join: finding cities in non-EU countries whose temperatures are below 5.0")
# my_table2 = my_DB.search('countries')
# my_table3 = my_table1.join(my_table2, 'country')
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
# print(my_table3_filtered.table)
# print()
# print("Selecting just three fields, city, country, and temperature")
# print(my_table3_filtered.select(['city', 'country', 'temperature']))
# print()
#
# print("Print the min and max temperatures for cities in EU that do not have coastlines")
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
# print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
# print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
# print()
#
# print("Print the min and max latitude for cities in every country")
# for item in my_table2.table:
#     my_table1_filtered = my_table1.filter(lambda x: x['country'] == item['country'])
#     if len(my_table1_filtered.table) >= 1:
#         print(item['country'], my_table1_filtered.aggregate(lambda x: min(x), 'latitude'), my_table1_filtered.aggregate(lambda x: max(x), 'latitude'))
# print()
#
