"""Museum attendance data fetcher application."""
import sys

from museum_attendance_common import Settings, get_db_session, close_db, setup_logging, get_logger, ImportStatus
from museum_attendance_common.repository import CountryRepository, CityRepository, MuseumRepository, MuseumAttributesRepository, ImportLogRepository
from service import DataCollectionService, PersistenceService

# Configure logging
settings = Settings()
setup_logging(log_level=settings.log_level)

logger = get_logger(__name__)


def export() -> None:
    """Main application entry point."""
    logger.info("Starting museum attendance data fetcher...")
    
    with get_db_session() as session:
        import_log_repository = ImportLogRepository(session)
        import_log = None
        logger.debug("Starting import job log entry")

        result: dict[str, int|str] = {
            "page_name": "List_of_most_visited_museums"
        }

        import_log = import_log_repository.start_job(ImportStatus.IN_PROGRESS, result=result)
        session.commit()
        inserted_countries = 0
        updated_countries = 0
        inserted_cities = 0
        updated_cities = 0
        inserted_museums = 0
        updated_museums = 0
        inserted_attributes = 0
        updated_attributes = 0

        try:
            logger.debug("Collecting museum data from Wikipedia")
            data = DataCollectionService.collect_data("List_of_most_visited_museums")

            logger.debug("Persisting collected data to the database")
            persistence_service = PersistenceService(
                museum_repository=MuseumRepository(session),
                country_repository=CountryRepository(session),
                museum_attributes_repository=MuseumAttributesRepository(session),
                city_repository=CityRepository(session)
            )

            logger.debug("Beginning data persistence loop")
            for museum_dto in data.wikipedia_museum_instance_list:
                logger.debug(f"Persisting data for museum: {museum_dto.get_museum_name()}")
                logger.debug(f"Persisting data for country: {museum_dto.get_country()}")
                country, country_inserted, country_updated = persistence_service.persist_country(museum_dto.get_country())
                if country_inserted:
                    inserted_countries += 1
                if country_updated:
                    updated_countries += 1
                logger.debug(f"Persisting data for city: {museum_dto.get_city()}")
                city, city_inserted, city_updated = persistence_service.persist_city(museum_dto, country)
                if city_inserted:
                    inserted_cities += 1
                if city_updated:
                    updated_cities += 1
                logger.debug(f"Persisting data for museum: {museum_dto.get_museum_name()}")
                museum, museum_inserted, museum_updated = persistence_service.persist_museum(museum_dto, city)
                if museum_inserted:
                    inserted_museums += 1
                if museum_updated:
                    updated_museums += 1
                logger.debug(f"Persisting museum attributes for museum: {museum_dto.get_museum_name()}")
                attribute_inserted, attribute_updated = persistence_service.persist_museum_attributes(museum_dto.wikipedia_museum_attributes, museum)
                inserted_attributes += attribute_inserted
                updated_attributes += attribute_updated
            logger.info(f"Inserted Countries: {inserted_countries}, Updated Countries: {updated_countries}")
            logger.info(f"Inserted Cities: {inserted_cities}, Updated Cities: {updated_cities}")
            logger.info(f"Inserted Museums: {inserted_museums}, Updated Museums: {updated_museums}")
            logger.info(f"Inserted Museum Attributes: {inserted_attributes}, Updated Museum Attributes: {updated_attributes}")

            import_log_repository.end_job_with_success(import_log, result={**result, 
                "inserted_countries": inserted_countries,
                "updated_countries": updated_countries,
                "inserted_cities": inserted_cities,
                "updated_cities": updated_cities,
                "inserted_museums": inserted_museums,
                "updated_museums": updated_museums,
                "inserted_attributes": inserted_attributes,
                "updated_attributes": updated_attributes
            })
        except KeyboardInterrupt:
            if import_log:
                import_log_repository.end_job_with_failure(import_log, result={**result, "error_message": "Application interrupted by user"})
            logger.info("Application interrupted by user")
        except Exception as e:
            if import_log:
                import_log_repository.end_job_with_failure(import_log, result={**result, "error_message": str(e)})
            logger.exception(f"Unexpected error: {e}")
            sys.exit(1)
        finally:
            close_db()
            logger.info("Application shutdown complete")


if __name__ == "__main__":
    export()