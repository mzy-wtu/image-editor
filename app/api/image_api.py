from flask import Blueprint, request, jsonify
from flask_login import login_required
import base64
from app.utils.mock_api import APIFactory

image_bp = Blueprint('image_api', __name__)

@image_bp.route('/api/generate', methods=['POST'])
@login_required
def generate_image():
    data = request.get_json()
    if not data or 'prompt' not in data or 'api_choice' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    prompt = data['prompt']
    api_choice = data['api_choice']
    
    # 获取API实例
    api = APIFactory.get_api(api_choice)
    
    # 生成图像
    result = api.generate_image(prompt, api_choice)
    if isinstance(result, tuple) and len(result) == 2:
        image_data, logs = result
    else:
        image_data, logs = result, []
    
    return jsonify({'image': image_data, 'logs': logs}), 200

@image_bp.route('/api/edit', methods=['POST'])
@login_required
def edit_image():
    data = request.get_json()
    if not data or 'image' not in data or 'api_choice' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    image_data = data['image'].split(',')[1]  # 移除base64前缀
    prompt = data.get('prompt', '')
    api_choice = data['api_choice']
    
    # 获取API实例
    api = APIFactory.get_api(api_choice)
    
    # 编辑图像
    result = api.edit_image(image_data, prompt, api_choice)
    if isinstance(result, tuple) and len(result) == 2:
        edited_image, logs = result
    else:
        edited_image, logs = result, []
    
    return jsonify({'image': edited_image, 'logs': logs}), 200