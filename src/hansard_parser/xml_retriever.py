import requests


def download_xml_file(
        hansard_xml_url: str, 
        file_date: str,
        output_dir: str
    ):
    """
    Download XML files from a given URL based on the provided file date.

    Parameters:
    - hansard_xml_url (str): The URL where the XML files are located.
    - file_date (str): The date associated with the XML files to be downloaded.

    Returns:
    This function does not return anything.
    """
        
    file_version_suffixes = [chr(i) for i in range(ord('a'), ord('z')+1)]
    for file_version_suffix in file_version_suffixes:
        xml_filename = f"debates{file_date}{file_version_suffix}.xml"
        response = requests.get(f"{hansard_xml_url}/{xml_filename}")
    
        if response.status_code == 200:
            with open(f"{output_dir}\\{xml_filename}", 'wb') as file:
                file.write(response.content)
        else:
            break