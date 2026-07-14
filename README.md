# HumanSafe - DevSecOps Pipeline

A complete DevSecOps pipeline project featuring an attractive safety website for human protection services including Medical, SOS, and Emergency features.

## Project Structure

```
devsecops-pipeline/
├── app/
│   ├── app.py              # Flask application with HumanSafe website
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Docker containerization
├── terraform/
│   ├── main.tf             # AWS infrastructure configuration
│   └── variables.tf        # Terraform variables
├── Jenkinsfile             # CI/CD pipeline definition
├── sonar-project.properties # SonarQube configuration
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## Features

- **One-Touch SOS** - Instant emergency alerts
- **Live Location Tracking** - Real-time GPS sharing
- **Medical Emergency Support** - Connect with healthcare professionals
- **Safety Zones** - Geofenced protection areas
- **Emergency Contacts** - Quick access to trusted contacts
- **Video Verification** - Live video feeds for emergencies

## Tech Stack

- **Backend**: Python, Flask, Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript (animated, responsive)
- **Containerization**: Docker
- **Infrastructure**: Terraform (AWS)
- **CI/CD**: Jenkins
- **Code Quality**: SonarQube

## Quick Start

### Local Development

```bash
cd app
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

### Docker Build & Run

```bash
cd app
docker build -t humansafe .
docker run -d -p 5000:5000 humansafe
```

### Terraform Deployment

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## CI/CD Pipeline

The Jenkinsfile defines the following stages:

1. **Checkout** - Source code retrieval
2. **SonarQube Analysis** - Code quality gate
3. **Unit Tests** - Automated testing
4. **Docker Build** - Container image creation
5. **Security Scan** - Vulnerability assessment
6. **Push to Registry** - Image repository upload
7. **Deploy to Staging** - Staging environment deployment
8. **Deploy to Production** - Production deployment (manual approval)

## Color Scheme

- **Red**: #E63946 - Emergency actions, alerts, calls-to-action
- **Blue**: #1D3557 - Trust, security, backgrounds
- **White**: #F1FAEE - Clean backgrounds, readability

## License

MIT License
