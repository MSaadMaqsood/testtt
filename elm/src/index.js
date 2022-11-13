import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from './pages/dashboard/dashboard';
import Violation from './pages/violation/violation';
import Login from './pages/login/login';
import Google_Api from './pages/googleAPI/googleAPI';
import Verifier from './pages/verifier/verifier';
import Street from './pages/verifier/street';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
const root = ReactDOM.createRoot(document.getElementById('root'));
const server = "http://67.205.163.34:1244";
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route>
          
          <Route index element={<Login server={server}/>}/>
          <Route path="dashboard" element={<Dashboard  server={server}/>} />
          <Route path="violation/:id"  element={<Violation  server={server}/>} />
          <Route path="map_api" element={<Google_Api  server={server}/>} />
          <Route path="verifier"  element={<Verifier  server={server}/>} />
          <Route path="street"  element={<Street  server={server}/>} />
          <Route path="verifier/street/:id"  element={<Street  server={server}/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
