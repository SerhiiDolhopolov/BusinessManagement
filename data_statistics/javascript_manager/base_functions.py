def get_func_date_to_str() -> str:
    return """
        function dateToStr(date) 
        {
            return `${String(date.getDate()).padStart(2, '0')}.${String(date.getMonth() + 1).padStart(2, '0')}.${date.getFullYear()}`;
        }
    """


def get_func_get_count_days_in_month() -> str:
    return """
        function getCountDaysInMonth(date) 
        {
            let currentMonth = date.getMonth(); 
            let lastDayOfMonth = new Date(date.getFullYear(), currentMonth + 1, 0);
            let daysInMonth = lastDayOfMonth.getDate();
            return daysInMonth
        }
    """


def get_func_set_info_text():
    return """
        function setInfoText(info)
        {
            document.getElementById('diagram-info').innerText = info;
        }
    """