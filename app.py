
import requests
import streamlit as st



st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered",
)

# Styling inspired by your original PyQt app
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #102b46, #071522);
        color: white;
    }
    h1 {
        text-align: center;
        color: white;
        font-size: 44px !important;
    }
    .stTextInput label {
        color: white;
        font-size: 22px;
        font-weight: bold;
    }
    .stTextInput input {
        text-align: center;
        font-size: 22px;
        min-height: 55px;
    }
    div.stButton > button {
        width: 100%;
        min-height: 55px;
        font-size: 22px;
        font-weight: bold;
        background-color: #168aad;
        color: white;
        border-radius: 12px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #34a0c4;
        color: white;
    }
    .temperature {
        text-align: center;
        font-size: 65px;
        font-weight: bold;
        margin-top: 25px;
    }
    .weather-emoji {
        text-align: center;
        font-size: 100px;
    }
    .description {
        text-align: center;
        font-size: 30px;
        text-transform: capitalize;
    }
    .city-result {
        text-align: center;
        font-size: 24px;
        color: #bde0fe;
    }
</style>
""", unsafe_allow_html=True)


def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 299:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌦️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "❄️"
    elif 701 <= weather_id <= 741:
        return "🌫️"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪️"
    elif weather_id == 800:
        return "☀️"
    elif 801 <= weather_id <= 804:
        return "☁️"
    return "🌤️"


def fetch_weather(city):
    # Keep your API key out of the Python source code.
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error(
            "OpenWeatherMap API key not configured. "
            "Follow Step 2 below to add it."
        )
        return

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": api_key,
                "units": "metric",
            },
            timeout=10,
        )

        if response.status_code == 404:
            st.error("City not found. Please check the spelling.")
            return
        elif response.status_code == 401:
            st.error("Invalid API key. Check your OpenWeatherMap key.")
            return
        elif response.status_code == 429:
            st.error("Too many requests. Please try again later.")
            return

        response.raise_for_status()
        data = response.json()

        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        emoji = get_weather_emoji(weather_id)
        city_name = data["name"]
        country = data["sys"].get("country", "")

        st.markdown(
            f'<div class="city-result">{city_name}, {country}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="temperature">{temperature:.1f}°C</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="weather-emoji">{emoji}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="description">{description}</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        col1.metric("Feels like", f'{data["main"]["feels_like"]:.1f}°C')
        col2.metric("Humidity", f'{data["main"]["humidity"]}%')

        st.caption(
            f'Wind speed: {data["wind"]["speed"]} m/s'
        )

    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Check your internet connection.")
    except requests.exceptions.HTTPError:
        st.error("Weather service error. Please try again later.")
    except (KeyError, ValueError):
        st.error("The weather service returned unexpected data.")


st.title("🌤️ Weather App")
st.write("Enter a city name to check its current weather.")

with st.form("weather_form"):
    city = st.text_input(
        "Enter City name",
        placeholder="e.g. Kathmandu, London, Tokyo",
    )
    submitted = st.form_submit_button("Get Weather")

if submitted:
    if city.strip():
        fetch_weather(city.strip())
    else:
        st.warning("Please enter a city name.")
