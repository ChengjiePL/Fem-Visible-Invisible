import React, { useState, useCallback } from "react";
import {
  GoogleMap,
  useLoadScript,
  Marker,
  Circle,
  StreetViewPanorama,
} from "@react-google-maps/api";

const libraries = ["places"];
const mapContainerStyle = {
  width: "100%",
  height: "400px",
  borderRadius: "8px",
  position: "relative",
};

const GoogleMaps = () => {
  const [center, setCenter] = useState({
    lat: 41.38879,
    lng: 2.15899,
  });
  const [streetViewLocation, setStreetViewLocation] = useState(null);

  const circleOptions = useCallback(
    (isInside) => ({
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: isInside ? 0.8 : 0.35,
      clickable: true,
      draggable: true,
      editable: true,
      visible: true,
      radius: 15000,
      zIndex: 1,
    }),
    [],
  );

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: "AIzaSyBCJ78Va7qnwkVhbyB7JkZTcqRWZa5zu9A",
    libraries,
    googleMapsApiOptions: {
      version: "weekly",
      crossOrigin: true,
    },
  });

  if (loadError) return <div>Error loading maps</div>;
  if (!isLoaded) return <div>Loading maps</div>;

  const handleMapClick = (event) => {
    setCenter({
      lat: event.latLng.lat(),
      lng: event.latLng.lng(),
    });
  };

  const handleStreetViewPositionChanged = (panorama) => {
    if (panorama) {
      const position = panorama.getPosition();
      if (position) {
        const distance =
          window.google.maps.geometry.spherical.computeDistanceBetween(
            new window.google.maps.LatLng(center.lat, center.lng),
            position,
          );
        setStreetViewLocation({
          lat: position.lat(),
          lng: position.lng(),
          isInside: distance <= 5000,
        });
      }
    }
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
      }}
    >
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={10}
        center={center}
        onClick={handleMapClick}
      >
        <Marker position={center} />
        <Circle
          center={center}
          options={circleOptions(streetViewLocation?.isInside)}
        />
        <StreetViewPanorama
          position={center}
          visible={true}
          onPositionChanged={() => handleStreetViewPositionChanged(this)}
        />
      </GoogleMap>
    </div>
  );
};

export default GoogleMaps;
