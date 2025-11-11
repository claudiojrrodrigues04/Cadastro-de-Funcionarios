// app/static/app.js
console.log("App.js carregado.");

// Função principal que será executada quando o DOM estiver pronto
function main() {
  
  // Intercepta o envio de formulários que usam 'data-method'
  // (Usado para botões de Excluir e formulários de Editar)
  document.querySelectorAll('form[data-method]').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault(); // Impede o envio normal (POST)
      
      const method = this.getAttribute('data-method').toUpperCase();
      const action = this.getAttribute('action');

      // Pega os dados do formulário (para PUT)
      const formData = new FormData(this);
      
      // Define o método da requisição
      let options = {
        method: method,
        headers: {},
      };

      // Se for PUT ou POST, envia o corpo (body)
      if (method === 'PUT' || method === 'POST') {
        options.body = formData;
      }
      
      console.log(`Interceptado: ${method} para ${action}`);

      // Faz a requisição "correta" (PUT ou DELETE)
      fetch(action, options)
        .then(response => {
          // Se for 204 (No Content), ou 303 (See Other), ou 200 (OK)
          // significa que funcionou. Recarrega a página de lista.
          if (response.status === 204 || response.status === 303 || response.status === 200) {
            console.log("Sucesso! Redirecionando para /employees");
            window.location.href = '/employees';
          } else {
            // Se der erro, mostra no console
            console.error('Falha na requisição:', response.statusText);
            alert('Ocorreu um erro ao processar a requisição.');
          }
        })
        .catch(error => {
          console.error('Erro de rede:', error);
          alert('Erro de rede. Verifique o console.');
        });
    });
  });
}

// Garante que o script só rode depois que a página carregar
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', main);
} else {
  main();
}