from final_proj import *
import unittest
import sqlite3

class TestRestaurantSearch(unittest.TestCase):
    def setUp(self):
        self.ann_arbor_name = []
        self.chicago_name = []
        self.lansing_name = []
        self.milwaukee_name = []
        self.ann_arbor_dict = get_city_restaurant('Ann Arbor,MI','food',50)['businesses']
        self.chicago_dict = get_city_restaurant('Chicago,IL','food',50)['businesses']
        self.lansing_dict  = get_city_restaurant('LANSING,MI','food',50)['businesses']
        self.milwaukee_dict = get_city_restaurant('MILWAUKEE,WI','food',50)['businesses']
        self.milwaukee_weather = get_city_weather('milwaukee')
        for i in self.ann_arbor_dict:
            self.ann_arbor_name.append(i['name'])
        for i in self.chicago_dict:
            self.chicago_name.append(i['name'])
        for i in self.lansing_dict:
            self.lansing_name.append(i['name'])

    def test_basic_search(self):
        self.assertEqual(len(self.ann_arbor_dict), 50)
        self.assertEqual(len(self.chicago_dict), 50)
        self.assertEqual(len(self.lansing_dict), 50)
        self.assertEqual(len(self.milwaukee_dict), 50)
        self.assertIn('RoosRoast Coffee',self.ann_arbor_name)
        self.assertIn('Girl & the Goat',self.chicago_name)
        self.assertEqual(self.milwaukee_weather['name'],'Milwaukee')


class Testdatabase(unittest.TestCase):

    def testRestaurant(self):
        try:
            conn = sqlite3.connect('restaurant_info.db')
            cur = conn.cursor()
        except:
            return False

        sql1 = '''
        SELECT COUNT(*), Name, category1
        FROM Restaurants Where city == "ANN ARBOR"
        '''
        results1 = cur.execute(sql1)
        result_list1 = results1.fetchall()

        sql2 = '''
        SELECT COUNT(*), Name, category1
        FROM Restaurants Where city == "LANSING"
        '''
        results2 = cur.execute(sql2)
        result_list2 = results2.fetchall()

        sql3 = '''
        SELECT Name
        FROM Restaurants
        '''
        results3 = cur.execute(sql3)
        result_list3 = results3.fetchall()

        sql4 = '''
        SELECT *
        FROM Weather WHERE Name == "MILWAUKEE"
        '''
        results4 = cur.execute(sql4)
        result_list4 = results4.fetchall()

        self.assertGreater(result_list1[0][0], 1)
        self.assertIs(type(result_list1[0][1]), str)
        self.assertIs(type(result_list1[0][2]), str)
        self.assertGreater(result_list2[0][0], 1)
        self.assertIs(type(result_list2[0][1]), str)
        self.assertIs(type(result_list2[0][2]), str)
        self.assertIn(('Jolly Pumpkin Café & Brewery',), result_list3)
        self.assertIn(("Homes Brewery",), result_list3)
        self.assertEqual(len(result_list4[0]), 11)
        self.assertIs(type(result_list4[0][9]),float)

class TestMapping(unittest.TestCase):

    # we can't test to see if the maps are correct, but we can test that
    # the functions don't return an error!
    def test_show_resraurant_map(self):
        response1 ="ANN ARBOR, MI"
        category1 ="food"
        try:
            restaurant_location_query(response1,category1)
            plot_restaurant_site_offline(response1)
        except:
            self.fail()
        response2 ="Chicago, IL"
        category2 ="food"
        try:
            restaurant_location_query(response2,category2)
            plot_restaurant_site_offline(response2)
        except:
            self.fail()


if __name__ == '__main__':
    insert_db()
    insert_db()
    unittest.main()
