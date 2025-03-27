from UI import UI_statistics


def get_func_show_diagrams_by_dates_filter() -> str:
    return f"""
        function showDiagramsByDatesFilter() 
        {{
            const regex_pattern_date = /(\\d{{1,2}})\\D(\\d{{1,2}})\\D(\\d{{4}})/;
            let startDateText = document.getElementById('start-date').value;
            let endDateText = document.getElementById('end-date').value;

            let startDate = null;
            let endDate = null;

            const match_start = startDateText.match(regex_pattern_date);
            const match_end = endDateText.match(regex_pattern_date);
            if (match_start && match_end) 
            {{
              let [_, day, month, year] = match_start; 
              startDate = new Date(year, month - 1, day);
              [_, day, month, year] = match_end; 
              endDate = new Date(year, +month - 1, +day);
            }}
            else 
            {{
              alert("Select start and end date.");
              return;
            }}

            if (!startDate || !endDate) 
            {{
                alert("Select start and end date.");
                return;
            }}
            startDate.setHours(0, 0, 0, 0);
            endDate.setHours(23, 59, 59, 999);

            showIncomeDiagramByDatesFilter(startDate, endDate)
            showDefectsDiagramByDatesFilter(startDate, endDate)
            showUsersDiagramByDatesFilter(startDate, endDate)
            setInfoText(`{UI_statistics.get_statistic_from()} ${{dateToStr(startDate)}} {UI_statistics.get_statistic_to()} ${{dateToStr(endDate)}}`);
        }}
    """
def get_func_show_diagrams_by_dates() -> str:
    return f"""
            function showDiagramsByDates() 
            {{
                showIncomeDiagramByDates();
                showModelsDiagramByDates();
                showDefectsDiagramByDates();
                showUsersDiagramByDates();
                setInfoText('{UI_statistics.get_all_statistic()}');
            }}
            """

def get_func_show_diagrams_by_months() -> str:
    return get_func_show_diagrams_by('months', UI_statistics.get_statistic_by_months())

def get_func_show_diagrams_by_years() -> str:
    return get_func_show_diagrams_by('years', UI_statistics.get_statistic_by_years())

def get_func_show_diagrams_by(by: str, info_text: str) -> str:
    """Example:
        get_func_show_diagrams_by('months', 'Statistic by months')
    """
    return f"""
        function showDiagramsBy{by.title().replace(' ', '')}()
        {{
            showIncomeDiagramBy{by.title().replace(' ', '')}()
            showModelsDiagramByDates();
            showDefectsDiagramByDates();
            showUsersDiagramByDates();
            setInfoText('{info_text}');
        }}
    """



def get_func_show_diagrams_to_next_x_days() -> str:
    return f"""
        function showDiagramsToNextXDays(startDate, days_count) 
        {{
            const endDate = new Date(startDate);
            endDate.setDate(startDate.getDate() + days_count - 1);
            startDate.setHours(0, 0, 0, 0);
            endDate.setHours(23, 59, 59, 999);
            
            showIncomeDiagramByDatesFilter(startDate, endDate);
            showModelsDiagramByDatesFilter(startDate, endDate);
            showDefectsDiagramByDatesFilter(startDate, endDate);
            showUsersDiagramByDatesFilter(startDate, endDate);
            setInfoText(`{UI_statistics.get_statistic_from()} ${{dateToStr(startDate)}} {UI_statistics.get_statistic_to()} ${{dateToStr(endDate)}}`);
        }}
    """

def get_func_show_diagrams_by_x_days(days_count: int) -> str:
    return f"""
        function showDiagramsBy{days_count}Days() {{
            const day = new Date();
            day.setDate(day.getDate() - {days_count - 1});
            showDiagramsToNextXDays(day, {days_count});
        }}
    """



def get_func_show_diagrams_from_monday_to_next_week() -> str:
    return """
        function showDiagramsFromMondayToNextWeek(startDate) 
        {
            const day = startDate.getDay(); // 0 - sunday, 1 - monday
            const diff = (day === 0 ? -6 : 1) - day;
            const monday = new Date(startDate);
            monday.setDate(startDate.getDate() + diff);
            showDiagramsToNextXDays(monday, 7);
        }
    """

def get_func_show_diagrams_by_x_week(week_title: str, difference_week: int = 0):
    """Example: 
        week_title: Current, Previous, Next
        diffence_week: 0(current), -1(previous), 1(next)"""
    return f"""
        function showDiagramsBy{week_title.title().replace(' ', '')}Week() {{
            const day = new Date();
            day.setDate(day.getDate() + {7 * difference_week});
            showDiagramsFromMondayToNextWeek(day);
        }}
    """



def get_func_show_diagrams_from_first_day_to_next_month() -> str:
    return """
        function showDiagramsFromFirstDayToNextMonth(startDate) 
        {
            const firstDay = new Date(startDate);
            firstDay.setDate(1);
            showDiagramsToNextXDays(firstDay, getCountDaysInMonth(firstDay));
        }
    """

def get_func_show_diagrams_by_x_month(month_title: str, difference_month: int = 0):
    """Example: 
        month_title: Current, Previous, Next
        diffence_month: 0(current), -1(previous), 1(next)"""
    return f"""
        function showDiagramsBy{month_title.title().replace(' ', '')}Month() {{
            const day = new Date();
            for (let i = 0; i < {difference_month * -1}; i++)
            {{
                day.setDate(day.getDate() - getCountDaysInMonth(day));
            }}
            showDiagramsFromFirstDayToNextMonth(day);
        }}
    """