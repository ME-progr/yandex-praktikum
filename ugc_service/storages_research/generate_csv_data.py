from storages_research.config import settings
from storages_research.utils import generate_csv_film_view_data


if __name__ == '__main__':
    generate_csv_film_view_data(10_000_000, mongo=settings.mongo_settings.mongo_test)
