async function criarVoluntario() {
    const nome = document.getElementById("nome").value;
    const disponibilidade = document.getElementById("disponibilidade").value;
    const tipo_apoio = document.getElementById("tipo_apoio").value;
    const email = document.getElementById("email").value;

   const resposta = await fetch("/voluntarios", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            disponibilidade: disponibilidade,
            tipo_apoio: tipo_apoio,
            email: email,
        })
    });

    const data = await resposta.json();
    alert(data.message);
}