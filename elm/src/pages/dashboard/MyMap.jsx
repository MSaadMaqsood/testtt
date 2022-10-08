
import {Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';
import $ from 'jquery'; 
import { useEffect } from 'react';
import React, { Component } from "react";
import {
    GoogleMap,
    DirectionsService,
    DirectionsRenderer, LoadScript  
  } from '@react-google-maps/api';
  import { Circle, Polyline } from '@react-google-maps/api';

export default class MapContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            response: [],
            setter: false,
            street_id: [],
            show: false
     };
     this.directionsCallback = this.directionsCallback.bind(this)
     
}
directionsCallback  = para => response => {
  setTimeout(() => {  console.log("World!"); }, 2500);
  for (let i = 0; i < 100000000; i++) {
    let sdsdf= i;
    let dsfsd= i;
  }
  setTimeout(() => {  console.log("World!"); }, 2500);
    if (response !== null) {

      if (response.status === 'OK') {
        const coords = response.routes[0].overview_path;
        this.state.response.push({'res':coords,'str_id':para});

        console.log('response: ', response)
        this.setState({setter:true});
      } else {
        console.log('response: ', response)
      }
    }
    for (let i = 0; i < 100000000; i++) {
      let sdsdf= i;
      let dsfsd= i;
    }
    setTimeout(() => {  console.log("World!"); }, 2500);
  }
  add_street (id) {
    
        this.state.street_id.push(id);
    
  }
  sleep() {
    
  }
    render() {
      console.log(this.props.data)

     
      
        //  return (
        //      <Map
        //          google={this.props.google}
        //          containerStyle={{}}
        //          style={{width: "92%", height: "100%"}}
        //          center={{lat: 21.5102399, lng: 39.1995493}}
        //          initialCenter={{lat: 21.5102399, lng: 39.1995493}}
        //          zoom={12}
        //          disableDefaultUI={true}
        //     >
        //          {this.props.data.line.map((latlng) => (
        //              <Polyline
        //                 path={latlng}
        //                  strokeColor="red"
        //                  strokeOpacity={1}
        //                  strokeWeight={6}
        //                  onClick={() =>{  window.location.href ="/violation/"+latlng[0].street_id;  }}
        //              />
        //          ))}
        //          {
        //           this.props.data.circle.map((latlng)=>(
        //             <Circle
        //                 radius={7}
        //                 center={latlng}
        //                 onClick={() =>{  window.location.href ="/violation/"+latlng[0].street_id;  }}
        //                 strokeColor='transparent'
        //                 strokeOpacity={0}
        //                 strokeWeight={5}
        //                 fillColor='#FF0000'
        //                 fillOpacity={0.8}
        //               />
        //           ))
        //          }
        //      </Map>
        //  );

        return(<div style={{width: "100%", height: "100%"}}>
             <LoadScript
            googleMapsApiKey="AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
            style={{width: "100%", height: "100%"}}
          >
         <GoogleMap
                            id='direction-example'
                            mapContainerStyle={{width: "98%", height: "600px" }}
                            zoom={11}
                            center={{lat: 24.7478969, lng: 46.7861813}}
                            
           >
            {this.props.data.line.map((latlng) =>(
              
           <DirectionsService
                  
                  options={{ 
                    origin: latlng[0].lat+","+latlng[0].lng,
                    destination:  latlng[1].lat+","+latlng[1].lng,
                    travelMode: "WALKING",
                    
                    
                  }}
                  
                  callback={this.directionsCallback(latlng[0].street_id)}
                  onClick={() =>{  
                    // window.location.href ="/violation/1";  
                    console.log("hussain1");
                  }}
                />
                
                ))}
              {
                
                  this.state.response.map((res)=>(
                      
                      <Polyline
                        onClick={() =>{  window.location.href ="/violation/"+res.str_id;  }}
                        path={res.res}
                        options={{strokeColor: '#FF0000',
                        strokeOpacity: 0.8,
                        strokeWeight: 6,
                        fillColor: '#FF0000',
                        fillOpacity: 0.35,
                        draggable: false,
                        editable: false,
                        visible: true,
                        zIndex: 1}}
                    />
                  ))
                }
                {
                  this.props.data.circle.map((latlng)=>(
                    <Circle
                    center={latlng}
                        onClick={() =>{  window.location.href ="/violation/"+latlng.street_id;  }}
                        options={{strokeColor:'transparent',
                        strokeOpacity:100,
                        strokeWeight:50,
                        fillColor:'#FF0000',
                        fillOpacity:0.8,
                        radius: 8
                      }}
                      />
                  ))
                 }
          
          </GoogleMap>
          </LoadScript>
          </div>
          );
    }
  }
   
  //  export default GoogleApiWrapper({
  //    apiKey: "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
  //  })(MapContainer)
