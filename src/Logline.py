import logging
import os
from datetime import datetime
import time
from tabulate import tabulate

class Logger:
    """
    Set up a logger with console and file handlers.

    Args:
        name (str): The name of the logger.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = self.setup_logger()

    def setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)

        # Avoid adding handlers multiple times
        if not logger.hasHandlers():
            # Create logs directory if it doesn't exist
            os.makedirs("Logs", exist_ok=True)

            # Formatter with line number
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # Define the date format for filenames
            date_str = datetime.now().strftime("%Y-%m-%d")

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # File handler for general logs
            general_log_file = f"logs/general_{date_str}.log"
            file_handler = self.errorHandler(general_log_file, logdata=LogData)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger
    
    class errorHandler(logging.FileHandler):
        def __init__(self, filename, logdata):
            super().__init__(filename)
            self.logdata = logdata

        def emit(self, record):
            # Log the message to the file as usual
            super().emit(record)

            # If the record is an error, call the custom error function
            if record.levelno == logging.ERROR:
                self.logdata.addError()

    @staticmethod
    def errortrace(logger: logging.Logger, exception: Exception):
        """Log an exception with a stack trace."""
        logger.error("An error occurred", exc_info=True)


class LogData:
    inventoryCount = 0
    productDetailsCount = 0
    uomCount = 0
    priceCount = 0
    errorCount = 0
    startTime = None
    
    @classmethod
    def startTimer(cls):
        cls.startTime = time.time()


    @classmethod
    def getElapsedTime(cls):
        if cls.startTime is not None:
            elapsed_time = time.time() - cls.startTime
            return elapsed_time / 60  # Convert seconds to minutes
        else:
            return None  # Timer hasn't started

    @classmethod
    def addInventoryCount(cls):
        cls.inventoryCount += 1

    @classmethod
    def addProductDetailsCount(cls):
        cls.productDetailsCount += 1

    @classmethod
    def addUOMCount(cls):
        cls.uomCount += 1

    @classmethod
    def addPriceCount(cls):
        cls.priceCount += 1

    @classmethod
    def addError(cls):
        cls.errorCount += 1

    @classmethod
    def resetData(cls):
            cls.inventoryCount = 0
            cls.productDetailsCount = 0
            cls.uomCount = 0
            cls.priceCount = 0
            cls.errorCount = 0
            cls.startTime = None

    @classmethod
    def getLogData(cls):
        elapsed_time = cls.getElapsedTime()
        elapsed_time_str = (
            f"{elapsed_time:.2f} minutes"
            if elapsed_time is not None
            else "Timer not started"
        )

        data = [
            ["Elapsed Time", elapsed_time_str],
            ["Inventory Records Created", cls.inventoryCount],
            ["ProductDetails Records Created", cls.productDetailsCount],
            ["UOM Records Created", cls.uomCount],
            ["Price Records Created", cls.priceCount],
            ["Errors logged", cls.errorCount],
        ]

        table = tabulate(data, tablefmt="grid")
        cls.resetData()

        return table
