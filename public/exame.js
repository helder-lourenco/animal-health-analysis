async function carregarExames(idFiltro = "") {
  let url = "http://localhost:5000/exames";
  if (idFiltro) url += `?id=${encodeURIComponent(idFiltro)}`;
  const res = await fetch(url);
  const exames = await res.json();
  const tbody = document.querySelector("#exames-table tbody");
  tbody.innerHTML = "";
  exames.forEach((exame) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${exame.nome}</td>
      <td>${exame.id}</td>
      <td>${exame.documentos
        .map((doc) => `<a href="${doc}" target="_blank">Arquivo</a>`)
        .join(", ")}</td>
      <td><button onclick="analisarExame('${exame.id}')">Analisar</button></td>
    `;
    tbody.appendChild(tr);
  });
}

function buscarPorId() {
  const id = document.getElementById("search-id").value;
  carregarExames(id);
}

async function analisarExame(id) {
  const res = await fetch(
    `http://localhost:5000/analisar?id=${encodeURIComponent(id)}`
  );
  const data = await res.json();
  document.getElementById("popup-content").innerHTML = `
    <h2>Informações do Animal</h2>
    <p><strong>Nome:</strong> ${data.nome}</p>
    <p><strong>ID:</strong> ${data.id}</p>
    <p><strong>Resultado da Análise:</strong> ${data.resultado}</p>
  `;
  document.getElementById("popup").style.display = "block";
}

function fecharPopup() {
  document.getElementById("popup").style.display = "none";
}

window.onload = () => carregarExames();
