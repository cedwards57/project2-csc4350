import React from 'react'

export function ResultRecipe(props) {
    return (
        <p><form action="/recipe" method="get"><input type="hidden" name="recipeid" value={props.id} />{props.title} <input class="button3" type="submit" value="More Details"/></form></p>
    )
}
