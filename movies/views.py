import csv
from django.shortcuts import render
from django.conf import settings
import os
from collections import Counter

def display(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'movies', 'imdb.csv')
    data = []
    ratings = []
    release_years = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        
        # Get index for relevant columns
        try:
            rating_index = header.index('No_of_Votes')
            year_index = header.index('Released_Year')
        except ValueError:
            # Handle cases where columns might not be present
            rating_index = year_index = None

        for row in reader:
            data.append(row)

            if rating_index is not None:
                try:
                    ratings.append(float(row[rating_index]))
                except (ValueError, IndexError):
                    pass  # Ignore rows with non-numeric or missing ratings

            if year_index is not None:
                try:
                    release_years.append(row[year_index])
                except IndexError:
                    pass  # Ignore rows with missing release year

    total_movies = len(data)
    
    if ratings:
        average_number_votes = sum(ratings) / len(ratings)
        min_votes = min(ratings)
        max_votes = max(ratings)
    else:
        average_number_votes = min_votes = max_votes = None

    # Count the number of movies per year
    movies_per_year = Counter(release_years)

    # Sort the dictionary by year (key)
    sorted_movies_per_year = dict(sorted(movies_per_year.items()))

    context = {
        'header': header,
        'data': data,
        'total_movies': total_movies,
        'average_number_votes': average_number_votes,
        'min_votes': min_votes,
        'max_votes': max_votes,
        'movies_per_year': sorted_movies_per_year,
    }

    return render(request, 'display.html', context)
