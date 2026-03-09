 document.addEventListener("DOMContentLoaded", carregarAtendimentos);

function carregarAtendimentos() {
    fetch("/api/atendimentos")
    .then(response => response.json())
    .then(data => {
        const tbody = document.querySelector("#tabelaAtendimentos tbody");
        tbody.innerHTML = "";

        if (data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='4' class='text-center'>Nenhum atendimento cadastrado.</td></tr>";
            return;
        }

        data.forEach(a => {         //para cada dado que veio do banco de dados ele cria uma linha na tabela
            tbody.innerHTML += `
                <tr>
                    <td>${a.id}</td>
                    <td>${a.voluntario_nome}</td>
                    <td>${a.solicitante_nome}</td>
                    <td> <button onclick="deletarAtendimento(${a.id})" class="btn btn-danger fw-semibold btn-sm w-50">Deletar</button></td>
                </tr>
            `;
        });
    })
    .catch(err => console.error("Erro:", err));
}

function criarAtendimento() {
    const voluntario_id = document.getElementById("voluntario_id").value; // responsavel por pegar os dados do input
    const solicitante_id = document.getElementById("solicitante_id").value;

    if (!voluntario_id || !solicitante_id) {        //faz a verificação para analisar se tem algum campo vazio
        alert("Preencha os dois campos!");
        return;
    }
    console.log("Enviando:", voluntario_id, solicitante_id);

    fetch("/api/atendimentos", {        //envia novo atendimento ao servidor
        method: "POST",
        headers: { "Content-Type": "application/json" }, // serve para informar ao servidor qual tipo de dado  ta sendo enviado
        body: JSON.stringify({
        voluntario_id: parseInt(voluntario_id), // responsavel por transformar os textos em numeros
        solicitante_id: parseInt(solicitante_id)
        })
    })
    .then(response => response.json()) //responsavel por transformar as respostas do servidor em json
    .then(data => {                         //recebe os dados
        console.log("Resposta:", data)
        alert(data.message);
        carregarAtendimentos();
    });
}

function deletarAtendimento(id) {
    if (!confirm("Tem certeza que deseja deletar?")) return;

        fetch(`/api/atendimentos/${id}`, { method: "DELETE" })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            carregarAtendimentos();
    });
}