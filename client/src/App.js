import React from "react";
import { BrowserRouter, Switch, Route, Redirect } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import Home from "./components/Home/Home";

const App = () => {
  return (
    <BrowserRouter>
      {/* <Container maxWidth="xl"> */}
      <Navbar />
      <Switch>
        <Route path="/" exact component={() => <Redirect to="/stream" />} />
        <Route path="/stream" exact component={Home} />
      </Switch>
      {/* </Container> */}
    </BrowserRouter>
  );
};

export default App;
