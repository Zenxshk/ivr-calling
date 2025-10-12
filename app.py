from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# 📌 YOUR GOOGLE SHEET ID - I can see it from your URL
GOOGLE_SHEET_ID = "12oP1qNlGEgkEx7xypUojoyHO5yuIKAx6SnhKcVN3Uew"

def get_sheet_data(sheet_name='demo testing'):
    """Fetch data from YOUR Google Sheet"""
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:json&sheet={sheet_name}"
    
    try:
        print(f"🔗 Fetching from: {url}")
        response = requests.get(url, timeout=10)
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        # Clean the response text
        text = response.text
        
        # Remove Google's wrapper
        if text.startswith('/*O_o*/'):
            text = text.split('/*O_o*/')[1]
        
        if 'google.visualization.Query.setResponse(' in text:
            text = text.split('google.visualization.Query.setResponse(')[1]
            text = text.rsplit(');', 1)[0]
        
        print(f"📝 Cleaned response (first 500 chars): {text[:500]}...")
        
        # Parse JSON
        data = json.loads(text)
        return data
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise Exception(f"Failed to fetch sheet: {str(e)}")

def process_sheet_data(data):
    """Convert your sheet data to JSON"""
    print("🔄 Processing sheet data...")
    
    if not data or 'table' not in data:
        print("❌ No table found in data")
        return []
    
    rows = data['table']['rows']
    print(f"📊 Found {len(rows)} rows")
    
    if not rows:
        return []
    
    # Extract headers from first row
    headers = []
    first_row = rows[0]['c'] if rows[0] else []
    
    for i, cell in enumerate(first_row):
        if cell and 'v' in cell:
            header_name = str(cell['v']).strip()
        else:
            header_name = f"column_{i+1}"
        
        # Clean header name for JSON
        clean_header = header_name.replace(' ', '_').replace('-', '_').lower()
        headers.append(clean_header)
    
    print(f"🏷️ Headers: {headers}")
    
    # Process data rows (skip header row)
    processed_data = []
    for row_index, row in enumerate(rows[1:], start=1):
        if not row or not row.get('c'):
            continue
            
        row_cells = row['c']
        item = {"id": row_index}
        
        for i, header in enumerate(headers):
            if i < len(row_cells) and row_cells[i] and 'v' in row_cells[i]:
                item[header] = row_cells[i]['v']
            else:
                item[header] = ""  # Empty cell
        
        processed_data.append(item)
        print(f"📄 Row {row_index}: {item}")
    
    print(f"✅ Processed {len(processed_data)} data rows")
    return processed_data

@app.route('/')
def home():
    return jsonify({
        "message": "Google Sheets API - YOUR DATA",
        "status": "active",
        "your_sheet_id": GOOGLE_SHEET_ID,
        "endpoints": {
            "all_data": "/api/data",
            "test_connection": "/api/test",
            "debug_info": "/api/debug"
        }
    })

# 👇 TEST YOUR SHEET CONNECTION
@app.route('/api/test', methods=['GET'])
def test_sheet():
    try:
        print("🧪 Testing sheet connection...")
        data = get_sheet_data()
        
        return jsonify({
            "status": "success",
            "message": "✅ Your Google Sheet is accessible!",
            "sheet_id": GOOGLE_SHEET_ID,
            "data_structure": list(data.keys()) if data else "No data"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"❌ Connection failed: {str(e)}",
            "help": "Make sure your Google Sheet is shared publicly"
        }), 500

# 👇 DEBUG - SEE RAW DATA
@app.route('/api/debug', methods=['GET'])
def debug_sheet():
    try:
        data = get_sheet_data()
        
        # Show simplified debug info
        debug_info = {
            "table_keys": list(data.get('table', {}).keys()) if data else [],
            "row_count": len(data.get('table', {}).get('rows', [])) if data else 0,
            "first_few_rows": []
        }
        
        # Show first 2 rows as sample
        rows = data.get('table', {}).get('rows', [])
        for i, row in enumerate(rows[:2]):
            if row and row.get('c'):
                debug_info["first_few_rows"].append({
                    "row_index": i,
                    "cells": [cell.get('v', '') if cell else '' for cell in row['c']]
                })
        
        return jsonify({
            "status": "success",
            "debug_info": debug_info,
            "raw_data_keys": list(data.keys()) if data else []
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

# 👇 GET YOUR ACTUAL DATA
@app.route('/api/data', methods=['GET'])
def get_all_data():
    try:
        print("📥 Fetching your data...")
        raw_data = get_sheet_data()
        processed_data = process_sheet_data(raw_data)
        
        # Get column names for reference
        columns = []
        if processed_data:
            columns = list(processed_data[0].keys())
        
        return jsonify({
            "status": "success",
            "data": processed_data,
            "total_records": len(processed_data),
            "columns_available": columns,
            "your_sheet": GOOGLE_SHEET_ID
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e),
            "help": "Check if your sheet has data in Sheet1 with headers in first row"
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Flask Server for YOUR Google Sheet")
    print(f"📊 Your Sheet ID: {GOOGLE_SHEET_ID}")
    print("🌐 Testing URLs:")
    print(f"   • Test Connection: http://localhost:5000/api/test")
    print(f"   • Debug Info: http://localhost:5000/api/debug") 
    print(f"   • Your Data: http://localhost:5000/api/data")
    app.run(debug=True, host='0.0.0.0', port=5000)