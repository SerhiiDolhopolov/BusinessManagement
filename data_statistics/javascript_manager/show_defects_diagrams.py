from UI import UI_statistics


def get_func_get_defects_diagram_data(defects_diagram_data: str) -> str:
    return f"""
        function getDefectsDiagramData()
        {{
            data = {defects_diagram_data};
            return [...data];
        }}
    """

def get_func_show_defects_diagram_by_dates_filter() -> str:
    return """
        function showDefectsDiagramByDatesFilter(startDate, endDate) 
        {
            data = getDefectsDiagramData();
            const filteredData = data.filter(item => 
            {
                const date = new Date(item.date);
                return date >= startDate && date <= endDate;
            });
            showDefectsDiagram(filteredData)
        }
    """

def get_func_show_defects_diagram_by_dates() -> str:
    return """
        function showDefectsDiagramByDates() 
        {
            data = getDefectsDiagramData();
            showDefectsDiagram(data)
        }
    """

def get_func_show_defects_diagram(defects_diagram_layout: str, currency: str) -> str:
    return f"""
        function showDefectsDiagram(data)
        {{

            const incomeSumData = [];
            const countData = [];
            const withoutDefects = data.filter(item => item.defect === '{UI_statistics.get_without_defect()}');
            data = data.filter(item => item.defect !== '{UI_statistics.get_without_defect()}');

            countData.push(
                {{
                    histfunc: "sum",
                    x: data.map(item => item.model),     
                    y: data.map(item => item.orders_count),   
                    type: "histogram",
                    domain: {{ row: 1, column: 0 }},
                    showlegend: true,
                    legendgroup: "{UI_statistics.get_total_defects()}",
                    name: "{UI_statistics.get_total_defects()}",
                    xaxis: "x2",
                    yaxis: "y2",
                    marker: {{ color: 'gray' }}
                }});

            incomeSumData.push(
            {{
                histfunc: "sum",
                x: withoutDefects.map(item => item.model),     
                y: withoutDefects.map(item => item.income_sum),      
                type: "histogram", 
                name: "{UI_statistics.get_without_defect()}",
                domain: {{ row: 0, column: 0 }},
                showlegend: true,
                legendgroup: "{UI_statistics.get_without_defect()}",
                xaxis: "x1",
                yaxis: "y1",
                marker: {{ color: withoutDefects.map(item => item.trace_color) }},
                hovertemplate: "%{{y:.2f}} {currency}"
            }});
            countData.push(
            {{
                histfunc: "sum",
                x: withoutDefects.map(item => item.model),     
                y: withoutDefects.map(item => item.orders_count),    
                type: "histogram",
                name: "{UI_statistics.get_without_defect()}",
                domain: {{ row: 1, column: 0 }},
                showlegend: false,
                legendgroup: "{UI_statistics.get_without_defect()}",
                xaxis: "x2",
                yaxis: "y2",
                marker: {{ color: withoutDefects.map(item => item.trace_color)  }}
            }});


            const groupedData = data.reduce((acc, item) => 
            {{
                if (!acc[item.defect]) 
                {{
                    acc[item.defect] = {{ model: [], income_sum: [], trace_color: [], orders_count: []}};
                }}
                acc[item.defect].model.push(item.model);
                acc[item.defect].income_sum.push(item.income_sum);
                acc[item.defect].orders_count.push(item.orders_count);
                acc[item.defect].trace_color.push(item.trace_color);
                return acc;
            }}, {{}});
            for (let defect in groupedData) 
            {{
                const model = groupedData[defect].model;
                const income_sum = groupedData[defect].income_sum;
                const orders_count = groupedData[defect].orders_count;
                const trace_color = groupedData[defect].trace_color;
                incomeSumData.push(
                {{
                    histfunc: "sum",
                    x: model,     
                    y: income_sum,      
                    type: "histogram", 
                    name: defect,
                    domain: {{ row: 0, column: 0 }},
                    showlegend: true,
                    legendgroup: defect,
                    xaxis: "x1",
                    yaxis: "y1",
                    marker: {{ color: trace_color }},
                    hovertemplate: "%{{y:.2f}} {currency}"
                }});
                countData.push(
                {{
                    histfunc: "sum",
                    x: model,     
                    y: orders_count,   
                    type: "histogram",
                    name: defect,
                    domain: {{ row: 1, column: 0 }},
                    showlegend: false,
                    legendgroup: defect,
                    xaxis: "x2",
                    yaxis: "y2",
                    marker: {{ color: trace_color }}
                }});
            }}

            const layout = {defects_diagram_layout}
            layout.grid = {{ rows: 2, columns: 1}}

            Plotly.react('defects-diagram', [...incomeSumData, ...countData], layout);
        }}
    """