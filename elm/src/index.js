import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard/dashboard";
import Violation from "./pages/violation/violation";
import Login from "./pages/login/login";
import Google_Api from "./pages/googleAPI/googleAPI";
import Verifier from "./pages/verifier/verifier";
import Street from "./pages/verifier/street";
import UserActivity from "./pages/verifier/user_activity/user_activity";
import AllViolations from "./pages/allViolations/AllViolations";
import DuplicatePage from "./pages/duplicatePage/duplicatePage";
import Exe_Dashboard from "./pages/executive/dashboard/exe_dashboard";
import Exe_AllViolations from "./pages/executive/allViolations/exe_allviolation";
import ViewUserLogActivity from "./pages/executive/usermanagement/view_user_log_activity/view_user_log_activity";
import UserManagement from "./pages/executive/usermanagement/usermanagement";
import reportWebVitals from "./reportWebVitals";
import "bootstrap/dist/css/bootstrap.min.css";
const root = ReactDOM.createRoot(document.getElementById("root"));
//const server = "http://67.205.163.34:1244";
const server = "http://127.0.0.1:1244";
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route>
          <Route index element={<Login server={server} />} />
          <Route path="dashboard" element={<Dashboard server={server} />} />
          <Route path="violation/:id" element={<Violation server={server} />} />
          <Route path="map_api" element={<Google_Api server={server} />} />
          <Route path="verifier" element={<Verifier server={server} />} />
          <Route
            path="verifier/street/:id"
            element={<Street server={server} />}
          />
          <Route
            path="verifier/user/:id"
            element={<UserActivity server={server} />}
          />
          <Route
            path="allviolations"
            element={<AllViolations server={server} />}
          />
          <Route
            path="duplicatepage"
            element={<DuplicatePage server={server} />}
          />
          <Route
            path="exe_dashboard"
            element={<Exe_Dashboard server={server} />}
          />
          <Route
            path="exe_allviolations"
            element={<Exe_AllViolations server={server} />}
          />
          <Route
            path="usermanagement"
            element={<UserManagement server={server} />}
          />
          <Route
            path="usermanagement/userlog/:id"
            element={<ViewUserLogActivity server={server} />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
