from covid_news_handling import news_API_request
from covid_news_handling import update_news

def test_news_API_request() -> None:
    """ Checks if news_API_request returns a value and if it has default values
    of 'Covid COVID-19 coronavirus' """

    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news() -> None:
    """Runs function update_news with paramter 'test' to check the result """
    update_news('test')
