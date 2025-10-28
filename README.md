# community-resource-api
# Community Resource Sharing API

A simple Flask API to help people share resources during tough economic times.

## What it does
- People can create accounts and log in
- Users can post resources like food banks, job opportunities, housing help
- Others can search for resources by category and location
- Each user can manage their own posts

## How to run
1. Install: `pip install -r requirements.txt`
2. Run: `python app.py`
3. API will be at `http://localhost:5000`

## Main API endpoints
- `POST /register` - Create account
- `POST /login` - Get login token  
- `GET /resources` - Get all resources (add ?category=food or ?city=London to filter)
- `POST /resources` - Create new resource (need auth token)
- `DELETE /resources/<id>` - Delete your resource (need auth token)
- `GET /my-resources` - Get your resources (need auth token)

## Example usage
```bash
# Register
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"name":"John","email":"john@test.com","password":"123456","city":"London"}'

# Login  
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"email":"john@test.com","password":"123456"}'

# Create resource (use token from login)
curl -X POST http://localhost:5000/resources -H "Content-Type: application/json" -H "Authorization: YOUR_TOKEN" -d '{"title":"Free meals","description":"Daily free meals at community center","category":"food","city":"London"}'