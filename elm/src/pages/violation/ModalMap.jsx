import {
  Map,
  InfoWindow,
  Marker,
  GoogleApiWrapper,
  Polyline,
  Circle,
} from "google-maps-react";
import { useEffect } from "react";
import React, { Component } from "react";

export class ModalMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      render: false,
    };
  }

  render() {
    const violationpoits = [
      [
        { lat: 24.922358026072622, lng: 67.11996880738931 },
        { lat: 24.92246847927999, lng: 67.1201142845463 },
      ],

      [
        { lat: 24.92261827860137, lng: 67.12030056411868 },
        { lat: 24.923897733081713, lng: 67.11916330757066 },
      ],
    ];

    return (
      <Map
        google={this.props.google}
        containerStyle={{}}
        style={{
          width: "45%",
          height: "270px",
          marginLeft: "15px",
          marginTop: "30px",
        }}
        center={this.props.latlng}
        initialCenter={this.props.latlng}
        zoom={16}
        disableDefaultUI={true}
      >
        <Circle
          radius={15}
          center={this.props.latlng}
          strokeColor="transparent"
          strokeOpacity={0}
          strokeWeight={5}
          fillColor="#FF0000"
          fillOpacity={0.8}
        />
      </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo",
})(ModalMap);
