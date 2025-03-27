from UI import UI_statistics


def get_func_get_models_diagram_data(models_diagram_data: str) -> str:
    return f"""
        function getModelsDiagramData()
        {{
            data = {models_diagram_data};
            return [...data];
        }}
    """

def get_func_show_models_diagram_by_dates_filter() -> str:
    return """
        function showModelsDiagramByDatesFilter(startDate, endDate) 
        {
            data = getModelsDiagramData();
            const filteredData = data.filter(item => 
            {
                const date = new Date(item.date);
                return date >= startDate && date <= endDate;
            });
            showModelsDiagram(filteredData)
        }
    """

def get_func_show_models_diagram_by_dates() -> str:
    return """
        function showModelsDiagramByDates() 
        {
            data = getModelsDiagramData();
            showModelsDiagram(data)
        }
    """

def get_func_show_models_diagram(models_diagram_layout: str, currency: str) -> str:
    return f"""
        function showModelsDiagram(data)
        {{
            const incomeSumData = [];
            const countData = [];

            const income = data.reduce((sum, row) => sum + row.income_sum, 0);
            const priceSelling = data.reduce((sum, row) => sum + row.price_selling_sum, 0);
            const pricePurchase = data.reduce((sum, row) => sum + row.price_purchase_sum, 0);
            const charges = data.reduce((sum, row) => sum + row.charges_sum, 0);
            const orders_count = data.reduce((sum, row) => sum + row.orders_count, 0);

            incomeSumData.push(
                {{
                    x: ['{UI_statistics.get_total_models()}'],
                    y: [income],   
                    type: 'histogram',
                    histfunc: "sum",
                    domain: {{ row: 0, column: 0 }},
                    marker: {{ color: 'gray' }},
                    xaxis: "x1",
                    yaxis: "y1",
                    hovertemplate:
                        `{UI_statistics.get_profit()}: <span style="color:${{income >= 0 ? 'green' : 'red'}};">${{income.toFixed(2).replace(str_regex, ",")}} {currency} (${{(income / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `{UI_statistics.get_income()}: <span style="color:green;">${{priceSelling.toFixed(2).replace(str_regex, ",")}} {currency}</span><br>` +
                        `{UI_statistics.get_spent()}: <span style="color:red;">${{(pricePurchase + charges).toFixed(2).replace(str_regex, ",")}} {currency} (${{((pricePurchase + charges) / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `    {UI_statistics.get_price_purchase()}: <span style="color:red;">${{pricePurchase.toFixed(2).replace(str_regex, ",")}} {currency} (${{(pricePurchase / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `    {UI_statistics.get_charges()}: <span style="color:red;">${{charges.toFixed(2).replace(str_regex, ",")}} {currency} (${{(charges / priceSelling * 100).toFixed(2)}}%)</span>` +
                        '<extra></extra>'
                    ,
                    name: "{UI_statistics.get_total_models()}",
                    showlegend: true,
                    legendgroup: "{UI_statistics.get_total_models()}"
                }});

            countData.push(
                {{
                    histfunc: "sum",
                    x: ['{UI_statistics.get_total_models()}'],  
                    y: [data.reduce((sum, row) => sum + row.orders_count, 0)],   
                    type: "histogram",
                    domain: {{ row: 0, column: 1 }},
                    showlegend: false,
                    legendgroup: "{UI_statistics.get_total_models()}",
                    name: "{UI_statistics.get_total_models()}",
                    xaxis: "x2",
                    yaxis: "y2",
                    marker: {{ color: 'gray' }}
                }});



            const groupedData = data.reduce((acc, row) => 
            {{
                const model = row.model;
                if (!acc[model]) 
                {{
                    acc[model] = 
                    {{
                        income_sum: 0,
                        price_selling_sum: 0,
                        price_purchase_sum: 0,
                        charges_sum: 0,
                        orders_count: 0,
                        trace_color: null
                    }};
                }}
                acc[model].income_sum += row.income_sum;
                acc[model].price_selling_sum += row.price_selling_sum;
                acc[model].price_purchase_sum += row.price_purchase_sum;
                acc[model].charges_sum += row.charges_sum;
                acc[model].orders_count += row.orders_count;
                acc[model].trace_color = row.trace_color;
                return acc;
            }}, {{}});

            const models = Object.keys(groupedData);

            str_regex = /\\B(?=(\\d{{3}})+(?!\\d))/g
            models.forEach(model => 
            {{
                const currentData = groupedData[model];
                const income = currentData.income_sum;
                const priceSelling = currentData.price_selling_sum;
                const pricePurchase = currentData.price_purchase_sum;
                const charges = currentData.charges_sum;
                const trace_color = currentData.trace_color;
                const orders_count = currentData.orders_count;

                incomeSumData.push(
                {{
                    x: [model],
                    y: [income],
                    type: 'histogram',
                    histfunc: "sum",
                    domain: {{ row: 0, column: 0 }},
                    marker: {{ color: trace_color }},
                    xaxis: "x1",
                    yaxis: "y1",
                    hovertemplate:
                        `{UI_statistics.get_profit()}: <span style="color:${{income >= 0 ? 'green' : 'red'}};">${{income.toFixed(2).replace(str_regex, ",")}} {currency} (${{(income / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `{UI_statistics.get_income()}: <span style="color:green;">${{priceSelling.toFixed(2).replace(str_regex, ",")}} {currency}</span><br>` +
                        `{UI_statistics.get_spent()}: <span style="color:red;">${{(pricePurchase + charges).toFixed(2).replace(str_regex, ",")}} {currency} (${{((pricePurchase + charges) / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `    {UI_statistics.get_price_purchase()}: <span style="color:red;">${{pricePurchase.toFixed(2).replace(str_regex, ",")}} {currency} (${{(pricePurchase / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `    {UI_statistics.get_charges()}: <span style="color:red;">${{charges.toFixed(2).replace(str_regex, ",")}} {currency} (${{(charges / priceSelling * 100).toFixed(2)}}%)</span>` +
                        '<extra></extra>'
                    ,
                    name: model,
                    showlegend: true,
                    legendgroup: model
                }});

                countData.push(
                {{
                    x: [model],
                    y: [orders_count],
                    histfunc: "sum",
                    type: 'histogram',
                    domain: {{ row: 0, column: 1 }},
                    marker: {{ color: trace_color }},
                    xaxis: "x2",
                    yaxis: "y2",
                    name: model,
                    showlegend: false,
                    legendgroup: model
                }});
            }});


            const layout = {models_diagram_layout}
            layout.grid = {{ rows: 1, columns: 2}}

            Plotly.react('models-diagram', [...incomeSumData, ...countData], layout);

        }}
    """