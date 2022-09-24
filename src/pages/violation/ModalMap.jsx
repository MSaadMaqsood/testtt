import {
  Map,
  InfoWindow,
  Marker,
  GoogleApiWrapper,
  Polyline,
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
        style={{ width: "45%", height: "300px", marginLeft:"10px" }}
        center={{ lat: 24.92231296013835, lng: 67.11994378679105 }}
        initialCenter={{ lat: 24.92231296013835, lng: 67.11994378679105 }}
        zoom={15}
        disableDefaultUI={true}
      >
        {this.state.render &&
          this.state.data.map((latlng) => (
            <Polyline
              path={latlng}
              strokeColor="red"
              strokeOpacity={1}
              strokeWeight={12}
              onClick={() => {
                window.location.href = "/violation/" + latlng[0].devid;
              }}
            />
          ))}
      </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo",
})(ModalMap);
