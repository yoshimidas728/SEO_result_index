import requests

def read_keywords(file_path):
    """
    Read keywords from the specified file.
    """
    try:
        with open(file_path, 'r') as file:
            keywords = [line.strip() for line in file if line.strip()]
        return keywords
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def google_search(keyword, api_key, search_engine_id):
    """
    Perform a search query using Google's Custom Search JSON API.
    """
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': keyword,
        'key': api_key,
        'cx': search_engine_id,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error with API request for '{keyword}': {e}")
        return None


def extract_result_count(search_response):
    """
    Extract the total results count from Google's Custom Search API response.
    """
    if search_response and 'searchInformation' in search_response:
        return search_response['searchInformation'].get('totalResults', "0")
    return "0"


def save_results_to_file(results, file_path):
    """
    Save the results to a file in a 'keyword: count' format.
    """
    try:
        with open(file_path, 'w') as file:
            for keyword, result_count in results:
                file.write(f"{keyword}: {result_count}\n")
        print(f"Results saved to '{file_path}'.")
    except Exception as e:
        print(f"Error saving results to file: {e}")


def main():
    api_key = 'AIzaSyAB-s4bdNQc4NMKQdjEN4FfMkPKdoNaqIg'  # Replace with your API key
    search_engine_id = 'd17d856268ffa4247'  # Replace with your Search Engine ID

    # Read keywords from the domain.txt file
    keywords = read_keywords('domain.txt')

    if not keywords:
        print("No keywords found in the file.")
        return

    results = []

    # Process each keyword
    for keyword in keywords:
        search_response = google_search(keyword, api_key, search_engine_id)
        result_count = extract_result_count(search_response)
        print(f"Keyword: {keyword}, API Result Count: {result_count}")
        results.append((keyword, result_count))

    # Save results to a file
    save_results_to_file(results, 'result_numbers.txt')


if __name__ == "__main__":
    main()
