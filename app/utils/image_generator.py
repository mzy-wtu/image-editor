import base64
from PIL import Image, ImageDraw, ImageFont
import io

class MockAPI:
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        pass
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        pass

class API1(MockAPI):
    def __init__(self):
        try:
            import dashscope
            from dashscope import MultiModalConversation
            import requests
            import os
            import json
            
            self.dashscope = dashscope
            self.MultiModalConversation = MultiModalConversation
            self.requests = requests
            self.json = json
            
            # 配置API Key
            self.api_key = os.getenv("DASHSCOPE_API_KEY", "sk-e6387b41fb884c93ba2f7b7d93f4d9d4")
            
            # 配置API URL - 中国（北京）地域
            self.dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            
            self.available = True
        except ImportError:
            print("DashScope SDK not installed, using mock API instead")
            self.available = False
    
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        if not self.available:
            # 回退到模拟实现
            logs.append("DashScope SDK not available, using mock API")
            mock_result, mock_logs = self._mock_generate(prompt)
            logs.extend(mock_logs)
            return mock_result, logs
        
        try:
            # 构建请求消息
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ]
            
            # 调用千问万象API进行文生图
            api_params = {
                "api_key": self.api_key,
                "model": "qwen-image-2.0-pro",
                "messages": messages,
                "stream": False,
                "n": 1,
                "watermark": False,
                "negative_prompt": negative_prompt if negative_prompt else " ",
                "prompt_extend": True,
                "size": size,
            }
            
            # 添加随机种子（如果提供）
            if seed is not None:
                api_params["seed"] = int(seed)
            
            response = self.MultiModalConversation.call(**api_params)
            
            if response.status_code == 200:
                # 查看完整响应
                logs.append("Response JSON:")
                logs.append(self.json.dumps(response, ensure_ascii=False, indent=2))
                
                # 提取图像URL
                image_url = None
                try:
                    for i, content in enumerate(response.output.choices[0].message.content):
                        if 'image' in content:
                            image_url = content['image']
                            log_msg = f"输出图像{i+1}的URL:{image_url}"
                            logs.append(log_msg)
                            break
                except Exception as json_error:
                    log_msg = f"Error extracting image URL from JSON: {str(json_error)}"
                    logs.append(log_msg)
                
                if image_url:
                    # 下载图像到本地
                    try:
                        import os
                        # 创建images目录
                        if not os.path.exists('images'):
                            os.makedirs('images')
                        
                        # 生成文件名
                        import uuid
                        file_name = f"images/{str(uuid.uuid4())}.png"
                        
                        # 下载图像
                        log_msg = f"Downloading image to: {file_name}"
                        logs.append(log_msg)
                        img_response = self.requests.get(image_url, timeout=30)
                        img_response.raise_for_status()
                        
                        # 保存到本地
                        with open(file_name, 'wb') as f:
                            f.write(img_response.content)
                        log_msg = f"Image saved to: {file_name}"
                        logs.append(log_msg)
                        
                        # 读取本地文件并转换为base64
                        with open(file_name, 'rb') as f:
                            img_content = f.read()
                        img_str = base64.b64encode(img_content).decode('utf-8')
                        return f"data:image/png;base64,{img_str}", logs
                    except Exception as download_error:
                        log_msg = f"Error downloading and saving image: {str(download_error)}"
                        logs.append(log_msg)
                        # 回退到模拟实现
                        mock_result, mock_logs = self._mock_generate(prompt)
                        logs.extend(mock_logs)
                        return mock_result, logs
                else:
                    logs.append("No image URL found in response")
                    mock_result, mock_logs = self._mock_generate(prompt)
                    logs.extend(mock_logs)
                    return mock_result, logs
            else:
                log_msg = f"HTTP返回码：{response.status_code}"
                logs.append(log_msg)
                log_msg = f"错误码：{response.code}"
                logs.append(log_msg)
                log_msg = f"错误信息：{response.message}"
                logs.append(log_msg)
                logs.append("请参考文档： https://help.aliyun.com/zh/model-studio/error-code ")
                # 回退到模拟实现
                mock_result, mock_logs = self._mock_generate(prompt)
                logs.extend(mock_logs)
                return mock_result, logs
        except Exception as e:
            log_msg = f"Error in API1.generate_image: {str(e)}"
            logs.append(log_msg)
            # 回退到模拟实现
            mock_result, mock_logs = self._mock_generate(prompt)
            logs.extend(mock_logs)
            return mock_result, logs
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        if not self.available:
            # 回退到模拟实现
            logs.append("DashScope SDK not available, using mock API")
            mock_result, mock_logs = self._mock_edit(image_data, prompt)
            logs.extend(mock_logs)
            return mock_result, logs
        
        try:
            # 构建请求消息
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"image": f"data:image/png;base64,{image_data}"},
                        {"text": prompt if prompt else "编辑图像"}
                    ]
                }
            ]
            
            # 调用千问万象API进行图像编辑
            api_params = {
                "api_key": self.api_key,
                "model": "qwen-image-2.0-pro",
                "messages": messages,
                "stream": False,
                "n": 1,
                "watermark": False,
                "negative_prompt": negative_prompt if negative_prompt else " ",
                "prompt_extend": True,
                "size": size,
            }
            
            if seed is not None:
                api_params["seed"] = int(seed)
            
            response = self.MultiModalConversation.call(**api_params)
            
            if response.status_code == 200:
                # 查看完整响应
                logs.append("Response JSON:")
                logs.append(self.json.dumps(response, ensure_ascii=False, indent=2))
                
                # 提取图像URL
                image_url = None
                try:
                    for i, content in enumerate(response.output.choices[0].message.content):
                        if 'image' in content:
                            image_url = content['image']
                            log_msg = f"输出图像{i+1}的URL:{image_url}"
                            logs.append(log_msg)
                            break
                except Exception as json_error:
                    log_msg = f"Error extracting image URL from JSON: {str(json_error)}"
                    logs.append(log_msg)
                
                if image_url:
                    # 下载图像到本地
                    try:
                        import os
                        # 创建images目录
                        if not os.path.exists('images'):
                            os.makedirs('images')
                        
                        # 生成文件名
                        import uuid
                        file_name = f"images/{str(uuid.uuid4())}.png"
                        
                        # 下载图像
                        log_msg = f"Downloading image to: {file_name}"
                        logs.append(log_msg)
                        img_response = self.requests.get(image_url, timeout=30)
                        img_response.raise_for_status()
                        
                        # 保存到本地
                        with open(file_name, 'wb') as f:
                            f.write(img_response.content)
                        log_msg = f"Image saved to: {file_name}"
                        logs.append(log_msg)
                        
                        # 读取本地文件并转换为base64
                        with open(file_name, 'rb') as f:
                            img_content = f.read()
                        img_str = base64.b64encode(img_content).decode('utf-8')
                        return f"data:image/png;base64,{img_str}", logs
                    except Exception as download_error:
                        log_msg = f"Error downloading and saving image: {str(download_error)}"
                        logs.append(log_msg)
                        # 回退到模拟实现
                        mock_result, mock_logs = self._mock_edit(image_data, prompt)
                        logs.extend(mock_logs)
                        return mock_result, logs
                else:
                    logs.append("No image URL found in response")
                    mock_result, mock_logs = self._mock_edit(image_data, prompt)
                    logs.extend(mock_logs)
                    return mock_result, logs
            else:
                log_msg = f"HTTP返回码：{response.status_code}"
                logs.append(log_msg)
                log_msg = f"错误码：{response.code}"
                logs.append(log_msg)
                log_msg = f"错误信息：{response.message}"
                logs.append(log_msg)
                logs.append("请参考文档： https://help.aliyun.com/zh/model-studio/error-code ")
                # 回退到模拟实现
                mock_result, mock_logs = self._mock_edit(image_data, prompt)
                logs.extend(mock_logs)
                return mock_result, logs
        except Exception as e:
            log_msg = f"Error in API1.edit_image: {str(e)}"
            logs.append(log_msg)
            # 回退到模拟实现
            mock_result, mock_logs = self._mock_edit(image_data, prompt)
            logs.extend(mock_logs)
            return mock_result, logs
    
    def _mock_generate(self, prompt):
        logs = []
        logs.append("Using Qianwen API for image generation")
        logs.append(f"Prompt: {prompt[:100]}")
        img = Image.new('RGB', (512, 512), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 20)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), f"Qianwen Generated Image\nPrompt: {prompt[:100]}", fill=(255, 255, 255), font=font)
        
        # 转换为base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs
    
    def _mock_edit(self, image_data, prompt):
        logs = []
        logs.append("Using Qianwen API for image editing")
        if prompt:
            logs.append(f"Prompt: {prompt[:100]}")
        # 模拟实现
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 30)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), "Qianwen Edited", fill=(255, 0, 0), font=font)
        if prompt:
            d.text((10, 50), f"Prompt: {prompt[:50]}", fill=(255, 0, 0), font=font)
        
        # 转换为base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs

