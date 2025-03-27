from UI import UI_statistics


def get_func_get_users_diagram_data(users_diagram_data: str) -> str:
    return f"""
        function getUsersDiagramData()
        {{
            data = {users_diagram_data};
            return [...data];
        }}
    """

def get_func_show_users_diagram_by_dates_filter() -> str:
    return """
        function showUsersDiagramByDatesFilter(startDate, endDate) 
        {
            data = getUsersDiagramData();
            const filteredData = data.filter(item => 
            {
                const date = new Date(item.date);
                return date >= startDate && date <= endDate;
            });
            showUsersDiagram(filteredData)
        }
    """

def get_func_show_users_diagram_by_dates() -> str:
    return """
        function showUsersDiagramByDates() 
        {
            data = getUsersDiagramData();
            showUsersDiagram(data)
        }
    """

def get_func_show_users_diagram(users_diagram_layout: str, currency: str) -> str:
    return f"""
        function showUsersDiagram(data)
        {{
            const groupedData = data.reduce((acc, row) => 
            {{
                const username = row.username;
                if (!acc[username]) 
                {{
                    acc[username] = 
                    {{
                        income_sum: 0,
                        price_selling_sum: 0,
                        price_purchase_sum: 0,
                        charges_sum: 0,
                        orders_count: 0
                    }};
                }}
                acc[username].income_sum += row.income_sum;
                acc[username].price_selling_sum += row.price_selling_sum;
                acc[username].price_purchase_sum += row.price_purchase_sum;
                acc[username].charges_sum += row.charges_sum;
                acc[username].orders_count += row.orders_count;
                return acc;
            }}, {{}});

            const usernames = Object.keys(groupedData);
            const barTraces = [];

            str_regex = /\\B(?=(\\d{{3}})+(?!\\d))/g
            usernames.forEach(username => 
            {{
                const currentData = groupedData[username];
                const income = currentData.income_sum;
                const priceSelling = currentData.price_selling_sum;
                const pricePurchase = currentData.price_purchase_sum;
                const charges = currentData.charges_sum;

                barTraces.push(
                {{
                    x: [username],
                    y: [income],
                    type: 'bar',
                    hovertemplate:
                        `{UI_statistics.get_profit()}: <span style="color:${{income >= 0 ? 'green' : 'red'}};">${{income.toFixed(2).replace(str_regex, ",")}} {currency} (${{(income / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `{UI_statistics.get_income()}: <span style="color:green;">${{priceSelling.toFixed(2).replace(str_regex, ",")}} {currency}</span><br>` +
                        `{UI_statistics.get_spent()}: <span style="color:red;">${{(pricePurchase + charges).toFixed(2).replace(str_regex, ",")}} {currency} (${{((pricePurchase + charges) / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `    {UI_statistics.get_price_purchase()}: <span style="color:red;">${{pricePurchase.toFixed(2).replace(str_regex, ",")}} {currency} (${{(pricePurchase / priceSelling * 100).toFixed(2)}}%)</span><br>` +
                        `    {UI_statistics.get_charges()}: <span style="color:red;">${{charges.toFixed(2).replace(str_regex, ",")}} {currency} (${{(charges / priceSelling * 100).toFixed(2)}}%)</span>` +
                        '<extra></extra>'
                    ,
                    name: username,
                    showlegend: false
                }});
            }});


            const ordersCountData = 
            {{
                values: data.map(item => item.orders_count),
                labels: data.map(item => item.username),
                type: "pie",
                name: "Orders Count",
                hole: 0.3,
                textinfo: 'percent+label',
                textposition: 'inside',
                domain: {{ row: 0, column: 1 }},
                hovertemplate: '%{{label}}<br>%{{value}} телефонов<br>%{{percent}}<extra></extra>'
            }};

            const layout = {users_diagram_layout}
            layout.grid = {{ rows: 1, columns: 2 }}
            Plotly.react('users-diagram', [...barTraces, ordersCountData], layout);
        }}
    """