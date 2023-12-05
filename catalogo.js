
fetch("/catalogo",{method: 'POST'})
.then(ret=>ret.json())
.then(function(data){


    let target = document.querySelector("#juegos")
    for (let game of data.video_games){
        let localdiv = document.createElement("div")
        let element = document.createElement("h1")
        element.innerHTML=game.name
        localdiv.append(element)
        element = document.createElement("h2")
        element.innerHTML=game.developer
        localdiv.append(element)
        element = document.createElement("p")
        element.innerHTML = game.genere
        localdiv.append(element)
        element = document.createElement("p")
        element.innerHTML = game.description
        localdiv.append(element)
        localdiv.append(element)
        element = document.createElement("img")
        element.setAttribute("src",game.image)
        element.style.width = "60%"
        localdiv.append(element)

        if (game.subscrito){
            element = document.createElement("button")
            element.setAttribute("id","sub")
            element.setAttribute("type","submit")
            element.setAttribute("action","/cancelar")
            element.setAttribute("value",game.name)
            element.innerHTML="cancelar"
            localdiv.append(element)
        }else if (!game.subscrito){
            element = document.createElement("button")
            element.setAttribute("id","nosub")
            element.setAttribute("type","submit")
            element.setAttribute("action","/acetar")
            element.setAttribute("value",game.name)
            element.innerHTML="subscribirse"
            localdiv.append(element)
        }

        target.append(localdiv)
        console.log(game)
        
        
    }

    
})
