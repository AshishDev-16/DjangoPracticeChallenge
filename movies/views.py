import csv
from django.shortcuts import render
from django.conf import settings
import os

def display(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'movies', 'imdb.csv')
    data = []
    ratings = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  
        rating_index = header.index('No_of_Votes')  

        for row in reader:
            data.append(row)
            
            try:
                ratings.append(float(row[rating_index]))
            except ValueError:
                pass  
    total_movies = len(data)
    if ratings:
        average_number_votes = sum(ratings) / len(ratings)
        min_votes = min(ratings)
        max_votes = max(ratings)
    else:
        average_number_votes = min_votes = max_votes = None

    context = {
        'header': header,
        'data': data,
        'total_movies': total_movies,
        'average_number_votes': average_number_votes,
        'min_votes': min_votes,
        'max_votes': max_votes,
    }

    return render(request, 'display.html', context)
