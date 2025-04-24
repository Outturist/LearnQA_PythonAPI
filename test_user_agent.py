import pytest
import requests

class TestUserAgent:
    user_agents = [
        'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
        'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    ]

    expected_values = [
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'},
        {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'},
        {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'},
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'},
        {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
    ]

    @pytest.mark.parametrize("user_agent, expected_values", zip(user_agents, expected_values))
    def test_num(self, user_agent, expected_values):

        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent}
        )

        assert response.json()['platform'] == expected_values['platform'], f"For user_agent {user_agent} platform is not: {expected_values['platform']}. Actual value of platform is: {response.json()['platform']}"
        assert response.json()['browser'] == expected_values['browser'], f"For user_agent {user_agent} platform is not: {expected_values['browser']}. Actual value of platform is: {response.json()['browser']}"
        assert response.json()['device'] == expected_values['device'], f"For user_agent {user_agent} platform is not: {expected_values['device']}. Actual value of platform is: {response.json()['device']}"
