from UI import UI_statistics

def get_html_header() -> str:
    return f"""
    <header id="navbar" class="navbar">
        <div class="container">
            <nav>
                <ul class="menu">
                    <div class='filter-block' style='display:block;'>
                        <li style='grid-row:1'>
                            <button onclick="showDiagramsByDates()">{UI_statistics.get_by_days()}</button>
                            <button onClick="showDiagramsByMonths()">{UI_statistics.get_by_months()}</button>
                            <button onClick="showDiagramsByYears()">{UI_statistics.get_by_years()}</button>
                        </li>
                        <li style='grid-row:2'>
                            <p id="diagram-info">{UI_statistics.get_all_statistic()}</p>
                        </li>
                    </div>
                    <div class='filter-block' style='display:block;'>
                        <li style='grid-row:1'>
                            <button onClick="showDiagramsByPreviousWeek()">{UI_statistics.get_for_preview_week()}</button>
                            <button onClick="showDiagramsByCurrentWeek()">{UI_statistics.get_for_current_week()}</button>
                            <button onClick="showDiagramsBy7Days()">{UI_statistics.get_for_7_days()}</button>
                        </li>
                        <li style='grid-row:2'>
                            <button onClick="showDiagramsByPreviousMonth()">{UI_statistics.get_for_preview_month()}</button>
                            <button onClick="showDiagramsByCurrentMonth()">{UI_statistics.get_for_current_month()}</button>
                            <button onClick="showDiagramsBy30Days()">{UI_statistics.get_for_30_days()}</button>
                            <button onClick="showDiagramsBy31Days()">{UI_statistics.get_for_31_days()}</button>
                        </li>
                    </div>
                    <div class='filter-block'>
                        <li>
                            <input type="text" id="start-date" placeholder="DD.MM.YYYY" pattern="{r'\d{1,2}\D\d{1,2}\D\d{4}'}" required">
                            <label for="end_date">:</label>
                            <input type="text" id="end-date" placeholder="DD.MM.YYYY" pattern="{r'\d{1,2}\D\d{1,2}\D\d{4}'}" required">
                            <button onclick="showDiagramsByDatesFilter()">{UI_statistics.get_apply_filter()}</button>
                        </li>
                    </div>
                </ul>
            </nav>
        </div>
    </header>
"""