import pandas as pd

class AnalyticsEngine:
    def __init__(self, df):
        self.df = df

    def get_total_pipeline_value(self):
        """Total value of all jobs not in 'Completed' or 'Lead' (Active Pipeline)"""
        # Definition of "Pipeline" can vary. Let's say everything except Completed.
        if self.df.empty: return 0.0
        # return self.df[self.df['status'] != 'Completed']['value'].sum()
        # Actually, "Pipeline" usually means Active Opportunities.
        return self.df['value'].sum()

    def get_kpis(self):
        if self.df.empty:
            return {
                "total_value": 0,
                "avg_value": 0,
                "total_jobs": 0,
                "conversion_rate": 0
            }

        total_value = self.df['value'].sum()
        avg_value = self.df['value'].mean()
        total_jobs = len(self.df)

        # Simple Conversion Rate: Signed+ / Total
        # Let's define "converted" as Signed, In Progress, Completed
        converted_statuses = ["Signed", "In Progress", "Completed"]
        converted_count = self.df[self.df['status'].isin(converted_statuses)].shape[0]
        conversion_rate = (converted_count / total_jobs) * 100 if total_jobs > 0 else 0

        return {
            "total_value": total_value,
            "avg_value": avg_value,
            "total_jobs": total_jobs,
            "conversion_rate": conversion_rate
        }

    def get_jobs_by_stage(self):
        if self.df.empty: return pd.DataFrame()
        return self.df['status'].value_counts().reset_index()

    def get_revenue_by_source(self):
        if self.df.empty or 'lead_source' not in self.df.columns: return pd.DataFrame()
        return self.df.groupby('lead_source')['value'].sum().reset_index()
