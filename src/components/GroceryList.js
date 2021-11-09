import React from 'react'
import { useState } from 'react'

function GroceryList(props) {
    let name = props.name;
    /* fetch function from "/saverecipes"? */

    return (
        <h1>Hello, {name}!</h1>
    )
}


export default GroceryList;