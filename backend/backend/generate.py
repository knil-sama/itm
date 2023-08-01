import random

from models.url import Url


def generate_url() -> Url:
    """
    Notes:
        The url generate can false due to either because dim are too big (Invalid size)
        or dim are negative (page not found)

    Returns:
        Random url for picsum.photos
    """
    dim_width = random.randint(-1, 1_000)
    dim_heigth = random.randint(-1, 1_000)
    return Url(url=f"https://picsum.photos/{dim_width}/{dim_heigth}")


def generate_urls(min_nb_urls: int = 1, max_nb_urls: int = 100) -> list[Url]:
    """
    Generate of list of urls with various size for image

    Notes:
        We can have duplicate value for url
        We can generate an empty array
    """
    if min_nb_urls < 1 or max_nb_urls < 1:
        msg = f"min_nb_urls and max_nb_urls can't be lower than 1,\
            \ncurrent value {min_nb_urls}, {max_nb_urls}"
        raise ValueError(msg)
    nb_urls = random.randint(min_nb_urls, max_nb_urls)
    return [generate_url() for _ in range(min_nb_urls, nb_urls + 1)]


if __name__ == "__main__":
    generate_urls()
