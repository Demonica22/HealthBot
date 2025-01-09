from jinja2 import Template

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Illness Table</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>Illness Table</h1>
    <table>
        <thead>
            <tr>
                <th>Description</th>
                <th>Date From</th>
                <th>Date To</th>
                <th>Still Sick</th>
                <th>Title</th>
                <th>Treatment Plan</th>
            </tr>
        </thead>
        <tbody>
            {% for illness in diseases %}
            <tr>
                <td>{{ illness.description }}</td>
                <td>{{ illness.date_from }}</td>
                <td>{{ illness.date_to if illness.date_to else "N/A" }}</td>
                <td>{{ "Yes" if illness.still_sick else "No" }}</td>
                <td>{{ illness.title }}</td>
                <td>{{ illness.treatment_plan }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""


async def get_diseases_template(diseases: list[dict]) -> Template:
    template = Template(html_template)
    rendered_html = template.render(diseases=diseases)
    return rendered_html
