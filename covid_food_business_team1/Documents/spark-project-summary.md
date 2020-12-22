## Goal:
1. Create a Database (permanent closed/temporarily closed/still open; # of orders(pick up, dine in, delivery); turnover; ratings & reviews; operation hours; whether take subsidy)
2. Understand how Covid impacted restaurants
3. Show how government policies / assistance impact restaurants

## Steps:
- Get the restaurants from multiple sources (Google Places, Bing, Yelp, Uber eats and so on)
- Get the Open/Closed Status & Operation ，hours from the restaurant API
- Get additional information (licensure, health & safety data, activity levels) to dataset
- Analyze the ones that participated government assistance programs (to see the impact of government help)
- Conduct visualization results for client (not specified yet)

## Questions to be answered:
- How many businesses have permanently closed during Covid? How many are open? How many are temporarily closed? (based on yelp and google places data)
- What hours are they operating under? 
- How much activity is happening at different types of businesses by restaurant type (e.g. Italian vs. Thai vs. pizza, etc.), by neighborhood or zip code? (use safe graph data)? Do hours of operation seem to impact overall activity/ success?
- What has been the relative impact on government policies (e.g. sidewalk dining) or assistance programs?

## Techs and Resources:
### API for restaurants:
- Google Places -rating,reviews, business status(open/close), address, opening hours(day & week)
- Bing
- Yelp API - ratings and reviews
- City of Boston Certified Businesses
- Grubhub - only for signed-in restaurants, cannot get an account. 
- Uber Eats - “Your application currently does not have access to any scopes. Please contact your Uber Business Development representative or Uber point of contact to request access.” + Please do not share this document or API endpoint details with anyone who is not authorized to have access. 
- Food Establishment Inspections - Datasets - Analyze Boston 
- Active Food Establishment Licenses - Datasets - Analyze Boston
- Section 12 Licenses (Alcohol) - Datasets - Analyze Boston
- Licensing Board Licenses - Datasets

- https://datausa.io/profile/geo/boston-ma/#economy 
- https://pos.toasttab.com/
- https://www.clover.com/
- https://squareup.com/us/en
- https://www.themassrest.org/
- http://www.bostonrestaurantgroup.com/
- interesting to review restaurant sales data


## API for activity levels: Safegraph data
- Resources for government assistance: 
- PPE Loan Data (Mass) 
- Small business grant fund from City of Boston
- Reopen Boston fund from City of Boston
- Outdoor seating pilot participants
- Take out alcohol pilot participants
