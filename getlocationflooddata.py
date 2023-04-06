import requests

def getflooddata(x, y):
    x1 = x + 0.0001
    y1 = y + 0.0001
    bbox = [y, x, y1, x1]

    # Convert the bbox list to a string
    bbox_str = ','.join(str(coord) for coord in bbox)

    # Define the common URL parameters
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetFeatureInfo",
        "FORMAT": "image/png",
        "TRANSPARENT": "true",
        "INFO_FORMAT": "application/json",
        "FEATURE_COUNT": "8",
        "I": "50",
        "J": "50",
        "CRS": "EPSG:4326",
        "STYLES": "",
        "WIDTH": "101",
        "HEIGHT": "101",
        "BBOX": bbox_str,
        "x": x,
        "y": y,
    }

    # Define a dictionary to store the responses
    responses = {}

    # Define a list of layers to query
    layers = ["overstromingsdiepte_extreem_kleine_kans", "overstromingsdiepte_kleine_kans", "overstromingsdiepte_middelgrote_kans", "overstromingsdiepte_grote_kans"]

    # Loop over the layers and make separate requests for each layer
    for layer in layers:
        params["QUERY_LAYERS"] = layer
        params["LAYERS"] = layer
        
        # Construct the URL using string formatting
        url = "https://apps.geodan.nl/public/data/org/gws/YWFMLMWERURF/kea_public/wms?v1_0&" + "&".join("{}={}".format(k, v) for k, v in params.items())
        
        # Send the request and parse the JSON response
        response = requests.get(url)
        data = response.json()
        
        # Store the response in the dictionary
        responses[layer] = data

        # Extract the "properties" field from the response
        properties = data["features"][0]["properties"]
        
        # Get the "GRAY_INDEX" value and check if it's -9999
        gray_index = properties['GRAY_INDEX']
        if gray_index == -9999:
            gray_index = 0

        # Store the numerical value in the corresponding variable
        if layer == "overstromingsdiepte_extreem_kleine_kans":
            extreem_kleine_kans_val = gray_index
        elif layer == "overstromingsdiepte_kleine_kans":
            kleine_kans_val = gray_index
        elif layer == "overstromingsdiepte_middelgrote_kans":
            middelgrote_kans_val = gray_index
        elif layer == "overstromingsdiepte_grote_kans":
            grote_kans_val = gray_index

            design_stillwater_depths = [extreem_kleine_kans_val, kleine_kans_val, middelgrote_kans_val, grote_kans_val]

    return design_stillwater_depths