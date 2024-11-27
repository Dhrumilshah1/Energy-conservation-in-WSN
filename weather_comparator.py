import requests

# API endpoints
city_condition_url = "https://quest.squadcast.tech/api/RA2111003011293/weather"
weather_details_url = "https://quest.squadcast.tech/api/RA2111003011293/weather/get?q="
submission_url = "https://quest.squadcast.tech/api/RA2111003011293/submit/weather?answer={}&extension=py"

def get_city_and_condition():
    """Retrieve the two cities and the weather condition to compare."""
    response = requests.get(city_condition_url)
    if response.status_code == 200:
        return response.json().get("city1"), response.json().get("city2"), response.json().get("condition")
    else:
        print("Failed to fetch city and condition data.")
        return None, None, None

def get_weather(city):
    """Retrieve weather data for a given city."""
    response = requests.get(weather_details_url + city)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for {city}.")
        return None

def find_better_location(city1_data, city2_data, condition):
    """Determine the better city based on the specified condition."""
    if condition == "hot":
        return city1_data["name"] if city1_data["temperature"] > city2_data["temperature"] else city2_data["name"]
    elif condition == "cold":
        return city1_data["name"] if city1_data["temperature"] < city2_data["temperature"] else city2_data["name"]
    elif condition == "windy":
        return city1_data["name"] if city1_data["wind"] > city2_data["wind"] else city2_data["name"]
    elif condition == "rainy":
        return city1_data["name"] if city1_data["rain"] > city2_data["rain"] else city2_data["name"]
    elif condition == "sunny":
        return city1_data["name"] if city1_data["cloud"] < city2_data["cloud"] else city2_data["name"]
    elif condition == "cloudy":
        return city1_data["name"] if city1_data["cloud"] > city2_data["cloud"] else city2_data["name"]
    else:
        print("Unknown condition provided.")
        return None

def submit_result(answer):
    """Submit the result to the specified URL."""
    response = requests.post(submission_url.format(answer))
    if response.status_code == 200:
        print("Result submitted successfully!")
    else:
        print("Failed to submit the result.")

def main():
    # Step 1: Get cities and condition
    city1, city2, condition = get_city_and_condition()
    if not all([city1, city2, condition]):
        print("Could not retrieve city and condition information.")
        return

    # Step 2: Get weather data for each city
    city1_data = get_weather(city1)
    city2_data = get_weather(city2)

    if not city1_data or not city2_data:
        print("Could not retrieve weather data for both cities.")
        return

    # Step 3: Determine the better location based on the condition
    answer = find_better_location(city1_data, city2_data, condition)
    if answer:
        print(f"The better location based on the condition '{condition}' is: {answer}")

        # Step 4: Submit the answer
        submit_result(answer)

if __name__ == "__main__":
    main()
