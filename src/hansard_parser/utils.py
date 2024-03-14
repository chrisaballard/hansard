from datetime import datetime, timedelta
from typing import List

def generate_date_range(
        start_date: datetime, 
        end_date: datetime
) -> List[str]:
    """
    Generate a list of dates between the start_date and end_date, inclusive.
    
    Parameters:
    - start_date: The starting date of the date range (datetime.date)
    - end_date: The ending date of the date range (datetime.date)
    
    Returns:
    - date_list: List of dates in the format "%Y-%m-%d"

    # Example usage:
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 5)
    date_range = generate_date_range(start_date, end_date)
    print(date_range)
    """

    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_list

