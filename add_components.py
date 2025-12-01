import json

def read_ingredients_file(filepath):
    categories = {}
    current_category = None
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                if not line.startswith(' ') and line.endswith('s'):  # Category line
                    current_category = line
                    categories[current_category] = []
                elif line:  # Ingredient line
                    if current_category:
                        categories[current_category].append(line.lower())
    
    # Flatten all ingredients into a single list
    all_ingredients = []
    for ingredients in categories.values():
        all_ingredients.extend(ingredients)
    
    return all_ingredients

def find_components(ingredient_text, keyword_list):
    """Find all keywords that appear in the ingredient text."""
    ingredient_text = ingredient_text.lower()
    return list(set(keyword for keyword in keyword_list 
                   if keyword in ingredient_text.split()))

def update_recipes_with_components():
    # Read the ingredients keywords
    ingredients_keywords = read_ingredients_file('Ingredients.txt')
    
    # Read the recipes JSON
    with open('recipes_clean.json', 'r', encoding='utf-8') as file:
        content = file.read()
        if content.startswith('\ufeff'):
            content = content[1:]
        recipes = json.loads(content)
    
    # Update each recipe with components
    for recipe_id, recipe_data in recipes.items():
        components = set()  # Use set to avoid duplicates
        
        if 'ingredients' in recipe_data:
            # Process each ingredient in the recipe
            for ingredient in recipe_data['ingredients']:
                # Find components in this ingredient
                found_components = find_components(ingredient.lower(), ingredients_keywords)
                components.update(found_components)
        
        # Add the components array to the recipe
        recipe_data['components'] = sorted(list(components))
    
    # Save the updated recipes
    with open('recipes_with_components.json', 'w', encoding='utf-8') as file:
        json.dump(recipes, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    try:
        update_recipes_with_components()
        print("Successfully added components to recipes and saved to recipes_with_components.json")
    except Exception as e:
        print(f"An error occurred: {str(e)}")