class API2(MockAPI):
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Tongyi API for image generation")
        logs.append(f"Prompt: {prompt[:100]}")
        # 生成一个简单的图像，显示提示文本
        img = Image.new('RGB', (512, 512), color=(255, 223, 186))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 20)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), f"Tongyi Generated Image\nPrompt: {prompt[:100]}", fill=(0, 0, 0), font=font)
        
        # 转换为base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Tongyi API for image editing")
        if prompt:
            logs.append(f"Prompt: {prompt[:100]}")
        # 加载图像并转换为灰度
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        img = img.convert('L')
        
        # 转换为base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs

class API3(MockAPI):
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Mock API for image generation")
        logs.append(f"Prompt: {prompt[:100]}")
        # 生成一个简单的图像，显示提示文本
        img = Image.new('RGB', (512, 512), color=(144, 238, 144))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 20)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), f"Mock API Generated Image\nPrompt: {prompt[:100]}", fill=(0, 0, 0), font=font)
        
        # 转换为base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Mock API for image editing")
        if prompt:
            logs.append(f"Prompt: {prompt[:100]}")
        # 加载图像并添加边框
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        bordered_img = Image.new('RGB', (img.width + 20, img.height + 20), color=(255, 0, 0))
        bordered_img.paste(img, (10, 10))
        
        # 转换为base64
        buffer = io.BytesIO()
        bordered_img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs

# API工厂类
class APIFactory:
    @staticmethod
    def get_api(api_choice):
        if api_choice == 'API-1':
            return API1()
        elif api_choice == 'API-2':
            return API2()
        elif api_choice == 'API-3':
            return API3()
        else:
            return API1()  # 默认使用API-1