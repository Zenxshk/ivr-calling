from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# 📌 CONFIGURATION - SET THIS IN RENDER ENVIRONMENT VARIABLES
GOOGLE_SHEET_ID = os.environ.get('12oP1qNlGEgkEx7xypUojoyHO5yuIKAx6SnhKcVN3Uew', 'your_google_sheet_id_here')

def get_sheet_data(sheet_name='Sheet1'):
    """Fetch data from Google Sheets using Visualization API (No auth needed)"""
    url = f"https://docs.google.com/spreadsheets/d/12oP1qNlGEgkEx7xypUojoyHO5yuIKAx6SnhKcVN3Uew/edit?gid=0#gid=0"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Remove Google's JS wrapper and parse JSON
        text = response.text
        if text.startswith('/*O_o*/'):
            text = text[47:-2]  # Remove Google's JS wrapper
        data = json.loads(text)
        
        return data
        
    except Exception as e:
        raise Exception(f"Failed to fetch sheet data: {str(e)}")

def process_sheet_data(data):
    """Convert Google Visualization data to clean JSON"""
    if not data or 'table' not in data:
        return []
    
    rows = [row['c'] for row in data['table']['rows']]
    
    if not rows:
        return []
    
    # Extract headers (first row)
    headers = []
    if rows[0]:
        headers = [cell['v'] if cell and 'v' in cell else f"column_{i}" for i, cell in enumerate(rows[0])]
    
    # Process data rows
    processed_data = []
    for row_index, row in enumerate(rows[1:], start=1):  # Skip header row
        if not row:
            continue
            
        item = {"id": row_index}
        for i, cell in enumerate(row):
            header_name = headers[i] if i < len(headers) else f"column_{i}"
            # Clean header name for Webflow
            clean_header = str(header_name).strip().replace(' ', '_').replace('-', '_').lower()
            
            if cell and 'v' in cell:
                item[clean_header] = cell['v']
            else:
                item[clean_header] = ""
        
        processed_data.append(item)
    
    return processed_data

@app.route('/')
def home():
    return jsonify({
        "message": "Google Sheets API for Webflow",
        "status": "active", 
        "authentication": "none_required",
        "endpoints": {
            "all_data": "/api/data",
            "single_item": "/api/data/<row_id>",
            "filter_data": "/api/filter?key=value",
            "sheet_names": "/api/sheets"
        }
    })

# 👇 COPY THIS URL FOR WEBFLOW - GET ALL DATA
@app.route('/api/data', methods=['GET'])
def get_all_data():
    try:
        sheet_name = request.args.get('sheet', 'Sheet1')
        data = get_sheet_data(sheet_name)
        processed_data = process_sheet_data(data)
        
        return jsonify({
            "status": "success",
            "data": processed_data,
            "total": len(processed_data),
            "sheet": sheet_name,
            "source": "google_sheets_visualization_api"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

# 👇 COPY THIS URL FOR WEBFLOW - GET SINGLE ITEM BY ROW NUMBER
@app.route('/api/data/<int:row_id>', methods=['GET'])
def get_single_data(row_id):
    try:
        sheet_name = request.args.get('sheet', 'Sheet1')
        data = get_sheet_data(sheet_name)
        all_data = process_sheet_data(data)
        
        # Find the specific row (row_id is 1-based index in the data array)
        if 1 <= row_id <= len(all_data):
            item = all_data[row_id - 1]
            return jsonify({
                "status": "success",
                "data": item
            })
        else:
            return jsonify({
                "status": "error", 
                "message": f"Row {row_id} not found. Available rows: 1 to {len(all_data)}"
            }), 404
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

# 👇 COPY THIS URL FOR WEBFLOW - FILTER DATA
@app.route('/api/filter', methods=['GET'])
def filter_data():
    try:
        sheet_name = request.args.get('sheet', 'Sheet1')
        filters = request.args.to_dict()
        
        # Remove 'sheet' from filters if present
        if 'sheet' in filters:
            del filters['sheet']
        
        data = get_sheet_data(sheet_name)
        all_data = process_sheet_data(data)
        
        # Apply filters
        filtered_data = all_data
        if filters:
            filtered_data = []
            for item in all_data:
                match = True
                for key, value in filters.items():
                    if key in item:
                        if str(value).lower() not in str(item[key]).lower():
                            match = False
                            break
                    else:
                        match = False
                        break
                if match:
                    filtered_data.append(item)
        
        return jsonify({
            "status": "success",
            "data": filtered_data,
            "total": len(filtered_data),
            "filters_applied": filters,
            "sheet": sheet_name
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

# 👇 NEW: GET AVAILABLE SHEETS
@app.route('/api/sheets', methods=['GET'])
def get_sheet_names():
    try:
        # This endpoint returns basic info about available sheets
        return jsonify({
            "status": "success",
            "message": "Sheets are automatically detected. Use ?sheet=SheetName parameter",
            "default_sheet": "Sheet1",
            "usage": "Add ?sheet=YourSheetName to any endpoint"
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

# Health check for Render
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "google-sheets-api",
        "authentication": "none"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)