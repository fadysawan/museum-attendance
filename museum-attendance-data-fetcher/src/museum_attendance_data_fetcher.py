"""Museum attendance data fetcher application."""
import sys
import requests
from sqlalchemy import text

from config import settings, get_db_session, close_db
from utils import setup_logging, get_logger
from model import Country, City, Museum
from repository import CountryRepository, CityRepository, MuseumRepository, MuseumAttributesRepository, ImportLogRepository
from enumeration import ImportStatus
from service import DataCollectionService, PersistenceService

# Configure logging
setup_logging(log_level=settings.log_level)

logger = get_logger(__name__)


def main():
    """Main application entry point."""
    # logger.info("Starting museum attendance data fetcher...")
    
    with get_db_session() as session:
        import_log_repository = ImportLogRepository(session)
        import_log = None

        import_log = import_log_repository.start_job(ImportStatus.IN_PROGRESS, "List_of_most_visited_museums")

        inserted_countries = 0
        updated_countries = 0
        inserted_cities = 0
        updated_cities = 0
        inserted_museums = 0
        updated_museums = 0
        inserted_attributes = 0
        updated_attributes = 0

        try:
            data = DataCollectionService.collect_data("List_of_most_visited_museums")
            persistence_service = PersistenceService(
                museum_repository=MuseumRepository(session),
                country_repository=CountryRepository(session),
                museum_attributes_repository=MuseumAttributesRepository(session),
                city_repository=CityRepository(session)
            )

            for museum_dto in data.wikipedia_museum_instance_list:
                country, country_inserted, country_updated = persistence_service.persist_country(museum_dto.get_country())
                if country_inserted:
                    inserted_countries += 1
                if country_updated:
                    updated_countries += 1
                city, city_inserted, city_updated = persistence_service.persist_city(museum_dto, country)
                if city_inserted:
                    inserted_cities += 1
                if city_updated:
                    updated_cities += 1
                museum, museum_inserted, museum_updated = persistence_service.persist_museum(museum_dto, city)
                if museum_inserted:
                    inserted_museums += 1
                if museum_updated:
                    updated_museums += 1
                attribute_inserted, attribute_updated = persistence_service.persist_museum_attributes(museum_dto.wikipedia_museum_attributes, museum)
                inserted_attributes += attribute_inserted
                updated_attributes += attribute_updated
            logger.info(f"Inserted Countries: {inserted_countries}, Updated Countries: {updated_countries}")
            logger.info(f"Inserted Cities: {inserted_cities}, Updated Cities: {updated_cities}")
            logger.info(f"Inserted Museums: {inserted_museums}, Updated Museums: {updated_museums}")
            logger.info(f"Inserted Museum Attributes: {inserted_attributes}, Updated Museum Attributes: {updated_attributes}")

            result: dict[str, int] = {
                "inserted_countries": inserted_countries,
                "updated_countries": updated_countries,
                "inserted_cities": inserted_cities,
                "updated_cities": updated_cities,
                "inserted_museums": inserted_museums,
                "updated_museums": updated_museums,
                "inserted_attributes": inserted_attributes,
                "updated_attributes": updated_attributes
            }

            import_log_repository.end_job_with_success(import_log, result=result)
        except KeyboardInterrupt:
            if import_log:
                import_log_repository.end_job_with_failure(import_log, result={"error_message": "Application interrupted by user"})
            logger.info("Application interrupted by user")
        except Exception as e:
            if import_log:
                import_log_repository.end_job_with_failure(import_log, result={"error_message": str(e)})
            logger.exception(f"Unexpected error: {e}")
            sys.exit(1)
        finally:
            close_db()
            logger.info("Application shutdown complete")


if __name__ == "__main__":
    main()