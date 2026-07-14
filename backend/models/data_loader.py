# backend/models/data_loader.py

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

class DataLoader:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.load_data()
    
    def load_data(self):
        """Load all data files"""
        # Load price data
        price_file = os.path.join(self.data_dir, 'BrentOilPrices.csv')
        self.df = pd.read_csv(price_file)
        
        # Parse dates
        def parse_dates(date_str):
            try:
                return pd.to_datetime(date_str, format='%d-%b-%y')
            except:
                try:
                    return pd.to_datetime(date_str, format='%b %d, %Y')
                except:
                    return pd.NaT
        
        self.df['Date'] = self.df['Date'].apply(parse_dates)
        self.df = self.df.dropna(subset=['Date'])
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        
        # Load events
        events_file = os.path.join(self.data_dir, 'events_dataset.csv')
        if os.path.exists(events_file):
            self.events_df = pd.read_csv(events_file)
            self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
        else:
            self.create_events_dataset()
        
        # Load associations
        assoc_file = os.path.join(self.data_dir, 'event_associations.csv')
        if os.path.exists(assoc_file):
            self.associations_df = pd.read_csv(assoc_file)
            self.associations_df['Event_Date'] = pd.to_datetime(self.associations_df['Event_Date'])
            self.associations_df['Change_Date'] = pd.to_datetime(self.associations_df['Change_Date'])
        else:
            self.associations_df = pd.DataFrame()
    
    def create_events_dataset(self):
        """Create default events dataset if not exists"""
        events_data = [
            ('1990-08-02', 'Gulf War - Kuwait Invasion', 'Geopolitical_Conflict', 'High'),
            ('1991-01-17', 'Operation Desert Storm', 'Geopolitical_Conflict', 'High'),
            ('1997-07-02', 'Asian Financial Crisis', 'Economic_Shock', 'Medium'),
            ('2001-09-11', '9/11 Attacks', 'Geopolitical_Event', 'Medium'),
            ('2003-03-20', 'Iraq War Invasion', 'Geopolitical_Conflict', 'High'),
            ('2008-09-15', 'Global Financial Crisis', 'Economic_Shock', 'Very_High'),
            ('2008-12-17', 'OPEC Production Cuts', 'OPEC_Policy', 'High'),
            ('2011-02-15', 'Arab Spring - Libya', 'Geopolitical_Conflict', 'High'),
            ('2014-06-01', 'Oil Price Crash', 'Market_Event', 'High'),
            ('2016-11-30', 'OPEC+ Agreement', 'OPEC_Policy', 'High'),
            ('2018-05-08', 'US Iran Sanctions', 'Political', 'Medium'),
            ('2020-01-30', 'COVID-19 Pandemic', 'Public_Health', 'Very_High'),
            ('2020-03-06', 'OPEC+ Dispute', 'OPEC_Policy', 'Very_High'),
            ('2022-02-24', 'Russia-Ukraine War', 'Geopolitical_Conflict', 'Very_High')
        ]
        self.events_df = pd.DataFrame(events_data, 
                                      columns=['Date', 'Event_Name', 'Category', 'Expected_Impact'])
        self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
        self.events_df.to_csv(os.path.join(self.data_dir, 'events_dataset.csv'), index=False)
    
    def get_price_data(self, start_date=None, end_date=None):
        """Get price data with optional date filtering"""
        df_filtered = self.df.copy()
        if start_date:
            df_filtered = df_filtered[df_filtered['Date'] >= start_date]
        if end_date:
            df_filtered = df_filtered[df_filtered['Date'] <= end_date]
        return df_filtered
    
    def get_price_data_json(self, start_date=None, end_date=None):
        """Get price data as JSON-serializable format"""
        df = self.get_price_data(start_date, end_date)
        return {
            'dates': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'prices': df['Price'].tolist(),
            'min_price': float(df['Price'].min()),
            'max_price': float(df['Price'].max()),
            'mean_price': float(df['Price'].mean())
        }
    
    def get_events(self):
        """Get all events"""
        return self.events_df.to_dict('records')
    
    def get_associations(self):
        """Get event associations"""
        if self.associations_df.empty:
            return []
        return self.associations_df.to_dict('records')
    
    def get_summary_stats(self):
        """Get summary statistics"""
        return {
            'total_observations': len(self.df),
            'date_range': {
                'start': self.df['Date'].min().strftime('%Y-%m-%d'),
                'end': self.df['Date'].max().strftime('%Y-%m-%d')
            },
            'price_stats': {
                'min': float(self.df['Price'].min()),
                'max': float(self.df['Price'].max()),
                'mean': float(self.df['Price'].mean()),
                'std': float(self.df['Price'].std())
            },
            'total_events': len(self.events_df),
            'total_associations': len(self.associations_df)
        }
    
    def get_impact_by_category(self):
        """Get average impact by category"""
        if self.associations_df.empty:
            return {}
        impact = self.associations_df.groupby('Category')['Percent_Change'].agg(['mean', 'std', 'count']).round(2)
        return impact.to_dict('index')