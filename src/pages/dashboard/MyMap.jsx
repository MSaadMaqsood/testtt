
import {Map, InfoWindow, Marker, GoogleApiWrapper, Polyline} from 'google-maps-react';
import { useEffect } from 'react';
import React, { Component } from "react";


export class MapContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
        data: [],
        render: false,
        
     };

   
    this.GetData = this.GetData.bind(this);
    
     
}
componentDidMount() {
    setTimeout(function() { 
        this.setState({render: true}) 
    }.bind(this), 500)
}

GetData() {
    const com = this;
    const axios = require('axios').default;
    axios.get('http://67.205.163.34:1159/get_all_violations_loc_list')
    .then(function (response) {
      // handle success
      
      com.setState({
            data: response.data.myData
          });
    })
    
  }

    render() {
        const violationpoits=[ 
        
            [
            {lat: 24.922358026072622, lng: 67.11996880738931, devid: 1},
            {lat: 24.92246847927999, lng:67.1201142845463, devid: 1},
            ],
            [
                {lat: 24.92261827860137, lng:67.12030056411868, devid: 2},
                {lat:  24.923897733081713, lng:67.11916330757066, devid: 2},
            ],
            [
                {lat: 24.923479, lng:67.117335, devid: 3},
                {lat:  24.924371, lng:67.118565, devid: 3},
            ]
           
        ]
    
        return (
            <Map
                google={this.props.google}
                containerStyle={{}}
                style={{width: "90%", height: "100%"}}
                center={{lat: 24.92231296013835, lng: 67.11994378679105}}
                initialCenter={{lat: 24.92231296013835, lng: 67.11994378679105}}
                zoom={16}
                disableDefaultUI={true}
            >
                {violationpoits.map((latlng) => (
                    <Polyline
                        path={latlng}
                        strokeColor="red"
                        strokeOpacity={1}
                        strokeWeight={6}
                        onClick={() =>{  window.location.href ="/violation/"+latlng[0].devid;  }}
                    />
                ))}
            </Map>
        );
    }
  }
   
  export default GoogleApiWrapper({
    apiKey: "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
  })(MapContainer)
