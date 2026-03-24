import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class Visualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")

    def create_performance_comparison_charts(self, results_df):
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Среднее время чтения', 'Среднее время записи',
                          'Среднее время обновления', 'Среднее время поиска'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )

        operations = ['read', 'write', 'update', 'search']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        for idx, operation in enumerate(operations):
            row = (idx // 2) + 1
            col = (idx % 2) + 1

            op_data = results_df[results_df['operation'] == operation]

            for i, db_type in enumerate(op_data['database'].unique()):
                db_data = op_data[op_data['database'] == db_type]

                fig.add_trace(
                    go.Bar(
                        x=[f"{method}<br>({db_type})" for method in db_data['method']],
                        y=db_data['avg_time_ms'],
                        name=f"{db_type}",
                        marker_color=colors[i % len(colors)]
                    ),
                    row=row, col=col
                )

        fig.update_layout(height=800, showlegend=True, title_text="Сравнение производительности по операциям и методам")
        fig.update_xaxes(title_text="Метод хранения (База данных)")
        fig.update_yaxes(title_text="Время (мс)")

        return fig

    def create_heatmap(self, results_df):
        pivot_data = results_df.pivot_table(
            values='avg_time_ms',
            index=['database', 'method'],
            columns='operation',
            aggfunc='mean'
        ).fillna(0)

        pivot_data = pivot_data.reset_index()

        fig = go.Figure(data=go.Heatmap(
            z=pivot_data[['read', 'write', 'update', 'search']].values,
            x=['read', 'write', 'update', 'search'],
            y=[f"{row['database']}-{row['method']}" for _, row in pivot_data.iterrows()],
            colorscale='Viridis',
            text=np.round(pivot_data[['read', 'write', 'update', 'search']].values, 2),
            texttemplate="%{text}мс",
            textfont={"size": 10},
        ))

        fig.update_layout(
            title="Тепловая карта производительности: среднее время по методам и операциям",
            xaxis_title="Операция",
            yaxis_title="Комбинация База данных-Метод"
        )

        return fig

    def create_radar_chart(self, results_df, db_type, operation):
        filtered_data = results_df[(results_df['database'] == db_type) &
                                  (results_df['operation'] == operation)]

        categories = filtered_data['method'].tolist()
        values = filtered_data['avg_time_ms'].tolist()

        max_val = max(values) if values else 1
        if max_val > 0:
            values = [(v / max_val) * 100 for v in values]

        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=f'{db_type} - {operation}'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title=f"Диаграмма: {db_type} - {operation} Производительность"
        )

        return fig

    def create_trend_analysis(self, results_df):
        fig = go.Figure()

        for operation in results_df['operation'].unique():
            op_data = results_df[results_df['operation'] == operation]
            for method in op_data['method'].unique():
                method_data = op_data[op_data['method'] == method]
                for db in method_data['database'].unique():
                    db_data = method_data[method_data['database'] == db]
                    fig.add_trace(go.Box(
                        y=db_data['avg_time_ms'],
                        name=f"{method}<br>({db})-{operation}",
                        boxmean=True
                    ))

        fig.update_layout(
            title="Распределение времени производительности по методу, базе данных и операции",
            yaxis_title="Время (мс)",
            xaxis_title="Метод (База данных)-Операция"
        )

        return fig

    def generate_all_visualizations(self, results_df):
        visualizations = {}

        if results_df.empty:
            print("Нет данных для визуализации")
            return visualizations

        try:
            visualizations['comparison_bars'] = self.create_performance_comparison_charts(results_df)
            visualizations['heatmap'] = self.create_heatmap(results_df)
            visualizations['trend_analysis'] = self.create_trend_analysis(results_df)

            for db_type in results_df['database'].unique():
                for operation in results_df['operation'].unique():
                    key = f"radar_{db_type}_{operation}"
                    visualizations[key] = self.create_radar_chart(results_df, db_type, operation)

        except Exception as e:
            print(f"Ошибка генерации визуализаций: {e}")

        return visualizations

    def save_visualization(self, fig, filepath, format='html'):
        if format.lower() == 'html':
            fig.write_html(filepath)
        elif format.lower() == 'png':
            fig.write_image(filepath)
        elif format.lower() == 'pdf':
            fig.write_image(filepath)
        else:
            raise ValueError(f"Неподдерживаемый формат: {format}")

        print(f"Визуализация сохранена в {filepath}")

    def show_visualization(self, fig):
        fig.show()
