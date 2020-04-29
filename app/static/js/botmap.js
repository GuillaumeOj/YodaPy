class BotMap {
    constructor(feed) {
        this.mapId = 0;
        this.feed = feed;
    }

    createMap(coordinates) {
        this.mapId++;

        // Create a container for the map
        let mapDiv = document.createElement("div");
        mapDiv.id = "map-" + this.mapId;
        mapDiv.classList.add("post", "incoming", "map");
        this.feed.write(mapDiv);


        // Create the map
        let map = new mapboxgl.Map({
            container: mapDiv.id, // Container ID
            style: "mapbox://styles/mapbox/streets-v10", // Map style to use
            center: coordinates,// Starting position [lng, lat]
            zoom: 14, // Starting zoom level
        });

        // Change map language for french
        let language = new MapboxLanguage({
            defaultLanguage: "fr"
        });
        map.addControl(language);

        // Add a marker to the map
        new mapboxgl.Marker() // initialize a new marker
            .setLngLat(coordinates) // Marker [lng, lat] coordinates
            .addTo(map); // Add the marker to the map
    }
}
