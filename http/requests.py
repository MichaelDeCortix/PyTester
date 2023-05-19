import requests
from rich.console import Console
from rich.theme import Theme
import curlify
from widgets.display_and_copy import display_and_copy

# Подсветка синтаксиса json
# https://rich.readthedocs.io/en/stable/appendix/colors.html
console = Console(
    theme=Theme(
        {
            "json.key": "orange3",
            "json.str": "deep_sky_blue3",
            "json.number": "dark_cyan",
        }
    )
)

# Отправка запроса через requests
def request(method, url, headers=None, data=None):
    try:
        response = requests.request(method, url, headers=headers, data=data)
        response_time = response.elapsed.total_seconds()
        print(f"Response time (ms): {response_time}")
        print(f"Code: {response.status_code}")
        if response.text:
            try:
                # rich.print_json(json.dumps(response.json(), indent=4, sort_keys=True))
                console.print_json(response.text)
            except:
                print('Body:\n' + response.text)
        display_and_copy(curlify.to_curl(response.request))
        return response
    except requests.exceptions.ConnectionError as e:
        print(f"ConnectionError: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout: {e}")
    except requests.exceptions.TooManyRedirects as e:
        print(f"TooManyRedirects: {e}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")