const API_URL = "http://127.0.0.1:5000";


// async function carregarVoluntarios() {
//     const response = await fetch(`${API_URL}/voluntarios`);
//     const voluntarios = await response.json();

//     const tbody = document.querySelector("#tabelaVoluntarios tbody");
//     tbody.innerHTML = "";

//     voluntarios.forEach(v => {
//         const tr = document.createElement("tr");
//         tr.innerHTML = `
//             <td>${v.id}</td>
//             <td>${v.nome}</td>
//             <td>${v.disponibilidade}</td>
//             <td>${v.tipo_apoio}</td>
//             <td>${v.email}</td>
//         `;
//         tbody.appendChild(tr);
//     });
// }

// carregarVoluntarios();


function Login() {
    const email = document.getElementById("login").value;
    const senha = document.getElementById("senha").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            senha: senha
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            window.location.href = "/admin";  
        } else {
            alert("E-mail ou senha inválidos!");
        }
    })
    .catch(error => {
        console.error("Erro:", error);
    });
}
