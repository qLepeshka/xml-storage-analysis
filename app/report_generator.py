import pandas as pd
from datetime import datetime
import os


class ReportGenerator:
    def __init__(self):
        self.template_dir = "templates"
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")

        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except FileExistsError:
            pass

    def generate_report(self, test_results, visualizations=None):
        if isinstance(test_results, dict):
            df = self._convert_results_to_dataframe(test_results)
        else:
            df = test_results

        report_content = self._create_report_content(df, visualizations)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"xml_storage_analysis_report_{timestamp}.html"
        report_path = os.path.join(self.output_dir, report_filename)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"Отчёт сгенерирован: {report_path}")
        return report_path

    def _convert_results_to_dataframe(self, test_results):
        rows = []

        for db_type, db_results in test_results.items():
            for method_name, method_results in db_results.items():
                for operation, op_result in method_results.items():
                    row = {
                        'database': db_type,
                        'method': method_name,
                        'operation': operation,
                        'avg_time_ms': op_result['avg_time'],
                        'min_time_ms': op_result['min_time'],
                        'max_time_ms': op_result['max_time'],
                        'std_dev_ms': op_result['std_dev']
                    }
                    rows.append(row)

        return pd.DataFrame(rows)

    def _create_report_content(self, df, visualizations=None):
        html_content = [
            "<!DOCTYPE html>",
            "<html lang='ru'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            "    <title>Отчёт по сравнительному анализу методов хранения XML</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
            "        h1, h2, h3 { color: #2c3e50; }",
            "        table { border-collapse: collapse; width: 100%; margin: 20px 0; }",
            "        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }",
            "        th { background-color: #34495e; color: white; }",
            "        tr:nth-child(even) { background-color: #f2f2f2; }",
            "        .summary-box { background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }",
            "        .recommendation { background-color: #d5f4e6; padding: 15px; border-left: 5px solid #27ae60; margin: 20px 0; }",
            "        .visualization { margin: 30px 0; }",
            "    </style>",
            "</head>",
            "<body>",
            f"    <h1>Отчёт по сравнительному анализу методов хранения XML</h1>",
            f"    <p><strong>Сгенерировано:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
            self._create_summary_section(df),
            self._create_detailed_results_section(df),
            self._create_recommendations_section(df),
            self._create_visualizations_section(visualizations),
            "    </body>",
            "</html>"
        ]

        return "\n".join(html_content)

    def _create_summary_section(self, df):
        total_tests = len(df)
        databases = df['database'].unique()
        methods = df['method'].unique()
        operations = df['operation'].unique()

        fastest_row = df.loc[df['avg_time_ms'].idxmin()] if not df.empty else None

        summary_html = [
            "    <div class='summary-box'>",
            "        <h2>Основное резюме</h2>",
            f"        <p>Всего тестов выполнено: {total_tests}</p>",
            f"        <p>Протестировано баз данных: {', '.join(databases)}</p>",
            f"        <p>Оценено методов хранения: {', '.join(methods)}</p>",
            f"        <p>Измерено операций: {', '.join(operations)}</p>"
        ]

        if fastest_row is not None:
            summary_html.append(
                f"        <p>Самая быстрая операция: {fastest_row['operation']} используя {fastest_row['method']} на {fastest_row['database']} "
                f"(среднее время: {fastest_row['avg_time_ms']:.2f} мс)</p>"
            )

        summary_html.extend([
            "    </div>"
        ])

        return "\n".join(summary_html)

    def _create_detailed_results_section(self, df):
        detailed_html = [
            "    <h2>Подробные результаты</h2>",
            "    <h3>Производительность по базе данных и методу</h3>"
        ]

        grouped = df.groupby(['database', 'method']).agg({
            'avg_time_ms': ['mean', 'min', 'max', 'std']
        }).round(2)

        grouped.columns = ['_'.join(col).strip() for col in grouped.columns]
        grouped = grouped.reset_index()

        detailed_html.append("    <table>")
        detailed_html.append("        <thead>")
        detailed_html.append("            <tr>")
        detailed_html.extend([f"                <th>{col}</th>" for col in grouped.columns])
        detailed_html.append("            </tr>")
        detailed_html.append("        </thead>")
        detailed_html.append("        <tbody>")

        for _, row in grouped.iterrows():
            detailed_html.append("            <tr>")
            for val in row:
                detailed_html.append(f"                <td>{val}</td>")
            detailed_html.append("            </tr>")

        detailed_html.extend([
            "        </tbody>",
            "    </table>",
            "    <h3>Производительность по операциям</h3>"
        ])

        op_grouped = df.groupby(['operation']).agg({
            'avg_time_ms': ['mean', 'min', 'max', 'std']
        }).round(2)

        op_grouped.columns = ['_'.join(col).strip() for col in op_grouped.columns]
        op_grouped = op_grouped.reset_index()

        detailed_html.append("    <table>")
        detailed_html.append("        <thead>")
        detailed_html.append("            <tr>")
        detailed_html.extend([f"                <th>{col}</th>" for col in op_grouped.columns])
        detailed_html.append("            </tr>")
        detailed_html.append("        </thead>")
        detailed_html.append("        <tbody>")

        for _, row in op_grouped.iterrows():
            detailed_html.append("            <tr>")
            for val in row:
                detailed_html.append(f"                <td>{val}</td>")
            detailed_html.append("            </tr>")

        detailed_html.extend([
            "        </tbody>",
            "    </table>"
        ])

        return "\n".join(detailed_html)

    def _create_recommendations_section(self, df):
        recommendations_html = [
            "    <div class='recommendation'>",
            "        <h2>Рекомендации</h2>"
        ]

        for operation in df['operation'].unique():
            op_data = df[df['operation'] == operation]
            if not op_data.empty:
                best_method_row = op_data.loc[op_data['avg_time_ms'].idxmin()]
                recommendations_html.append(
                    f"        <h3>Для операций {self._translate_operation(operation)}:</h3>"
                    f"        <p>Лучший метод: <strong>{best_method_row['method']}</strong> на <strong>{best_method_row['database']}</strong> "
                    f"(среднее время: {best_method_row['avg_time_ms']:.2f} мс)</p>"
                )

        avg_by_method = df.groupby('method')['avg_time_ms'].mean().sort_values()
        best_overall_method = avg_by_method.index[0]

        recommendations_html.append(
            f"        <h3>Лучший метод в целом:</h3>"
            f"        <p>Метод <strong>{best_overall_method}</strong> показывает наилучшую общую производительность по всем операциям.</p>"
        )

        recommendations_html.extend([
            "        <h3>Рекомендации по выбору:</h3>",
            "        <ul>",
            "            <li><strong>Native Text Storage</strong>: Лучше всего для простого хранения с минимальными запросами</li>",
            "            <li><strong>Normalized Relational</strong>: Лучше всего для сложных запросов и связей</li>",
            "            <li><strong>XML Data Type</strong>: Лучше всего для баз данных с нативной поддержкой XML и XQuery</li>",
            "            <li><strong>Hybrid Approach</strong>: Лучше всего для смешанных сценариев с структурированным и неструктурированным доступом</li>",
            "        </ul>",
            "    </div>"
        ])

        return "\n".join(recommendations_html)

    def _create_visualizations_section(self, visualizations):
        if not visualizations:
            return "    <!-- Визуализации не предоставлены -->"

        viz_html = [
            "    <h2>Визуализации</h2>"
        ]

        for name, viz in visualizations.items():
            viz_html.append(f"    <div class='visualization'>")
            viz_html.append(f"        <h3>{name.replace('_', ' ').title()}</h3>")
            viz_html.append(f"        <p>Визуализация: {name}</p>")
            viz_html.append(f"    </div>")

        return "\n".join(viz_html)

    def _translate_operation(self, operation):
        translations = {
            'read': 'чтения',
            'write': 'записи',
            'update': 'обновления',
            'search': 'поиска'
        }
        return translations.get(operation, operation)
