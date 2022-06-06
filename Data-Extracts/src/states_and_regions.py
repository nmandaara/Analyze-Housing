import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_lookup():
    file_name = os.path.abspath(os.path.join(os.path.dirname(__file__),'..',
                            'resources','state_and_regions.csv'))

    url = "https://www.mappr.co/political-maps/us-regions-map/"
    data = requests.get(url, verify=False).text

    soup = bs(data, "html.parser")
    table = soup.find("table")

    df = pd.DataFrame(columns = ["StateCode", "State", "Region"])

    for row in table.tbody.find_all("tr"):
        columns = row.find_all("td")

        if(columns != []):
            state_code = columns[0].text.strip()
            state_name = columns[1].text.strip()
            region = columns[2].text.strip()
            df = df.append({"StateCode" : state_code, "State":state_name, "Region":region}, ignore_index=True)
    df.to_csv(file_name, index=False)