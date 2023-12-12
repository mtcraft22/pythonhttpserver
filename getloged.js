fetch("/logedinfo",{method:'POST'})
.then(
    function(ret){
        if (ret.status ==200){
            return ret.json()
        }
    }
).then(function(data){
    let menu = document.getElementsByTagName("mt-vsiderbar")
    let dest = document.getElementById("user")


    let username  = document.createElement("p")
    dest.append(username)

    username.innerHTML=data.nombre
})