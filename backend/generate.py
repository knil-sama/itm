import typing
import random
import typing

def generate_url() -> str:
    """
    Notes:
        The url generate can false due to either because dim are too big (Invalid size) or dim are negative (page not found)
        
    Returns:
        Random url for picsum.photos
    """
    dim_width = random.randint(-1, 10_000)
    dim_heigth = random.randint(-1, 10_000)
    return f'https://picsum.photos/{dim_width}/{dim_heigth}'

def generate_urls(min_nb_urls: int=0, max_nb_urls:int=100) -> typing.List[str]:
    """
    Generate of list of urls with various size for image

    Notes:
        We can have duplicate value for url
        We can generate an empty array
    """
    nb_urls = random.randint(min_nb_urls, max_nb_urls)
    urls = [generate_url() for _ in range(min_nb_urls, max_nb_urls)]
    return urls

if __name__ == "__main__":
    generate_urls()
