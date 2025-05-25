from enum import Enum

from types_descriptors.date_time import DateTime
from bot import DATE_TIME_FORMAT_VISIBLE
from UI import UI_statuses
from UI.emoji import UI_status


class StatusType(Enum):
    ON_THE_WAY = UI_statuses.get_on_the_way()
    WAITING_FOR_SPARES = UI_statuses.get_waiting_for_spares()
    WAITING_FOR_REPAIRS = UI_statuses.get_waiting_for_repairs()
    WAITING_FOR_PHOTO = UI_statuses.get_waiting_for_photo()
    WAITING_FOR_PUBLICATION = UI_statuses.get_waiting_for_publication()
    AVAILABLE = UI_statuses.get_available()
    FINISHED = UI_statuses.get_finished()
    CANCELED = UI_statuses.get_cancelled()

    def __str__(self):
        return self.value


class StatusManager:
    @staticmethod
    def get_emoji(status_type: StatusType) -> str:
        return (
            UI_status.get_on_the_way() if status_type == StatusType.ON_THE_WAY else
            UI_status.get_waiting_for_spares() if status_type == StatusType.WAITING_FOR_SPARES else
            UI_status.get_waiting_for_repairs() if status_type == StatusType.WAITING_FOR_REPAIRS else
            UI_status.get_waiting_for_photo() if status_type == StatusType.WAITING_FOR_PHOTO else
            UI_status.get_waiting_for_publication() if status_type == StatusType.WAITING_FOR_PUBLICATION else
            UI_status.get_available() if status_type == StatusType.AVAILABLE else
            UI_status.get_finished() if status_type == StatusType.FINISHED else
            UI_status.get_cancelled() if status_type == StatusType.CANCELED else
            UI_status.get()
        )


class Status:
    date_time = DateTime(True)

    def __init__(self, status_type: StatusType):
        self.comment = None
        self.date_time = None
        self.status_type: StatusType = status_type

    def __repr__(self):
        return (
            f"Status\n"
            f"Status:{self.status_type}\n"
            f"Date:{self.date_time}\n"
            f"Comment:{self.comment}"
        )

    def get_str_date_time(self):
        return self.date_time.strftime(DATE_TIME_FORMAT_VISIBLE)