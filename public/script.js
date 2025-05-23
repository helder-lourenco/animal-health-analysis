const form = document.getElementById("animal-form");
const fileInput = document.getElementById("file-input");
const nameInput = document.getElementById("name-input");
const healthStatusInput = document.getElementById("health-status-input");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = fileInput.files[0];
  const name = nameInput.value;
  const healthStatus = healthStatusInput.value;

  if (!file || !name || !healthStatus) {
    alert("Please fill in all fields and select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  formData.append("healthStatus", healthStatus);

  try {
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();
      alert("Data uploaded successfully: " + JSON.stringify(result));
      window.location.href = "exame.html";
    } else {
      alert("Error uploading data: " + response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while uploading data.");
  }
});

window.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("animal-form")
    .addEventListener("submit", async function (e) {
      e.preventDefault();

      const name = document.getElementById("animal-name").value;
      const id = document.getElementById("health-status").value;
      const fileInput = document.getElementById("file-upload");
      if (!fileInput) {
        document.getElementById("status-message").textContent =
          "Campo de arquivo não encontrado!";
        return;
      }
      const files = fileInput.files;

      if (!files.length) {
        document.getElementById("status-message").textContent =
          "Selecione pelo menos um arquivo.";
        return;
      }

      const formData = new FormData();
      formData.append("name", name);
      formData.append("id", id);
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }

      try {
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();
        if (response.ok) {
          window.location.href = "exame.html";
        } else {
          document.getElementById("status-message").textContent =
            result.error || "Erro ao enviar.";
        }
      } catch (err) {
        document.getElementById("status-message").textContent =
          "Erro de conexão com o servidor.";
      }
    });
});
