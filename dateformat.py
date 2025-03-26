EN = {
    'days': {
        'Mon': 'Monday',
        'Tue': 'Tuesday',
        'Wed': 'Wednesday',
        'Thu': 'Thursday',
        'Fri': 'Friday',
        'Sat': 'Saturday',
        'Sun': 'Sunday'
    },
    'months': {
        'Jan': 'January',
        'Feb': 'February',
        'Mar': 'March',
        'Apr': 'April',
        'May': 'May',
        'Jun': 'June',
        'Jul': 'July',
        'Aug': 'August',
        'Sep': 'September',
        'Oct': 'October',
        'Nov': 'November',
        'Dec': 'December'
    }
}

def date_format(date: str) -> str:
    """
    Format a date string by expanding abbreviated day and month names.
    
    Converts short day and month names (like 'Mon' or 'Jan') to their
    full form (like 'Monday' or 'January').
    
    Args:
        date: Date string with abbreviated day and month names
        
    Returns:
        Formatted date string with full day and month names
    """

    #todo dodać zamiane na polskie nazwy dni i miesięcy
    #todo dodać zmiane kolejności dni i miesięcy

    try:
        for month in EN['months']:
            if date[5:8] == month:
                date = date.replace(date[5:8], EN['months'][month])
                break
    
        for day in EN['days']:
            if date[:3] == day:
                date = date.replace(date[:3], EN['days'][day])
                break
    
        return date
    except (IndexError, TypeError) as e:
        print(f'Error formatting date: {e}')
        return date

def main() -> None:
    print('RUN `main.py`!!!')
    exit()

if __name__ == '__main__':
    main()