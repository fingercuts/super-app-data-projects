import generate_entities
import generate_transactions
import generate_dirty_data
from logger import logger

if __name__ == "__main__":
    logger.info("Starting Enterprise Data Generation Pipeline...")
    generate_entities.generate_users()
    generate_entities.generate_drivers()
    generate_entities.generate_merchants()
    generate_entities.generate_services_and_promos()
    
    generate_transactions.generate_transactions()
    
    generate_dirty_data.simulate_dirty_data_pipeline()
    
    logger.info("Pipeline Completed Successfully!")
