import React from "react";
import "./App.css";
// import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/register";
import Home from './pages'

// import Axios from "axios";
// import { useHistory } from "react-router-dom";
//import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/register" component={Register} />
        <Route path="/login" component={Login} />
      </Switch>
    </Router>
  );
}

export default App;
