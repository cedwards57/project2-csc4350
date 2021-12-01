import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';
import { ResultRecipe } from './components/ResultRecipe'
import { UserRecipe } from './components/UserRecipe'

function App() {
  const args = JSON.parse(document.getElementById("data").text);
  const [recipeList, updateRecipeList] = useState(args.recipes);
  const [searchRecipes, updateSearchRecipes] = useState([]);
  const [delRecipes, updateDelRecipes] = useState([]);
  const [addRecipes, updateAddRecipes] = useState([]);
  const inputRef = useRef(null);
  
  function searchRecipe() {
    let query = document.getElementById("searchQuery").value
    fetch("/searchrecipes", {
      method:"POST",
      cache: "no-cache",
      headers:{
          "content_type":"application/json",
      },
      body:JSON.stringify({"query": query})
    }
    ).then(response => {
      return response.json();
    }).then(data => {
      updateSearchRecipes(data.results);
    })
  }

  function saveChanges() {
    fetch("/saverecipes", {
      method:"POST",
      cache: "no-cache",
      headers:{
          "content_type":"application/json",
      },
      body:JSON.stringify({"delRecipes": delRecipes, "addRecipes": addRecipes})
    }
    ).then(response => {
      return response.json();
    }).then(data => {
      updateRecipeList(data.newRecipeList);
      updateAddRecipes([]);
      updateDelRecipes([]);
    })
  }

  function addRecipe(add_recipe) {
    let newAddRecipes = [...addRecipes, add_recipe["id"]];
    updateAddRecipes(newAddRecipes);
    let newRecipeList = [...recipeList, add_recipe];
    updateRecipeList(newRecipeList);
  }

  function delRecipe(del_recipe) {
    let newDelRecipes = [...delRecipes, del_recipe["id"]];
    updateAddRecipes(newDelRecipes);
    let remove_index = recipeList.indexOf(del_recipe);
    let newRecipeList = [...recipeList];
    newRecipeList.splice(remove_index,1);
    updateRecipeList(newRecipeList);
    console.log(newRecipeList);
    console.log(delRecipes);
  }

  return (
    <>
    <ul>
      <li><a href="/recipelist">Recipe List</a></li>
      <li><a href="/">Grocery List</a></li>
      <li><a href="/logout">logout</a></li>
    </ul>
    
    <h1>{args.name}</h1>
    <input type="text" id="searchQuery" placeholder="Search by ingredient..." /><button onClick={searchRecipe}>Search</button>
    {searchRecipes.map((item, k) => <p><ResultRecipe id={item.id} title={item.title}/><button onClick={() => addRecipe(item)}>Add Recipe</button></p>)}
    <h3>Your Recipes</h3>
    {recipeList.map((item, j) => <p><UserRecipe id={item.id} title={item.title}/><button onClick={() => delRecipe(item)}>Delete</button></p>)}
    <button onClick={saveChanges}>Save Changes</button>
    </>
  );
}


export default App;
