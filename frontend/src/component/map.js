import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';


export default function Map({ longitude, latitude }) {
    const mapContainer = useRef(null);
    const [map, setMap] = useState(null);
    const [placeName, setPlaceName] = useState(null);
  
    useEffect(() => {
      if (mapContainer.current && !map) {
        const newMap = new mapboxgl.Map({
          container: mapContainer.current,
          style: 'mapbox://styles/mapbox/streets-v11',
          center: [longitude, latitude],
          zoom: 12,
        });
  
        const marker = new mapboxgl.Marker({ color: 'red' })
          .setLngLat([longitude, latitude])
          .addTo(newMap);
  
        mapboxgl.accessToken = 'pk.eyJ1IjoiYmV3aW4wMDciLCJhIjoiY2xma3h0ZXMzMGZtZjNxbHEzOGF5ZmpkeCJ9.aIme4c3n0jIx0zIjgZIqhg';

        fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${mapboxgl.accessToken}`)
        .then(response => response.json())
        .then(data => {
        const popup = new mapboxgl.Popup({ closeOnClick: true })
            .setLngLat([longitude, latitude])
            .setHTML(`<span style="color: red">${data.features[0].place_name}</span>`);

        marker.setPopup(popup);
        })
        .catch(error => console.error(error));

    setMap(newMap);
    }
    }, [map, longitude, latitude]);
  
    return <div ref={mapContainer} style={{ width: '100%', height: '400px' }} />;
  }
  
  