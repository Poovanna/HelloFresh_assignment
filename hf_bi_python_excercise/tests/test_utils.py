import pytest
import pandas as pd
from unittest.mock import patch

# using __import__ to support module name with - (hyphen symbol)
GeneralUtils = __import__('hf_bi_python_excercise.recipes-etl.utils', fromlist=['hf_bi_python_excercise','recipes-etl','utils'])
GeneralUtils=GeneralUtils.GeneralUtils

class TestGeneralUtils:
    @pytest.mark.parametrize("input_str, expected_output", [
        ("PT12H30M", 750),
        ("PT8H", 480),
        ("PT55M", 55),
        ("pt3h45m", 225),
        ("PT", 0),
        ("InvalidFormat", 0)
    ])
    def test_extract_mins(self, input_str, expected_output):
        """
        Testing the various possible inputs to the time parisng function.
        """
        result = GeneralUtils.extract_mins(input_str)
        assert result == expected_output
        
    @patch("requests.get")
    def test_file_fetch(self, mock_get):
        # Mocking the requests.get().content 
        mock_get.return_value.content = b"""
                                            {"name": "Easter Leftover Sandwich", "ingredients": "12 whole Hard Boiled Eggs\n1/2 cup Mayonnaise\n3 Tablespoons Grainy Dijon Mustard\n Salt And Pepper, to taste\n Several Dashes Worcestershire Sauce\n Leftover Baked Ham, Sliced\n Kaiser Rolls Or Other Bread\n Extra Mayonnaise And Dijon, For Spreading\n Swiss Cheese Or Other Cheese Slices\n Thinly Sliced Red Onion\n Avocado Slices\n Sliced Tomatoes\n Lettuce, Spinach, Or Arugula", "url": "http://thepioneerwoman.com/cooking/2013/04/easter-leftover-sandwich/", "image": "http://static.thepioneerwoman.com/cooking/files/2013/03/leftoversandwich.jpg", "cookTime": "PT", "recipeYield": "8", "datePublished": "2013-04-01", "prepTime": "PT15M", "description": "Got leftover Easter eggs?    Got leftover Easter ham?    Got a hearty appetite?    Good! You've come to the right place!    I..."}
                                            {"name": "Pasta with Pesto Cream Sauce", "ingredients": "3/4 cups Fresh Basil Leaves\n1/2 cup Grated Parmesan Cheese\n3 Tablespoons Pine Nuts\n2 cloves Garlic, Peeled\n Salt And Pepper, to taste\n1/3 cup Extra Virgin Olive Oil\n1/2 cup Heavy Cream\n2 Tablespoons Butter\n1/4 cup Grated Parmesan (additional)\n12 ounces, weight Pasta (cavitappi, Fusili, Etc.)\n2 whole Tomatoes, Diced", "url": "http://thepioneerwoman.com/cooking/2011/06/pasta-with-pesto-cream-sauce/", "image": "http://static.thepioneerwoman.com/cooking/files/2011/06/pesto.jpg", "cookTime": "PT10M", "recipeYield": "8", "datePublished": "2011-06-06", "prepTime": "PT6M", "description": "I finally have basil in my garden. Basil I can use. This is a huge development.     I had no basil during the winter. None. G..."}
                                            {"name": "Herb Roasted Pork Tenderloin with Preserves", "ingredients": "2 whole Pork Tenderloins\n Salt And Pepper, to taste\n8 Tablespoons Herbs De Provence (more If Needed\n1 cup Preserves (fig, Peach, Plum)\n1 cup Water\n1 Tablespoon Vinegar", "url": "http://thepioneerwoman.com/cooking/2011/09/herb-roasted-pork-tenderloin-with-preserves/", "image": "http://static.thepioneerwoman.com/cooking/files/2011/09/porkloin.jpg", "cookTime": "PT15M", "recipeYield": "12", "datePublished": "2011-09-15", "prepTime": "PT5M", "description": "This was yummy. And easy. And pretty! And it took basically no time to make.     Before I share the recipe, I'll just say it:..."}
                                         """
        
        result = GeneralUtils.file_fetch("<file_url>")  
        assert result ==  mock_get.return_value.content 
        
    def test_make_dataframe(self):
        """
        Testing the byte data to dataframe conversion
        """

        # passing a valid json line data
        data=b"""
                 {"name": "Easter Leftover Sandwich", "ingredients": "12 whole Hard Boiled Eggs\n1/2 cup Mayonnaise\n3 Tablespoons Grainy Dijon Mustard\n Salt And Pepper, to taste\n Several Dashes Worcestershire Sauce\n Leftover Baked Ham, Sliced\n Kaiser Rolls Or Other Bread\n Extra Mayonnaise And Dijon, For Spreading\n Swiss Cheese Or Other Cheese Slices\n Thinly Sliced Red Onion\n Avocado Slices\n Sliced Tomatoes\n Lettuce, Spinach, Or Arugula", "url": "http://thepioneerwoman.com/cooking/2013/04/easter-leftover-sandwich/", "image": "http://static.thepioneerwoman.com/cooking/files/2013/03/leftoversandwich.jpg", "cookTime": "PT", "recipeYield": "8", "datePublished": "2013-04-01", "prepTime": "PT15M", "description": "Got leftover Easter eggs?    Got leftover Easter ham?    Got a hearty appetite?    Good! You've come to the right place!    I..."}
                 {"name": "Pasta with Pesto Cream Sauce", "ingredients": "3/4 cups Fresh Basil Leaves\n1/2 cup Grated Parmesan Cheese\n3 Tablespoons Pine Nuts\n2 cloves Garlic, Peeled\n Salt And Pepper, to taste\n1/3 cup Extra Virgin Olive Oil\n1/2 cup Heavy Cream\n2 Tablespoons Butter\n1/4 cup Grated Parmesan (additional)\n12 ounces, weight Pasta (cavitappi, Fusili, Etc.)\n2 whole Tomatoes, Diced", "url": "http://thepioneerwoman.com/cooking/2011/06/pasta-with-pesto-cream-sauce/", "image": "http://static.thepioneerwoman.com/cooking/files/2011/06/pesto.jpg", "cookTime": "PT10M", "recipeYield": "8", "datePublished": "2011-06-06", "prepTime": "PT6M", "description": "I finally have basil in my garden. Basil I can use. This is a huge development.     I had no basil during the winter. None. G..."}
                 {"name": "Herb Roasted Pork Tenderloin with Preserves", "ingredients": "2 whole Pork Tenderloins\n Salt And Pepper, to taste\n8 Tablespoons Herbs De Provence (more If Needed\n1 cup Preserves (fig, Peach, Plum)\n1 cup Water\n1 Tablespoon Vinegar", "url": "http://thepioneerwoman.com/cooking/2011/09/herb-roasted-pork-tenderloin-with-preserves/", "image": "http://static.thepioneerwoman.com/cooking/files/2011/09/porkloin.jpg", "cookTime": "PT15M", "recipeYield": "12", "datePublished": "2011-09-15", "prepTime": "PT5M", "description": "This was yummy. And easy. And pretty! And it took basically no time to make.     Before I share the recipe, I'll just say it:..."}
              """
        valid_result = GeneralUtils.make_dataframe(data)
        assert type(valid_result)==pd.DataFrame

        # passing an incomplete/invalid json data
        data =b"""
                 {"name": "Easter Leftover Sandwich",
                """ 
        invalid_result = GeneralUtils.make_dataframe(data)
        assert type(invalid_result)==type(None)



    @pytest.mark.parametrize("total_time, hard_cutoff, medium_cutoff, missing_label, expected_output", [
        (67, 60, 30,"Unknown","Hard"),
        (40, 60, 30,"Unknown","Medium"),
        (12, 60, 30,"Unknown","Easy"),
        (0, 60, 30,"Unknown","Unknown"),
        (-34, 60, 30,"Invalid","Invalid"),
        (90, 120, 60,"Unknown","Medium"),
        (40, 60, 45,"Unknown","Easy"),
    ])
    def test_difficulty_label(self, total_time, hard_cutoff, medium_cutoff, missing_label,expected_output):
        """
        Passing various values with different thresholds to check the difficulty labelling function
        """
        result = GeneralUtils.difficulty_label(total_time, hard_cutoff, medium_cutoff, missing_label)
        assert result == expected_output
