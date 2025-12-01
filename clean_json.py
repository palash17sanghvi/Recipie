import json

def clean_string(text):
    return text.replace(' ADVERTISEMENT', '').strip()

# Read the original JSON file
with open('recipes_raw_nosource_ar.json', 'r', encoding='utf-8') as file:
    content = file.read()
    # Remove any BOM if present
    if content.startswith('\ufeff'):
        content = content[1:]
    data = json.loads(content)

# Clean each recipe's ingredients
cleaned_data = {}
for recipe_id, recipe in data.items():
    cleaned_recipe = recipe.copy()
    if 'ingredients' in recipe:
        cleaned_recipe['ingredients'] = [
            clean_string(ingredient)
            for ingredient in recipe['ingredients']
            if clean_string(ingredient) != ''
        ]
    cleaned_data[recipe_id] = cleaned_recipe

# Save the cleaned data to a new file
with open('recipes_clean.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, indent=2, ensure_ascii=False)

print("Successfully created recipes_clean.json with cleaned data!")