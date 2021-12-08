
# Covid 19 Dashboard
---
Welcome to the Covid 19 Dashboard!

## Requirements

You will need to have the following modules installed.
  - Flask
  - uk-covid19
  - sched
  - requests

Use

    pip install [module name]

in your terminal to do this (or pip3)

# Set the API key

You need to register for an API key by going to News API
https://newsapi.org

Once you have a key, open the config.json file.
There is a string that says:

    "NEWS_API_KEY": "key"

replace the word key with your API key, keeping the speech marks.

Save the file.

## Running the Dashboard

Using the terminal, run the program using

    python3 main.py

You will need to be in the covid_dashboard directory. You can move through your
file system to find this using the commands

    ls

To show the contents of your current directory and

    cd [directory name]

To move into that directory

You should then see that the Flask app main is being served.
Open your browser and navigate to http://127.0.0.1:5000/index

The Dashboard should then be up and running!

You can add alarms to schedule updates to the data and news using the form.

You can also remove news and alarms by clicking the x in the widget's corner.

## Custom news searching

Open the config.json file.

In this file there is a string with news search terms set to

    "Covid COVID-19 coronavirus"

You can modify this (leaving the speech marks) to customise your news.

Save the file.


## Setting your location

### National

Open the config.json file.
In this file there is a string specifying the national location:

        "NATION":"England"

Modify the word England to your national location ie England, Scotland, Wales,

Save the file.

<details>
<summary>Show all locations</summary>
'England', 'Northern Ireland', 'Scotland', 'Wales'
</details>

### Local
Open the config.json file.
In this file there is a string specifying the local location:

      "LOCAL": "Exeter"

Modify the word Exeter to your local location ie Exeter, Swindon etc

Save the file.


<details>
<summary>Show all locations</summary>

