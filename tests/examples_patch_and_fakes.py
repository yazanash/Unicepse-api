import requests
from unittest import mock
from unittest.mock import patch


def imdb_info(title):
    """ Gets the movie from IMDB """
    print(f"Searching for the movie {title}!")
    result = requests.get(f"https://imdb-api.com/API/SearchTitle/{title}")
    return result.json()


def bye():
    return "bye"


def hello():
    return "hello"


@patch('__main__.hello', side_effect=bye)
def test(hello_mock):
    return hello()


if __name__ == '__main__':
    with mock.patch('__main__.imdb_info', return_value={'statusCode': 200}) as dummy:  # noqa: E501
        """ This is a patch for imdb_info method """
        print(imdb_info("Bambi"))   # prints {'statusCode': 200}

    with mock.patch('__main__.imdb_info') as imdb:
        """ This is another patch from for imdb_info method """
        imdb.return_value = {'statusCode': 404}
        print(imdb_info("Bambi"))   # prints {'statusCode': 200}

    with mock.patch('requests.get', return_value={'statusCode': 200}) as req:
        """ This is a patch for the requests package get method """
        # this will never call the requests.get method
        print(imdb_info("Bambi"))

    print(hello())    # prints 'hello'
    print(bye())      # prints 'bye'
    print(test())     # prints 'bye'
