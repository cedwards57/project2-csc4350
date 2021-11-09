import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from 'react-router-dom'


 function getMealData() {
    const [mealData, setMealData] = useState(null)
    fetch('/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mealData),
    })
      .then(response => response.json())
      .then(data => {
        setMealData(data)
      })
      .catch(() => {
        console.log("error")
      })
  }

function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  var convert = require('convert-units')
  const [amnt, setamnt] = useState('');
  const [unt, setunt] = useState('');

  function add_quantities(amnt1, unt1, amnt2, unt2){
    if(unt1 == unt2){
      setunt(unt1)
      setamnt(amnt1 + amnt2)
    }
    else {
      if (convert(amnt1).from(unt1).to(unt2) < 1) {
        setunt(unt1)
        setamnt(amnt1 + convert(amnt2).from(unt2).to(unt1))
      }
      else {
        setunt(unt2)
        setamnt(amnt2 + convert(amnt1).from(unt1).to(unt2))
      }
    }

    return {"amount" : amnt, "unit": unt}
  }

  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/about">About</Link>
            </li>
            <li>
              <Link to="/users">Users</Link>
            </li>
          </ul>
        </nav>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route exact path="/about">
            <About />
          </Route>
          <Route exact path="/users">
            <div>
              <p>Hello World!</p>
              <ol>
                <li>hey</li>
              </ol>
            </div>
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>HELLO WORLD</h2>;
}

function Users() {
  return (<h2>Users</h2>);
}

export default App;