
import {Map, InfoWindow, Marker, GoogleApiWrapper, Polyline, Circle} from 'google-maps-react';
import { useEffect } from 'react';
import React, { Component } from "react";
import {
    GoogleMap,
    DirectionsService,
    DirectionsRenderer, LoadScript 
  } from '@react-google-maps/api'

export class MapContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            response: null,
     };
     this.directionsCallback = this.directionsCallback.bind(this)
}
directionsCallback (response) {
    console.log(response)

    if (response !== null) {
      if (response.status === 'OK') {
        this.setState(
          () => ({
            response
          })
        )
      } else {
        console.log('response: ', response)
      }
    }
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
                 style={{width: "92%", height: "100%"}}
                 center={{lat: 21.5102399, lng: 39.1995493}}
                 initialCenter={{lat: 21.5102399, lng: 39.1995493}}
                 zoom={12}
                 disableDefaultUI={true}
            >
                 {this.props.data.line.map((latlng) => (
                     <Polyline
                        path={latlng}
                         strokeColor="red"
                         strokeOpacity={1}
                         strokeWeight={6}
                         onClick={() =>{  window.location.href ="/violation/"+latlng[0].street_id;  }}
                     />
                 ))}
                 {
                  this.props.data.circle.map((latlng)=>(
                    <Circle
                        radius={7}
                        center={latlng}
                        onClick={() =>{  window.location.href ="/violation/"+latlng[0].street_id;  }}
                        strokeColor='transparent'
                        strokeOpacity={0}
                        strokeWeight={5}
                        fillColor='#FF0000'
                        fillOpacity={0.8}
                      />
                  ))
                 }
             </Map>
         );

        // return(<div style={{width: "90%", height: "100%"}}>
        //     <LoadScript
        //     googleMapsApiKey="AIzaSyB9Vn8oxR_0zSETwnggqgVRNz9rRxyQwTw"
        //     style={{width: "90%", height: "100%"}}
        //   >
        // <GoogleMap
        //                     id='direction-example'
        //                     mapContainerStyle={{width: "98%", height: "600px" }}
        //                     zoom={12}
        //                     center={{lat: 21.5102399, lng: 39.1995493}}
                            
        //   >
        //    <DirectionsService
        //           // required
        //           options={{ 
        //             origin: "21.550661,39.221493",
        //             destination:  "21.548605,39.221821",
        //             travelMode: "WALKING"
        //           }}
        //           // required
        //           callback={this.directionsCallback}
                  
        //         />
        //         {
        //       this.state.response !== null && (
        //         <DirectionsRenderer
        //           // required
        //           options={{ 
        //             directions: this.state.response
        //           }}
                  
        //         />
        //       )
        //     }
        //   </GoogleMap>
        //   </LoadScript>
        //   </div>
        //   );
    }
  }
   
   export default GoogleApiWrapper({
     apiKey: "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
   })(MapContainer)
