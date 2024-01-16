recipeFilter = __import__('recipes-etl.recipeFilter')
GeneralUtils = __import__('recipes-etl.utils')
 

if __name__=='__main__':
    # URL to access the file with recipe data
    url='https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json'

    # Fetching contents of the file from the url
    file_data = GeneralUtils.utils.GeneralUtils.file_fetch(url)

    # Initialising an instance of the RecipeFilter object
    recipes_obj =recipeFilter.recipeFilter.RecipeFilter(file_data, 'chilies')

    # Calculating total time for each recipe
    recipes_obj.parse_total_time()

    # Rating the difficulty of each recipe, with defined cutoff values
    recipes_obj.rate_difficulty(hard_cutoff=60, medium_cutoff=30, missing_label='Unknown')
    
    # Saving the filtered and rated set of recipes 
    recipes_obj.save_recipes(file_name='Chilies')

    # Calculating and saving the average time of each difficulty for filtered set of recipes 
    recipes_obj.save_metrics(file_name='Results')

    






