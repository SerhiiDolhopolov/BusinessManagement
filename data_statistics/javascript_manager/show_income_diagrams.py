def get_func_get_income_diagram_figure_by_dates(income_diagram_figure_by_dates: str) -> str:
    return f"""
        function getIncomeDiagramFigureByDates()
        {{
            var figure = {income_diagram_figure_by_dates};
            return {{...figure}};
        }}
    """

def get_func_show_income_diagram_by_dates_filter() -> str:
    return """
        function showIncomeDiagramByDatesFilter(startDate, endDate) 
        {
            showIncomeDiagram(getIncomeDiagramFigureByDates(), true, startDate, endDate)
        }
    """
def get_func_show_income_diagram_by_dates() -> str:
    return """
        function showIncomeDiagramByDates() 
        {
            showIncomeDiagram(getIncomeDiagramFigureByDates())
        }
        """

def get_func_show_income_diagram_by_months(income_diagram_figure_by_months: str) -> str:
    return f"""
        function showIncomeDiagramByMonths() 
        {{
            showIncomeDiagram({income_diagram_figure_by_months})
        }}
        """

def get_func_show_income_diagram_by_years(income_diagram_figure_by_years: str) -> str:
    return f"""
        function showIncomeDiagramByYears() 
        {{
            showIncomeDiagram({income_diagram_figure_by_years})
        }}
        """

def get_func_show_income_diagram(currency: str) -> str:
    return f"""
        function showIncomeDiagram(figure, is_filter_by_date = false, startDate = null, endDate = null)
        {{
            let minValue = [Infinity, Infinity, Infinity];
            let minValueDate = [null, null, null];
            let maxValue = [-Infinity, -Infinity, -Infinity];
            let maxValueDate = [null, null, null];
            let sumValue = [0, 0, 0];

            figure.data.forEach((trace, index) => 
            {{
                const filteredDates = [];
                const filteredYValues = [];
                const filteredCustomData = trace.customdata ? [] : null;
                for (let i = 0; i < trace.x.length; i++) 
                {{
                    const dateTime = new Date(trace.x[i]);

                    if (is_filter_by_date == true)
                    {{
                        if (!(dateTime >= startDate && dateTime <= endDate))
                            continue;
                    }}

                    filteredDates.push(trace.x[i]);
                    filteredYValues.push(trace.y[i]);
                    if (filteredCustomData) 
                    {{
                        filteredCustomData.push(trace.customdata[i]);
                    }}

                    if (trace.y[i] < minValue[index]) 
                    {{
                        minValue[index] = trace.y[i];
                        minValueDate[index] = trace.x[i].toString().replace("T00:00:00", "");
                    }}
                    if (trace.y[i] > maxValue[index]) 
                    {{
                        maxValue[index] = trace.y[i];
                        maxValueDate[index] = trace.x[i].toString().replace("T00:00:00", "");
                    }}
                    sumValue[index] += trace.y[i];

                }}

                trace.x = filteredDates;
                trace.y = filteredYValues;
                if (filteredCustomData) 
                {{
                    trace.customdata = filteredCustomData;
                }}
            }});

            str_regex = /\\B(?=(\\d{{3}})+(?!\\d))/g
            for (const i of [['purchase', 0], ['was-spent', 1], ['income', 2]]) 
            {{
                document.getElementById(`${{i[0]}}-min`).innerText = `${{minValue[i[1]].toFixed(2).replace(str_regex, ",")}} {currency}   |   ${{minValueDate[i[1]]}}`;
                document.getElementById(`${{i[0]}}-avg`).innerText = `${{(sumValue[i[1]] / figure.data[0].x.length).toFixed(2).replace(str_regex, ",")}} {currency}`;
                document.getElementById(`${{i[0]}}-max`).innerText = `${{maxValue[i[1]].toFixed(2).replace(str_regex, ",")}} {currency}  |   ${{maxValueDate[i[1]]}}`;
                document.getElementById(`${{i[0]}}-sum`).innerText = `${{sumValue[i[1]].toFixed(2).replace(str_regex, ",")}} {currency}`;
            }}

            Plotly.react('income-diagram', figure.data, figure.layout);
        }}
    """