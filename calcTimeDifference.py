from datetime import datetime
import constants


def calculate_time_difference(alarm_str, updated_time=None):

    if alarm_str:
        formatted_alarm_str = datetime.strptime(alarm_str, '%I:%M %p')

        if updated_time is not None:
            formatted_current_time = datetime.strptime(updated_time, '%I:%M %p')
        else:
            formatted_current_time = datetime.strptime(constants.current_time, '%I:%M %p')

        time_difference = formatted_alarm_str - formatted_current_time

        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            time_str = f"in {days} days {hours} hours {minutes} minutes"
        elif hours > 0:
            time_str = f"in {hours} hours {minutes} minutes"
        else:
            time_str = f"in {minutes} minutes"

        return time_str
