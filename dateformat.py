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

#* Później można dodać więcej języków
def date_format(date: str) -> str:
    '''
    Function for unshorting days/moths names
    '''

    for month in EN['months']:
        if date[5:8] == month:
            date = date.replace(date[5:8], EN['months'][month])
            break
    
    for day in EN['days']:
        if date[:3] == day:
            date = date.replace(date[:3], EN['days'][day])
            break
    
    return date

def main() -> None:
    print('RUN `main.py`!!!')
    exit()

if __name__ == '__main__':
    main()