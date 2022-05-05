"""
Extracting housing datasets from zillow
Zillow Home Value Index (ZHVI): A smoothed, seasonally adjusted measure of the typical
home value and market changes across a given region and housing type. It reflects the
typical value for homes in the 35th to 65th percentile range. The raw version of that 
mid-tier ZHVI time series is also available.

data
"""
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

log = logging.getLogger(__name__)

HV_DOWNLOAD_BTN_ID = "median-home-value-zillow-home-value-index-zhvi-download-link"
HV_GEOGRAPHY_DROPDOWN_ID = "median-home-value-zillow-home-value-index-zhvi-dropdown-2"
ZHVI_VALUES_ID = "median-home-value-zillow-home-value-index-zhvi-dropdown-1"
ZHVI_FORECAST_ID = "home-values-forecasts-dropdown-1"
FORECAST_GEOGRAPHY_ID = "home-values-forecasts-dropdown-2"
FORECAST_DOWNLOAD_BTN_ID = "home-values-forecasts-download-link"

def setup():
    """
    Method to set preferences of chrome driver
    """
    try:   
        download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..',
                        'resources'))
        driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..',
                        'resources','Drivers_And_Resources','chromedriver'))
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": download_dir}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(driver_path, options=chrome_options)
        return driver
    except FileNotFoundError as err:
        log.error(err)
        print(f"File/Folder not found {err}")

def data_extracts(chrome_drvr):
    """
    Method to extract the home values data from zillow
    This loops through the dropdown list and then clicks on the download button
    """
    try:
        home_values_dropdown = Select(
            chrome_drvr.find_element(By.ID, ZHVI_VALUES_ID))
        hv_all_options = home_values_dropdown.options
        home_values_geography = Select(
            chrome_drvr.find_element(By.ID, HV_GEOGRAPHY_DROPDOWN_ID))
        for index in range(0, len(hv_all_options)):
            home_values_dropdown.select_by_index(index)
            home_values_geography.select_by_visible_text("Metro & U.S.")
            chrome_drvr.find_element(By.ID, HV_DOWNLOAD_BTN_ID).click()

        forecasts_dropdown = Select(chrome_drvr.find_element(By.ID, ZHVI_FORECAST_ID))
        forecasts_all_options = forecasts_dropdown.options
        forecasts_geography = Select(chrome_drvr.find_element(By.ID, FORECAST_GEOGRAPHY_ID))
        for index in range(0, len(forecasts_all_options)):
            forecasts_dropdown.select_by_index(index)
            forecasts_geography.select_by_visible_text("Metro & U.S.")
            chrome_drvr.find_element(By.ID, FORECAST_DOWNLOAD_BTN_ID).click()
    except NoSuchElementException as exc:
        log.error(exc)
        print(f"Check drop down list values: {exc}")
        chrome_drvr.close()   

def run_extract():
    Chromedriver = setup()
    Chromedriver.get("https://www.zillow.com/research/data/")
    data_extracts(Chromedriver)
