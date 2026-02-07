from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import base64

app = Flask(__name__)

# Configure Gemini API (replace with your API key)
genai.configure(api_key="AIzaSyC81VjLXLX4kNAit_0IhrgfF2nas7Iz8Lk")  # Replace with your actual API key

# Use the Gemini model
model_name = "gemini-1.5-pro-latest"
model = genai.GenerativeModel(model_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' in request.files:
        image_file = request.files['image']
        image_bytes = image_file.read()
        # Encode image bytes to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        prompt = "Does this image contain any inappropriate, NSFW, bad content, or signs of cyberbullying? Reply with 'not safe' if any such content is present, otherwise reply with 'safe'."
        # Prepare image data in the format expected by Gemini
        image_data = {
            "mime_type": image_file.content_type,
            "data": image_base64
        }
        response = model.generate_content([prompt, image_data])
        print("Raw response:", response)
        if hasattr(response, 'text'):
            result = response.text
        else:
            result = str(response)
        return jsonify({'analysis': result})
    else:
        data = request.get_json()
        text = data.get('text', '') if data else ''
        if not text:
            return jsonify({'error': 'No text or image provided'}), 400
        prompt = f"Analyze the following text and return 'offensive' if there is any offensive, hatespeech, cyberbulling present else return 'good' you are allowed to return only offensive or good and nothhing else,:\n\n{text}"
        response = model.generate_content(prompt)
        result = response.text if hasattr(response, 'text') else str(response)
        return jsonify({'analysis': result})

if __name__ == '__main__':
    app.run(debug=True)