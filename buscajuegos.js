fetch("juegos.json")
.then((data)=>data.json())
.then(function(info){
    let form = document.getElementById("registro")
    for (let game of info.video_games){
        let check = document.createElement("input")
        check.setAttribute("type","checkbox")
        check.setAttribute("name","juegos")
        check.setAttribute("value",game.name)
        let label = document.createElement("label")
        label.innerHTML = game.name
        form.append(label)
        form.append(check)
        form.append(document.createElement("br"))

    }

    let ok = document.createElement("button")
    ok.setAttribute("type","submit")
    ok.innerHTML ="Registrarse"
    form.append(ok)

})