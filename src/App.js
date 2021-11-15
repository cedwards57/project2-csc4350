import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';
import { BrowserRouter as Router, Routes as Switch, Route, Link, Redirect } from 'react-router-dom'
import GroceryList from './components/GroceryList'
import RecipeList from './components/RecipeList'

function App() {
  const args = JSON.parse(document.getElementById("data").text);

  return (
    <Router>
      <div>
        <Switch>
          <Route exact path="/grocerylist" >
            <GroceryList name={args.name} />
          </Route>
          <Route exact path="/recipelist">
            <RecipeList name={args.name} />
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