import React, { useEffect } from 'react'
import './App.css';
import main from './components/main'
import {BrowserRouter as Router, Route} from "react-router-dom"
import {Redirect} from "react-router-dom"


class App extends React.Component{
  render(){

    
  return (
    <div className="container">
    <Router>

              <Route exact path="/">
                  <Redirect to="/Participants" />
              </Route>

              <Route path="/Participants" component={main} />
    </Router>
        


    </div>
  );
}

}
export default App;
