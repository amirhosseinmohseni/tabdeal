from datetime import datetime
from .documents import LogDocument

def write_log(level, message, type, source, destination, amount, accept):

    log = LogDocument(
        level=level,
        message=message,
        timestamp=datetime.utcnow(),
        type=type,
        source=source,
        destination=destination,
        amount=amount,
        accept=accept,
    )
    log.save()