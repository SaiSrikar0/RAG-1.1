import os
import json
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from indexing import get_vector_store
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY not found")


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = "data/sample_data.jsonl"

class DataIngestionHandler(FileSystemEventHandler):
    def __init__(self):
        self.vector_store = get_vector_store()

    def on_modified(self, event):
        if event.src_path.endswith(".jsonl"):
            logger.info(f"Detected changes in {event.src_path}. Updating vector store...")
            self.update_vector_store()

    def update_vector_store(self):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                docs = [json.loads(line) for line in f]

            if not docs:
                logger.warning("No new data found.")
                return

            texts = [doc.get("text") for doc in docs if "text" in doc]
            if not texts:
                logger.warning("No valid text fields found.")
                return

            self.vector_store = get_vector_store()
            logger.info("Vector store updated successfully!")

        except Exception as e:
            logger.error(f"Error updating vector store: {str(e)}", exc_info=True)

def start_ingestion():
    os.makedirs("data", exist_ok=True)  # Ensure the "data" folder exists
    if not os.path.exists(DATA_PATH):
        open(DATA_PATH, "w").close()


    event_handler = DataIngestionHandler()
    observer = Observer()
    observer.schedule(event_handler, path="data/", recursive=False)
    observer.start()

    logger.info("Started real-time ingestion service.")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Ingestion service stopped.")

    observer.join()

if __name__ == "__main__":
    start_ingestion()
