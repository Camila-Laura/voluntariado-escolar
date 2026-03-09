//esta função serve para pegar os dados que foram enviados do front end e enviar para o servidor
async function criarSolicitante() {   
    const nome = document.getElementById("nome").value; // pega o valor digitado no front end e adciona na variavel
    const dificuldade = document.getElementById("dificuldade").value;
    const horario_disponivel = document.getElementById("horario_disponivel").value;
    const email = document.getElementById("email").value; 

    const resposta = await fetch("/solicitante", { // faz uma requisição para a rota indicada
        method: "POST",                              // envia os dados para o backend
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({           // transforma os dados em formato json para mandar para o flask
            nome: nome,
            dificuldade: dificuldade,
            horario_disponivel: horario_disponivel,
            email: email
        })
    });
    const data = await resposta.json(); // converte a reposta em json e armazena na  variavel
    alert(data.message);
}