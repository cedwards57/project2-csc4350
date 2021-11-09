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

  return (
<<<<<<< HEAD
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
=======
    <>
    <h1>Your Grocery List</h1>
    <div class="theTable">
      <table className="table table-striped table-dark">
        <thead>
          <tr>
            <th scope="col">#</th>
            {/* the next three columns should be variables passed form back end database */}
            <th scope="col">Ingredient</th>
            <th scope="col">Quantity</th>
            <th scope="col">Unit</th>
          </tr>
        </thead>
      </table>
    </div>
    </>
  );
>>>>>>> main
}

export default App;