'South Gloucestershire', 'Luton', 'Southend-on-Sea', 'Shropshire', 'Aylesbury Vale', 'South Derbyshire', 'Cheltenham', 'Gloucester', 'Sevenoaks', 'Swale', 'Fylde', 'South Ribble', 'Harborough', 'Hinckley and Bosworth', 'Craven', 'Newark and Sherwood', 'Staffordshire Moorlands', 'Surrey Heath', 'Rugby', 'Manchester', 'Rochdale', 'Tameside', 'Sunderland', 'Dudley', 'Hackney and City of London', 'Antrim and Newtownabbey', 'Gwynedd', 'Ceredigion', 'North East Lincolnshire', 'Derby', 'Peterborough', 'Medway', 'Southampton', 'Dorset', 'Cambridge', 'East Cambridgeshire', 'Eden', 'Braintree', 'Tendring', 'Broxbourne', 'Blaby', 'Boston', 'North Kesteven', 'Breckland', 'North Norfolk', 'Scarborough', 'Mansfield', 'West Oxfordshire', 'Mole Valley', 'Redditch', 'Barking and Dagenham', 'Camden', 'Redbridge', 'Armagh City, Banbridge and Craigavon', 'North Ayrshire', 'Argyll and Bute', 'Stoke-on-Trent', 'Cheshire West and Chester', 'Northumberland', 'South Cambridgeshire', 'Allerdale', 'Harlow', 'Thanet', 'South Holland', 'Broadland', 'Cherwell', 'Waverley', 'Woking', 'Worcester', 'Wychavon', 'West Suffolk', 'North Tyneside', 'Gateshead', 'Kingston upon Thames', 'Richmond upon Thames', 'Wandsworth', 'Derry City and Strabane', 'Fife', 'Glasgow City', 'Conwy', 'Denbighshire', 'Carmarthenshire', 'Blaenau Gwent', 'Blackpool', 'Plymouth', 'Bournemouth, Christchurch and Poole', 'East Devon', 'Colchester', 'Rushmoor', 'Test Valley', 'Tonbridge and Malling', 'Tunbridge Wells', 'Chorley', 'Pendle', 'Rossendale', 'Great Yarmouth', 'South Norfolk', 'Kettering', 'Ashfield', 'South Oxfordshire', 'Mid Suffolk', 'Elmbridge', 'Epsom and Ewell', 'Tandridge', 'East Hertfordshire', 'Newcastle upon Tyne', 'Wolverhampton', 'Bradford', 'Bromley', 'Lambeth', 'Vale of Glamorgan', 'North Somerset', 'Slough', 'Central Bedfordshire', 'Chesterfield', 'Derbyshire Dales', 'Teignbridge', 'Brentwood', 'Fareham', 'Burnley', 'Lancaster', "King's Lynn and West Norfolk", 'Richmondshire', 'Rushcliffe', 'Bromsgrove', 'Wyre Forest', 'Barnsley', 'Birmingham', 'Croydon', 'Haringey', 'Islington', 'Lisburn and Castlereagh', 'East Ayrshire', 'Highland', 'West Lothian', 'Wrexham', 'Monmouthshire', 'Newport', 'Kingston upon Hull, City of', 'West Berkshire', 'Wiltshire', 'South Lakeland', 'Mid Devon', 'West Devon', 'Hastings', 'Forest of Dean', 'Eastleigh', 'Ribble Valley', 'Oadby and Wigston', 'Lichfield', 'Tamworth', 'Babergh', 'Ipswich', 'Guildford', 'Reigate and Banstead', 'Nuneaton and Bedworth', 'Stratford-on-Avon', 'Welwyn Hatfield', 'Bury', 'Solihull', 'Kirklees', 'Havering', 'Sutton', 'Clackmannanshire', 'Stirling', 'Rhondda Cynon Taf', 'North Lincolnshire', 'Bath and North East Somerset', 'Bristol, City of', 'Swindon', 'Fenland', 'North Devon', 'Torridge', 'Hertsmere', 'North Hertfordshire', 'Three Rivers', 'Ashford', 'Hyndburn', 'Daventry', 'East Northamptonshire', 'East Staffordshire', 'Spelthorne', 'Adur', 'Mid Sussex', 'Somerset West and Taunton', 'Wigan', 'Sefton', 'Enfield', 'Harrow', 'Mid Ulster', 'Comhairle nan Eilean Siar', 'North Lanarkshire', 'Cardiff', 'York', 'Rutland', 'Isle of Wight', 'County Durham', 'South Hams', 'Lewes', 'Stroud', 'East Hampshire', 'Norwich', 'Wellingborough', 'Oxford', 'Mendip', 'Warwick', 'Walsall', 'Wakefield', 'Hammersmith and Fulham', 'Hillingdon', 'Hounslow', 'East Lothian', 'East Renfrewshire', 'Orkney Islands', 'South Lanarkshire', 'Renfrewshire', 'East Dunbartonshire', 'Isle of Anglesey', 'Swansea', 'Neath Port Talbot', 'Bridgend', 'Torbay', 'Bedford', 'South Bucks', 'Epping Forest', 'Winchester', 'Maidstone', 'Folkestone and Hythe', 'Wyre', 'Lincoln', 'Northampton', 'Harrogate', 'Vale of White Horse', 'South Somerset', 'Newcastle-under-Lyme', 'Chichester', 'Knowsley', 'Lewisham', 'Westminster', 'Causeway Coast and Glens', 'Falkirk', 'Moray', 'Shetland Islands', 'Aberdeen City', 'West Dunbartonshire', 'Angus', 'Torfaen', 'Powys', 'Hartlepool', 'Redcar and Cleveland', 'Halton', 'East Riding of Yorkshire', 'Nottingham', 'Brighton and Hove', 'Wycombe', 'Carlisle', 'Erewash', 'North East Derbyshire', 'Maldon', 'Uttlesford', 'Havant', 'Dartford', 'Dover', 'South Kesteven', 'West Lindsey', 'Broxtowe', 'Cannock Chase', 'St Albans', 'Wirral', 'South Tyneside', 'Calderdale', 'Bexley', 'Waltham Forest', 'Midlothian', 'City of Edinburgh', 'Pembrokeshire', 'Amber Valley', 'High Peak', 'Eastbourne', 'Tewkesbury', 'Watford', 'North West Leicestershire', 'Corby', 'South Northamptonshire', 'Ryedale', 'Gedling', 'Sedgemoor', 'South Staffordshire', 'Stafford', 'North Warwickshire', 'Crawley', 'Salford', 'Trafford', 'St. Helens', 'Rotherham', 'Sandwell', 'Greenwich', 'Kensington and Chelsea', 'Southwark', 'Tower Hamlets', 'Ards and North Down', 'Dumfries and Galloway', 'South Ayrshire', 'Middlesbrough', 'Stockton-on-Tees', 'Blackburn with Darwen', 'Leicester', 'Thurrock', 'Reading', 'Windsor and Maidenhead', 'Wokingham', 'Milton Keynes', 'Cheshire East', 'Exeter', 'Castle Point', 'Cotswold', 'New Forest', 'West Lancashire', 'Horsham', 'Worthing', 'Stevenage', 'Bolton', 'Sheffield', 'Coventry', 'Ealing', 'Merton', 'Newry, Mourne and Down', 'Aberdeenshire', 'Dundee City', 'Perth and Kinross', 'Herefordshire, County of', 'Telford and Wrekin', 'Bracknell Forest', 'Barrow-in-Furness', 'Copeland', 'Bolsover', 'Rother', 'Basildon', 'Rochford', 'Dacorum', 'Canterbury', 'Preston', 'Charnwood', 'East Lindsey', 'Bassetlaw', 'Arun', 'Malvern Hills', 'East Suffolk', 'Oldham', 'Stockport', 'Liverpool', 'Barnet', 'Brent', 'Newham', 'Fermanagh and Omagh', 'Inverclyde', 'Scottish Borders', 'Flintshire', 'Darlington', 'Warrington', 'Portsmouth', 'Cornwall and Isles of Scilly', 'Chiltern', 'Huntingdonshire', 'Wealden', 'Chelmsford', 'Basingstoke and Deane', 'Gosport', 'Hart', 'Gravesham', 'Melton', 'Hambleton', 'Selby', 'Runnymede', 'Doncaster', 'Leeds', 'Belfast', 'Mid and East Antrim', 'Caerphilly', 'Merthyr Tydfil'

</details>

## Code Documentation
The codes documentation wesbite can be found under CovidDashboard/docs/_build/html
