# Mscraper

Selenium-Beautifulsoup based web scraper.

Example usage: automate web browsing and information retrieval by storing scraped data in a csv file and sending the file via email.
Support basic Google and Linkedin profiles scraping.

## Disclaimer

This project has been created for research purposes. We do not take any responsibility for the usage of this software. Please check the license for more info.

## Getting Started and Deployment

We suggest using docker-compose, to easily deploy in the cloud or for testing.

```
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
docker-compose up --build
```

Then:

```
docker run -dit -P [image_name]
docker attach [container_id]
```

See the google_linkedin_example.py and the tests for code examples.
For Linkedin, insert the required username, email, password and LI_AT cookie to start scraping. See [here](https://github.com/austinoboyle/scrape-linkedin-selenium) for more info.

### Prerequisites

Tested with:
* docker-compose 1.25.1
* Docker 19.03.5
* Google Chrome 79.0.3945.88-1
* Linkedin website 2020


## Running the tests

```
pytest tests -s
```


## Acknowledgments

* Some code snippets and inspiration for the Linkedin scraping have been taken from [scrape-linkedin-selenium](https://github.com/austinoboyle/scrape-linkedin-selenium). Go check out this repo for a more comprehensive Linkedin scraping.
