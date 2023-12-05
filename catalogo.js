
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
        let form = document.createElement("form")
        form.setAttribute("method","post")
        if (game.subscrito){

            element = document.createElement("button")
            element.setAttribute("id","sub")
            element.setAttribute("type","submit")
            form.setAttribute("action","/cancelar")
            element.setAttribute("name","game")
            element.setAttribute("value",game.name)
            element.innerHTML="cancelar"
            form.append(element)
            localdiv.append(form)
        }else if (!game.subscrito){
            form.setAttribute("action","/apcetar")
            element = document.createElement("button")
            element.setAttribute("id","nosub")
            element.setAttribute("type","submit")
            element.setAttribute("name","game")
            element.setAttribute("value",game.name)
            element.innerHTML="subscribirse"
            form.append(element)
            localdiv.append(form)
        }

        target.append(localdiv)
        console.log(game)
        
        
    }

    
})
