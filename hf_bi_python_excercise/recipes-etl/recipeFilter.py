from thefuzz import fuzz
from nltk.stem import PorterStemmer
from .utils import GeneralUtils

# BASE_PATH="hf_bi_python_excercise/tests/"

class RecipeFilter:
    """
        A class for Recipies to be filtered and labelled.
    """

    def __init__(self, all_recipies, filter_ingredient):
        """
            The constructor for the RecipeFilter class.
            Defines basic common variables used across the class

            Args:
                all_recipies (Byte): the byte data representing the recipes to be made into a DataFrame
                filter_ingredient (string): a string filter parameter on the ingredients field on which 
                                            the DataFrame of recipes will be filtered

        """


        self.recipe_df = GeneralUtils.make_dataframe(all_recipies)
        # Stemming the search ingredient to handle plural vs singular cases
        stemmer = PorterStemmer()
        self.filter_ingredient_stemmed = ' '.join([stemmer.stem(word) for word in filter_ingredient.split()])
        
        # calling the internal function to search for the given ingredient
        self.recipe_df=self.recipe_df[self.recipe_df.apply(lambda x: self.__ingredient_search(x['ingredients']),
                                                            axis=1)]

    def __ingredient_search(self, ingredients):
        """
            A function that looks for the specified filter ingredient in a recipe.
            Both the filter and the ingredient list is stemmed to allow for plurals.
            The the search is based on a fuzzy similarity, with a threshold of 80% match

            Args:
                ingredients (string): the full list of ingredients in the recipe

        """

        stemmer = PorterStemmer()
        ingredients=ingredients.lower().replace('\n',' ')
        
        # Stemming all the word sin the list of ingredients to match for singluar as well as plural words
        stemmed_ingredients = ' '.join([stemmer.stem(word) for word in ingredients.split()])
        
        # Matching using fuzzy match to determins similarity between words
        similarity_score = fuzz.partial_ratio(self.filter_ingredient_stemmed, stemmed_ingredients)
        
        # The threshold can be adjusted as needed 
        threshold = 85  
        if similarity_score >= threshold:
            return True
        else:
            return False
    
    def parse_total_time(self):
        """
            Parse the given prepTime and cookTime of a recipe into totalTime in minutes
            NOTE: prepTime and cookTime are in PTxxHxxM format, each component being optional.

            Args:
                -
        """

        self.recipe_df["prepTime_mins"]=self.recipe_df["prepTime"].apply(GeneralUtils.extract_mins)
        self.recipe_df["cookTime_mins"]=self.recipe_df["cookTime"].apply(GeneralUtils.extract_mins)

        self.recipe_df["totalTime_mins"]=self.recipe_df["prepTime_mins"] + self.recipe_df["cookTime_mins"]
        
        # Dropping the temporary columns created for total time calculation
        self.recipe_df.drop(columns=["prepTime_mins", "cookTime_mins"], inplace=True)

    def rate_difficulty(self, hard_cutoff, medium_cutoff, missing_label):
        """
            Rate the difficulty level of the recipe based on the total time it takes.
            
            Args:
                hard_cutoff (int): threshold in minutes for the Hard label
                medium_cutoff (int): threshold in minutes for the Medium label
                missing_label (int): label for invalid total time, i.e 0 mins or other values

        """

        # Labelling all filtered recipes using the apply function to ma the function to every row of the DataFrame
        self.recipe_df["difficulty"] = self.recipe_df["totalTime_mins"].apply(\
            lambda x: GeneralUtils.difficulty_label(x,
                                                     hard_cutoff=hard_cutoff, 
                                                     medium_cutoff=medium_cutoff, 
                                                     missing_label=missing_label)
                                                    )
    
    def save_recipes(self, file_name):
        """
            Save the filters and labelled recipes.
            
            Args:
                file_name (string): name of the file to save the data.

        """

        self.recipe_df.drop_duplicates(inplace=True)
        self.recipe_df.to_csv(f'{file_name}.csv',
                               sep='|',
                               index=False,
                               columns=list(set(self.recipe_df.columns)-set(['totalTime_mins']))
                            )

    def save_metrics(self, file_name):
        """
            Calculate and save the average time of each ddifficulty of recipe.
            
            Args:
                file_name (string): name of the file to save the data.

        """
        # Grouping the recipes based on difficulty and find the mean totalTime_mins
        metric_df = self.recipe_df[self.recipe_df['difficulty'].isin(['Easy','Medium','Hard'])]\
                            .groupby('difficulty').agg({'totalTime_mins':'mean'})
        metric_df['_']='AverageTotalTime'

        # Rounding all values to 2 decimal points
        metric_df['totalTime_mins']= metric_df['totalTime_mins'].round(2)

        # Reset index allows for the reset after the groupby operation
        metric_df.reset_index(drop=False, inplace=True)
        metric_df[['difficulty','_','totalTime_mins']].to_csv(f'{file_name}.csv', index=False, header=False, sep='|')
