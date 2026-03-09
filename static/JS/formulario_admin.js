async function criarAdmin() {
    const nome = document.getElementById("nome").value;
    const cargo = document.getElementById("cargo").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    const confirmar_senha = document.getElementById("confirmar_senha").value;

    const resposta = await fetch("/cadastro-administrador", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            cargo: cargo,
            email: email,
            senha: senha,
            confirmar_senha: confirmar_senha
        })
    });

    const data = await resposta.json();
    alert(data.message);

}