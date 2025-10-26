from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from csv_parser import process_csv
from gemini_seller import get_seller_info, configure_gemini

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure upload folder
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/parse-bom', methods=['POST'])
def parse_bom():
    """Parse uploaded BOM file and extract part names and quantities."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only CSV, TXT, XLSX, XLS files allowed"}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the CSV file
        parsed_data = process_csv(filepath)
        
        # Clean up temporary file
        os.remove(filepath)
        
        return jsonify({
            "success": True,
            "data": parsed_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-sellers', methods=['POST'])
def get_sellers():
    """Get seller information for parsed BOM items."""
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            return jsonify({"error": "No items provided"}), 400
        
        items = data['items']
        api_key = data.get('api_key')  # Optional: pass API key from frontend
        
        # Configure Gemini if API key provided
        if api_key:
            configure_gemini(api_key)
        
        # Get seller information
        seller_info = get_seller_info(items)
        
        return jsonify({
            "success": True,
            "data": seller_info
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-bom', methods=['POST'])
def process_bom_complete():
    """Complete pipeline: parse BOM and get seller info in one call."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Step 1: Parse the CSV file
        parsed_data = process_csv(filepath)
        
        # Clean up temporary file
        os.remove(filepath)
        
        # Step 2: Get seller information
        seller_info = get_seller_info(parsed_data)
        
        return jsonify({
            "success": True,
            "parsed_data": parsed_data,
            "seller_info": seller_info
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Try to configure Gemini on startup
    try:
        configure_gemini()
        print("✅ Gemini API configured successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not configure Gemini API: {e}")
        print("    API key can be provided via request")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
