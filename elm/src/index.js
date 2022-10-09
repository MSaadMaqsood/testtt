import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from './pages/dashboard/dashboard';
import Violation from './pages/violation/violation';

import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
const root = ReactDOM.createRoot(document.getElementById('root'));
//const server = "http://127.0.0.1:4587";
const server = "http://67.205.163.34:4587";
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route>
          
          <Route index element={<Dashboard server={server}/>} />
          <Route path="dashboard" element={<Dashboard  server={server}/>} />
          <Route path="violation/:id"  element={<Violation  server={server}/>} />
          
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
