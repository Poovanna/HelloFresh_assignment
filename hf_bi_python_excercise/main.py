recipeFilter = __import__('recipes-etl.recipeFilter')
GeneralUtils = __import__('recipes-etl.utils')
 

if __name__=='__main__':

    url='https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json'
    file_data = GeneralUtils.utils.GeneralUtils.file_fetch(url)

    recipes_obj =recipeFilter.recipeFilter.RecipeFilter(file_data, 'chilies')

    recipes_obj.parse_total_time()
    recipes_obj.rate_difficulty(hard_cutoff=60, medium_cutoff=30, missing_label='Unknown')
    recipes_obj.save_recipes(file_name='Chilies')
    recipes_obj.save_metrics(file_name='Results')

    






