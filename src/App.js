import logo from './logo.svg';
import './App.css';

function App() {
  const args = JSON.parse(document.getElementById("data").text);
  
  return (
    <h1>{args["name"]} {args["recipes"]}</h1>
  );
}

export default App;