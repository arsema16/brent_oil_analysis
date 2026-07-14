# backend/api/routes.py

from flask import jsonify, request
from models.data_loader import DataLoader
from datetime import datetime

data_loader = DataLoader()

def register_routes(app):
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'API is running'})
    
    @app.route('/api/prices', methods=['GET'])
    def get_prices():
        """Get price data with optional date filtering"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        data = data_loader.get_price_data_json(start_date, end_date)
        return jsonify(data)
    
    @app.route('/api/events', methods=['GET'])
    def get_events():
        """Get all events"""
        events = data_loader.get_events()
        # Convert datetime objects to strings
        for event in events:
            event['Date'] = event['Date'].strftime('%Y-%m-%d')
        return jsonify(events)
    
    @app.route('/api/associations', methods=['GET'])
    def get_associations():
        """Get event associations"""
        associations = data_loader.get_associations()
        for assoc in associations:
            assoc['Event_Date'] = assoc['Event_Date'].strftime('%Y-%m-%d')
            assoc['Change_Date'] = assoc['Change_Date'].strftime('%Y-%m-%d')
        return jsonify(associations)
    
    @app.route('/api/summary', methods=['GET'])
    def get_summary():
        """Get summary statistics"""
        return jsonify(data_loader.get_summary_stats())
    
    @app.route('/api/impact-by-category', methods=['GET'])
    def get_impact_by_category():
        """Get impact by category"""
        return jsonify(data_loader.get_impact_by_category())
    
    @app.route('/api/events/<event_id>', methods=['GET'])
    def get_event_detail(event_id):
        """Get detailed information about a specific event"""
        events = data_loader.get_events()
        for event in events:
            if event['Event_Name'] == event_id:
                event['Date'] = event['Date'].strftime('%Y-%m-%d')
                return jsonify(event)
        return jsonify({'error': 'Event not found'}), 404
    
    @app.route('/api/price-range', methods=['GET'])
    def get_price_range():
        """Get min and max dates for price data"""
        df = data_loader.df
        return jsonify({
            'min_date': df['Date'].min().strftime('%Y-%m-%d'),
            'max_date': df['Date'].max().strftime('%Y-%m-%d')
        })