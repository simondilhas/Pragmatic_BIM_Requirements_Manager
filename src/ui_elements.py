import streamlit as st
from streamlit.runtime.scriptrunner import RerunData, RerunException, get_script_run_ctx
from streamlit.source_util import get_pages
import logging
import time
import yaml
import json
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def switch_page(page_name: str):
    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    
    page_name = standardize_name(page_name)
    pages = get_pages("home.py")
    page_names = [standardize_name(config["page_name"]) for config in pages.values()]
    print("Available pages:", page_names)
    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )
    page_names = [standardize_name(config["page_name"]) for config in pages.values()]
    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

def logo():
  try:
    logo_path = "assets/Pragmatic Projects_Logo.png"
    link = "https://abstractroombook-dhuy3nusz6wbgleubfrmbl.streamlit.app"
    app_logo = st.logo(logo_path, link=link, icon_image="assets/Pragmatic_fav.png")

    logging.debug("Logo set")

  except Exception as e:
    logging.debug("Error with setting Logo: %s", e)
    
  return app_logo

def footer():
  try:
    footer = """
<style>
#footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: 10px;
  background-color: #E11A27;
  box-sizing: border-box;
}

#footer a {
  text-decoration: none;
  color: #262730;
  font-size: 12px;
}
</style>

<div id="footer">
  <div>
    <a href="https://www.abstract.build" target="_blank">Made by Abstract ------ </a>
    <a href="https://www.pragmaticprojects.ch/privacy" target="_blank">Privacy Policy & Terms of service</a>
  </div>
</div>
"""
    app_footer = st.markdown(footer, unsafe_allow_html=True)
    
    logging.debug("Footer set")
  
  except Exception as e:
    logging.debug("Error with setting Footer: %s", e)

    return app_footer

def padding():
  try:
    st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 15px;  /* Adjust this value to increase or decrease the distance */
        padding-right: 5px
        padding-left: 5px
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    logging.debug("Footer set")
  
  except Exception as e:
    logging.debug("Error with setting padding: %s", e)


def display_temp_data(space_data, full_geometry, reduced_geometry):

  try:
    with st.expander("Ifc Meta Data", expanded=True):
        st.table(space_data)
    with st.expander("Full Geometry", expanded=False):
        st.write(full_geometry)
    with st.expander("2d Floorplan Geometry", expanded=False):
        st.write(reduced_geometry)

    logging.debug("The saved Temp files displayed succesfully ")
  
  except Exception as e:
    logging.debug("Error with displaying Temp files: %s", e)

def list_of_ifc_entities():
  #used in extract ifc entities, so be careful when adding Project-Storey
  
  ifc_entities = [
            # General
    #"IfcProject",
    #"IfcSite",
    #"IfcBuilding",
    #"IfcBuildingStorey",
    "IfcSpace",

    # Architecture
    "IfcWall",
    "IfcSlab",
    "IfcRoof",
    "IfcColumn",
    "IfcBeam",
    "IfcStair",
    "IfcRamp",
    "IfcDoor",
    "IfcWindow",
    "IfcCurtainWall",
    "IfcRailing",
    "IfcCovering",

    # HVAC
    "IfcAirTerminal",
    "IfcAirTerminalBox",
    "IfcDamper",
    "IfcDuctFitting",
    "IfcDuctSegment",
    "IfcFan",
    "IfcFilter",
    "IfcFlowInstrument",
    "IfcPipeFitting",
    "IfcPipeSegment",
    "IfcPump",
    "IfcValve",
    "IfcBoiler",
    "IfcChiller",
    "IfcCoil",
    "IfcCondenser",
    "IfcCooledBeam",
    "IfcCoolingTower",
    "IfcEvaporator",
    "IfcHeatExchanger",
    "IfcHumidifier",
    "IfcTank",
    "IfcTubeBundle",
    "IfcUnitaryEquipment",

    # Infrastructure
    "IfcBridge",
    "IfcRoad",
    "IfcRailway",
    "IfcTunnel",
    "IfcCivilElement",
    "IfcEarthworksFill",
    "IfcEarthworksCut",
    "IfcKerb",
    "IfcPavement",
    "IfcReinforcedSoil",
    "IfcRetainingWall",
    "IfcSweptDrainageElement",
    "IfcTrackElement",
    "IfcSignal",
    "IfcPile",
    "IfcFooting",
    "IfcBorehole",
    "IfcGeoslice",
    "IfcGeotechnicalElement"
  ]

  return ifc_entities


def progress_bar(progress_text):
  my_bar = st.progress(0)
  for percent_complete in range(100):
      time.sleep(0.1)
      my_bar.progress(percent_complete + 1, text=progress_text)

def _load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def _load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def _get_translation(translations, key, lang):
    if key in translations and lang in translations[key]:
        return translations[key][lang]
    return key.capitalize()  # Fa[llback to capitalized key if translation not found

def custom_sidebar(current_language):

    config = _load_yaml('config.yaml')
    
    translations = _load_json('data/translations.json')
       
    # Use the created pages dictionary to build the sidebar with bold, black text links
    for page_key, page_file in config['pages'].items():
            translated_name = _get_translation(translations['sidebar_nav'], page_key, current_language)
            if page_key == 'home':
                st.sidebar.page_link(page_file, label=translated_name)
            else:
                st.sidebar.page_link(f"pages/{page_file}", label=translated_name)
    st.sidebar.divider()

# Usage in your main.py and other page files:
# from custom_sidebar import custom_sidebar
# custom_sidebar()