# Face Recognition System

## Overview

This is a comprehensive face recognition system built with Django and various AI technologies. The system provides
robust face detection, feature extraction, and face matching capabilities through both RESTful APIs and a web interface.

## Features

- **Face Library Management**: Register, update, query, and delete face information
- **Face Detection**: Detect faces in images and extract the largest face by default
- **Feature Extraction**: Extract 512-dimensional face feature vectors
- **1:1 Face Verification**: Compare two faces for similarity
- **1:N Face Identification**: Match a face against the entire database
- **Similar Face Search**: Find similar faces in the database (top-5 results)
- **Web Management Interface**: Visual interface for face library management

## System Requirements

- Python 3.7+
- GPU support (for optimal performance)
- CUDA compatible environment (for GPU acceleration)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/senthree3/faceRecognition.git
cd faceRecognition
```

### 2. Set up a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install PyTorch (uncomment the PyTorch packages in requirements.txt or install manually)

```bash
# For CUDA 11.x
pip install torch==2.0.0+cu117 torchvision==0.15.0+cu117 torchaudio==2.0.0 --index-url https://download.pytorch.org/whl/cu117
```

### 5.Model Installation

```bash
# Download the AI models package
# Download the required AI models file (aiModels.zip) from:
wegt https://drive.google.com/file/d/1w2eQzqurwTwB-5yoonRFGXb4YbHZCscc/view?usp=sharing

# Extract the model files
# Extract the downloaded aiModels.zip file to the faceRecognition directory
unzip aiModels.zip -d /path/to/project/faceRecognition/
```

### 6. Set up Django

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

## Configuration

Configure the Django settings in `faceRecognition/settings.py` to match your environment. You may need to adjust
database settings, static files, and security settings.

## Web Management Interface

The system includes a web interface for face library management. Access it through:

```
http://{IP}:{PORT}/admin/
```

## API Documentation

The system provides RESTful APIs for face recognition operations. All API endpoints use standardized request and
response formats with encryption and authentication mechanisms.

### Base URL

```
http://{IP}:{PORT}/ai/openAbility/v1/
```

### Authentication

All API requests require authentication via:

- `access_key`: Access key identifier
- `secret_key`: Secret key for encryption and signing
- `time_stamp`: Unix timestamp (milliseconds)
- `request_id`: UUID4 string
- `sign`: MD5 signature
- `data`: AES-encrypted request data

* **`access_key` and `secret_key` obtain from Web Management**

### API Endpoints

#### Face Library Management

1. **Register Face**: `/faceReg`
2. **Delete Face**: `/faceRegDelete`
3. **Update Face**: `/faceReg` (with existing face_id)
4. **Query Face by ID**: `/faceRegIDQuery`
5. **Query Faces with Pagination**: `/faceRegQuery`

#### Face Recognition

1. **Face Detection**: `/faceDet`
2. **Feature Extraction**: `/faceFeatureExtraction`
3. **1:1 Face Verification**: `/faceVerify`
4. **1:1 Face Verification Against DB**: `/faceVerifyDB`
5. **1:N Face Identification**: `/face1N`
6. **Similar Face Search**: `/faceSimilarRetrieval`

## Example Usage

For detailed API usage examples, parameter specifications, and response formats, please refer to
the [API Documentation](./api-doc-zh.md) included in the project.

## Security Considerations

- Keep your `access_key` and `secret_key` confidential
- Use HTTPS in production
- Implement proper authentication and authorization
- Consider data privacy regulations when storing face data

## Contact Information
For technical support or inquiries:
- Email-1: senthree30@gmail.com 
- Email-2: 717192305@qq.com
- GitHub Issues: https://github.com/senthree3/faceRecognition/issues

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgements

- This project uses various libraries including Django, OpenCV, FAISS, ONNX Runtime, and PyTorch
- Thanks to all contributors and the open-source community