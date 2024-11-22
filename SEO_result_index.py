
# API_KEY = 'AIzaSyAB-s4bdNQc4NMKQdjEN4FfMkPKdoNaqIg'
# CX = 'd17d856268ffa4247'

from urllib.parse import urlparse
import requests


def read_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = [line.strip() for line in file if line.strip()]
    return keywords


def google_search(keyword, api_key, search_engine_id):
    url = f"https://www.googleapis.com/customsearch/v1?q={keyword}&key={api_key}&cx={search_engine_id}"
    response = requests.get(url)
    return response.json()


def extract_result_count(search_response):
    if 'searchInformation' in search_response:
        return search_response['searchInformation'].get('totalResults', "0")
    return "0"


def batch_keywords(keywords, batch_size=10):
    for i in range(0, len(keywords), batch_size):
        yield keywords[i:i + batch_size]


def save_results_to_file(results, file_path):
    with open(file_path, 'w') as file:
        for keyword, result_count in results:
            file.write(f"{keyword}: {result_count}\n")


def main():
    api_key = 'AIzaSyAB-s4bdNQc4NMKQdjEN4FfMkPKdoNaqIg'  
    search_engine_id = 'd17d856268ffa4247'  

    
    keywords = read_keywords('domain.txt')

    results = []

    # Process keywords in batches
    for batch in batch_keywords(keywords, batch_size=10):  # Adjust batch size if needed
        for keyword in batch:
            search_response = google_search(keyword, api_key, search_engine_id)

            # Extract the total result count
            result_count = extract_result_count(search_response)
            print(f"Keyword: {keyword}, Results: {result_count}")

            results.append((keyword, result_count))

    # Save the results to a file
    save_results_to_file(results, 'result_numbers.txt')
    print("Result numbers saved to result_numbers.txt")


if __name__ == "__main__":
    main()
