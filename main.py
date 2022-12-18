import bs4.element
import requests
from bs4 import BeautifulSoup, SoupStrainer

URL = "https://news.ycombinator.com/newest"
RESULTS = []


def get_story_rank(
        rank_element: bs4.element.ResultSet,
) -> str:
    """Finds and returns story rank"""
    return rank_element.find("span", attrs={"class": "rank"}).text


def get_story_title(
        title_element: bs4.element.ResultSet
) -> str:
    """Finds and returns story title"""
    return title_element.find("a").text


def get_story_points(
        metrics_element: bs4.element.ResultSet
) -> str:
    """Finds and returns story points"""
    return metrics_element.find("span", attrs={"class": "score"}).text


def get_story_age(
        metrics_element: bs4.element.ResultSet
) -> str:
    """Finds and returns story age"""
    return metrics_element.find("span", attrs={"class": "age"}).text


def run() -> None:
    """Parses the html page.
    Prints the details of top 10 stories"""
    page = requests.get(URL)
    # We only want to parse td
    only_td = SoupStrainer('td')
    soup = BeautifulSoup(page.content, "html.parser", parse_only=only_td)
    # Get the title of the story
    td_title = soup.find_all("td", attrs={"class": "title"})
    # Get the rank of the story
    td_rank = soup.find_all("td", attrs={"class": "title", "align": "right"})
    # Get the metrics of the story
    td_metrics = soup.find_all("td", attrs={"class": "subtext"})
    # Some titles have rank td in them,
    # We need only the titles
    td_title_only = [title for title in td_title if title not in td_rank]

    for i in range(11):
        story_dict = {
            "rank": get_story_rank(td_rank[i]),
            "title": get_story_title(td_title_only[i]),
            "points": get_story_points(td_metrics[i]),
            "age": get_story_age(td_metrics[i])
        }
        RESULTS.append(story_dict)
    [print(story) for story in RESULTS]


if __name__ == '__main__':
    run()
