# calgary_dogs.py
# Ryan Baker
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd
import numpy as np

def validate_user_input(user_input, dog_breed_list):
    """Validates user input against a dog breed list
    params:
        user_input (str) the dog name or text input by the user
        dog_breed_list (list) the list of dog breeds to check against
        
    returns: 
        (str) the user input (capitalized) as a string if dog name is found
        ValueError (ValueError) if dog name not found
    """
    if user_input in dog_breed_list:
        return user_input.upper()
    else:
        raise ValueError("Dog breed not found in the data. Please try again.")

def main():

    # Import data here
    print("ENSF 692 Dogs of Calgary")

    # Requirement: Your code should include and use at least one multi-index Pandas DataFrame
    df = pd.read_excel("CalgaryDogBreeds.xlsx", index_col=[2,0,1])
    
    # User input stage
    breeds = df.index.levels[0]
    

    while(True):
        user_input = input("Enter a dog breed: ").upper()
        try:
            validate_user_input(user_input, breeds)
            break
        except ValueError as e:
            print(e)


    # Data anaylsis stage
    # 1. Find and print all years where the selected breed was listed in the top breeds.
    # Requirement: Your code should include and use at least one IndexSlice object
    idx = pd.IndexSlice
    breed_data = df.loc[idx[user_input,:,:]]
    top_years = breed_data.index.levels[0]
    print(f"The {user_input} was found in the top breeds for years: {' '.join([str(point) for point in top_years])}")

    # 2. Calculate and print the total number of registrations of the selected breed found in the dataset.
    print(f"There have been {breed_data.sum().values[0]:,} dogs registered total.")

    # 3. Calculate and print the percentage of selected breed registrations out of the total percentage for each year (2021, 2022, 2023).
    for vals in zip(breed_data.groupby('Year').sum()['Total'],df.groupby('Year').sum()['Total'],breed_data.groupby('Year').sum().index):
        print(f"The {user_input} was {vals[0]/vals[1]*100:.6f}% of top breeds in {vals[2]}.")

    # 4. Calculate and print the percentage of selected breed registrations out of the total three-year percentage.
    # Reset indices to demonstrate masking
    df = df.reset_index(['Breed', 'Year', 'Month'])
    # Requirement: Your code should include and use
    print(f"The {user_input} was {df[df['Breed'] == user_input]['Total'].sum()/df['Total'].sum()*100:.6f}% of top breeds across all years.")

    # 5. Find and print the months that were most popular for the selected breed registrations. Print all months that tie.
    # Requirement: Your code should include and use at least one grouping operation
    # Requirement: Your code should include and use at least one built-in Pandas or NumPy computational method
    grouped_breed_data = breed_data.groupby('Month').count()
    max_val = grouped_breed_data.max().values[0]
    popular_months = ' '.join(grouped_breed_data[grouped_breed_data['Total'] == max_val].index)
    print(f"Most popular month(s) for {user_input} dogs: {popular_months}")


if __name__ == '__main__':
    main()
