import pandas as pd
from pandas.testing import assert_frame_equal
recipeFilter = __import__('hf_bi_python_excercise.recipes-etl.recipeFilter', fromlist=['hf_bi_python_excercise','recipes-etl','recipeFilter'])
recipeFilter=recipeFilter.RecipeFilter
import pytest
import os 
from unittest.mock import patch
base_path="hf_bi_python_excercise/tests/"

class TestRecipeFilter:
    def test_constructor(self):
        """ 
        Testing the constructor for the RecipeFilter object.
        This also covers the ingredient_filter as it is internally called in the constructor
        """

        dummy_json= open(f"{base_path}dummy_json.json", 'rb').read()
        
        # Initialising the Object
        result = recipeFilter(dummy_json,"chilies")

        # Checking the stemmed filter ingredient value
        assert result.filter_ingredient_stemmed == "chili"
        
        # Reading the desired output file
        ideal_result=pd.read_csv(f"{base_path}dummy_df.csv", sep="|")

        # Resetting index to avoid index issues during assert
        result.recipe_df.reset_index(drop=True, inplace=True)
        assert_frame_equal(result.recipe_df,ideal_result )

    def test_parse_total_time(self):
        """
        Testing the parse_total_time function.
        The expected output is the sum of the prepTime and cookTime of the 1 recipe
        that is filtered in the dummy test data (15 mins)
        """
        dummy_json= open(f"{base_path}dummy_json.json", 'rb').read()
        result = recipeFilter(dummy_json,"chilies")
        result.parse_total_time()
        result.recipe_df.reset_index(drop=True, inplace=True)
        assert result.recipe_df.loc[0, "totalTime_mins"] == 15
        
    def test_rate_difficulty(self):
        """
        Testing the difficulty rating of the one recipe that is filtered in the dummy test data
        Also checking is label is correct with various threshold value changes for the 
        difficulty rating.
        """
        dummy_json= open(f"{base_path}dummy_json.json", 'rb').read()
        result = recipeFilter(dummy_json,"chilies")
        result.parse_total_time()

        # Checking lables on threshold for case 1
        result.rate_difficulty(hard_cutoff=60, medium_cutoff=30, missing_label="Unknown")
        result.recipe_df.reset_index(drop=True, inplace=True)
        assert result.recipe_df.loc[0, "difficulty"] == "Easy"

        # Checking lables on threshold for case 2
        result.rate_difficulty(hard_cutoff=20, medium_cutoff=10, missing_label="Unknown")
        result.recipe_df.reset_index(drop=True, inplace=True)
        assert result.recipe_df.loc[0, "difficulty"] == "Medium"

        # Checking lables on threshold for case 3
        result.rate_difficulty(hard_cutoff=10, medium_cutoff=5, missing_label="Unknown")
        result.recipe_df.reset_index(drop=True, inplace=True)
        assert result.recipe_df.loc[0, "difficulty"] == "Hard"

    def test_save_metrics(self):
        """
        Calculating the metrics (average of total time) of the filtered recipe
        """
        dummy_json= open(f"{base_path}dummy_json.json", 'rb').read()
        result = recipeFilter(dummy_json,"chilies")
        result.parse_total_time()
        result.rate_difficulty(hard_cutoff=60, medium_cutoff=30, missing_label="Unknown")

        result.save_metrics("tester")
        
        # Reading the saved output file
        output=pd.read_csv(f"tester.csv", sep="|", header=None)
        
        # Deleting the file created during testing
        os.remove(f"tester.csv")
        assert output.iloc[0,2] == 15.0
        assert output.iloc[0,0] == "Easy"
        
